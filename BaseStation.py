import Cell
import math

CollectionModes = ["TIP","TDPTrain","TDP"]
BaseLinePrice = 10.0

class BaseStation( Cell.Cell ):
    def __init__( self, system, center, radius, id, capacity ):
        Cell.Cell.__init__( self, center, radius )
        self.system = system
        self.N = system.getUpdatePerDay()
        self.M = system.getPtClassCount()
        N = self.N
        M = self.M
        self.id = id
        self.curTraffic = []        # current traffic set
        self.nearbyBs = {}
        self.baseline = [BaseLinePrice] * N
        self.capacity = capacity    # N*1 network capacity
        self.discount = [1.0] * N   # N*1 discount
        self.TIP = [0.0] * N        # N*1 base traffic
        self.TDP = [0.0] * N        # N*1 TDP traffic
        self.ptIndex = [1.0] * M    # M*1 pt index
        self.ptConst = [1.0] * M    # M*1 lamda
        self.ptRitio = []           # N*M ptclass fraction in a period
        for i in range(N):
            self.ptRitio.append([1.0/M]*M)
        self.mode = "TIP"

    def changeMode(self, newmode):
        self.mode = newmode
        if (newmode == "TDPTrain"):
            for i in range(self.N):
                self.TDP[i] = self.TIP[i]

    def addNearbyBs( self, baseStation ):
        self.nearbyBs[ baseStation.id ] = baseStation

    def clearNearbyBs( self ):
        self.nearbyBs.clear()

    def recordTraffic(self, traffic):
        # traffic is a list of [traffic TI apptype]
        for data in traffic:
            self.curTraffic.append(data)
    
    def updatePrice(self):
        print "station" + str(self.id)
        # first calculate the traffic of last slot from curTraffic
        ptClassCount = self.M
        curSlot = self.system.getCurrentUpdateIndex()
        lastSlot = (curSlot - 1) %  self.N
        ptIndexSum = [0.0] * ptClassCount
        ptTraffic = [0.0] * ptClassCount
        totalTraffic = 0.0
        for [traffic, ptIndex, appType] in self.curTraffic:
            appType = appType - 1
            ptIndexSum[appType] += ptIndex * traffic
            ptTraffic[appType] += traffic
            totalTraffic += traffic
        
        if (self.mode == "TIP"):
            self.TIP[lastSlot] = totalTraffic
            #print self.TIP
        else:
            self.TDP[lastSlot] = totalTraffic
            #print self.TDP
            self.calculatePtIndexRatio(lastSlot, ptIndexSum, ptTraffic, totalTraffic)
            #print ptIndexSum
            #print ptTraffic, totalTraffic
            #print self.ptIndex
            #print self.ptRitio
        
        # clean up traffic variables
        self.curTraffic = []
            
        # then do calculate
        if (self.mode != "TIP"):
            self.calculatePrice(lastSlot)


    def calculatePtIndexRatio(self, time, ptIndexSum, ptTraffic, totalTraffic):
        if (totalTraffic == 0):
            return    # assume no change in index and pt
        
        predictPeriod = self.N
        ptClassCount = self.M
        for j in range(ptClassCount):
            self.ptRitio[time][j] = ptTraffic[j] / totalTraffic
            if (ptTraffic[j] == 0):
                pass
            else:
                otherPtTraffic = 0.0
                for i in range(predictPeriod):
                    if i != time:
                        otherPtTraffic += self.TDP[i] * self.ptRitio[i][j]
                self.ptIndex[j] = (ptIndexSum[j] + self.ptIndex[j] * otherPtTraffic) \
                                  / (ptTraffic[j] + otherPtTraffic)
            

    def calculatePrice(self, time):
        self.findLamda(self.baseline)
        #print self.ptConst
        self.minimizeGamma(time)
        print self.discount

    def getPrice( self, offset ):
        index = (self.system.getCurrentUpdateIndex() + offset) % self.N
        if (self.mode == "TIP"):
            return self.baseline[index]
        else:
            return self.baseline[index] - self.discount[index]

    def calculateGamma(self):
        predictPeriod = self.N
        ptClassCount = self.M
        gamma1 = 0.0
        gamma2 = 0.0
        for i in range(predictPeriod):
            sigmaAki = 0.0
            mu = self.ptRitio[i]
            for k in range(predictPeriod):
                if i == k:
                    continue
                sigmaAki += self.calculateAik(k,i)
            sigmaDeleyIn = 0.0
            for j in range(ptClassCount):
                sigmaWaiting = 0.0
                for k in range(predictPeriod):
                    if i == k:
                        continue
                    d = self.discount[k]
                    t = (k - i) % predictPeriod
                    sigmaWaiting += self.waitingFunction(j, d, t)
                sigmaDeleyIn += mu[j] * sigmaWaiting
            gamma1 += self.networkcostFunction(self.TIP[i] * (1 - sigmaDeleyIn)
                                          + sigmaAki - self.capacity[i])
            gamma2 += self.discount[i] * sigmaAki
        #print gamma1, gamma2
        return gamma1 + gamma2

    def minimizeGamma(self, time):
        lowPrice = 0
        highPrice = self.baseline[time]
        self.discount[time] = self.baseline[time] - lowPrice
        lowGamma = self.calculateGamma()
        self.discount[time] = self.baseline[time] - highPrice
        highGamma = self.calculateGamma()                
        bestPrice = self.minimizeGammaHelper(
            time, lowPrice, lowGamma, highPrice, highGamma)
        self.discount[time] = self.baseline[time] - bestPrice
    
    def minimizeGammaHelper(self, time,
                            lowPrice, lowGamma, highPrice, highGamma):
        delta = 0.01
        roundDigit = 2
        if (highPrice - lowPrice) < delta:
            return round((highPrice + lowPrice)/2, roundDigit)
        midlowPrice = (highPrice - lowPrice) / 3 + lowPrice
        self.discount[time] = self.baseline[time] - midlowPrice
        midlowGamma = self.calculateGamma()
        midhighPrice = highPrice - (highPrice - lowPrice) / 3
        self.discount[time] = self.baseline[time] - midhighPrice
        midhighGamma = self.calculateGamma()
        if (midlowGamma == midhighGamma):
            # must be the case: lowGamma > midlowGamma = midhighGamma < high
            return self.minimizeGammaHelper(
                time, midlowPrice, midlowGamma, midhighPrice, midhighGamma)
        elif (midlowGamma < midhighGamma):
            if (lowGamma > midlowGamma):
                return self.minimizeGammaHelper(
                    time, lowPrice, lowGamma, midhighPrice, midhighGamma)
            else: # (lowGamma <= midlowGamma)
                return self.minimizeGammaHelper(
                    time, lowPrice, lowGamma, midlowPrice, midlowGamma)
        else: # (midlowGamma > midhighGamma)
            if (midhighGamma < highGamma):
                return self.minimizeGammaHelper(
                    time, midlowPrice, midlowGamma, highPrice, highGamma)
            else: # (midhighGamma >= highGamma)
                return self.minimizeGammaHelper(
                    time, midhighPrice, midhighGamma, highPrice, highGamma)
        

    def waitingFunction(self, ptClass, d, t):
        return d / (self.ptConst[ptClass] * (t+1)**self.ptIndex[ptClass])

    def findLamda(self, D):
        predictPeriod = self.N
        ptClassCount = self.M
        for ptClass in range(ptClassCount):
            p = self.ptIndex[ptClass]
            lamda = 0
            for i in range(predictPeriod):
                d = D[i]
                lamda += d/((i+1)**p)
            self.ptConst[ptClass] = lamda

    def calculateAik(self, i, k):
        predictPeriod = self.N
        ptClassCount = self.M
        sigma = 0
        mu = self.ptRitio[i]
        d = self.discount[k]
        t = (k - i) % predictPeriod
        for j in range(ptClassCount):
            sigma += mu[j] * self.waitingFunction(j, d, t)
        return sigma * self.TIP[i]

    def networkcostFunction(self, traffic):
        if (traffic <= 0):
            return 0
        increaseRate = 0.0001
        noTrafficBase = 20000
        return noTrafficBase * (math.exp(increaseRate * traffic) - 1)

    

        
