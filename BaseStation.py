import Cell

CollectionModes = ["TIP","TDPTrain","TDP"]
predictPeriod = 4       # N
ptClassCount = 3        # M

class BaseStation( Cell.Cell ):
    def __init__( self, center, radius, id ):
        Cell.Cell.__init__( self, center, radius )
        self.id = id
        self.nearbyBs = {}
        self.price = 0
        self.baseline = 10
        self.capacity = []  # N*1 network capacity
        self.discount = []  # N*1 discount
        self.TIP = []       # N*1 base traffic
        self.TDP = []       # N*1 TDP traffic
        self.ptIndex = []   # M*1 pt index
        self.ptConst = [None]*ptClassCount   # M*1 lamda
        self.ptRitio = []   # N*M ptclass fraction in a period
        self.mode = "TIP"

    def changeMode(self, newmode)
        this.mode = newmode

    def addNearbyBs( self, baseStation ):
        self.nearbyBs[ baseStation.id ] = baseStation

    def clearNearbyBs( self ):
        self.nearbyBs.clear()

    def updatePrice(self):
        self.price = self.calculatePrice()
        self.traffic = 0
        print "Price of " + self.id + ": " + str( self.price )

    def calculatePrice(self):
        # need to beimplemented
        return [ 5 ]

    def recordTraffic(self, traffic, slotnumber):
        if (mode == "TIP"):
            self.TIP[slotnumber] = traffic
        elif (mode == "TDPTrain"):
            self.TDP[slotnumber] = traffic
        else:
            self.TDP[slotnumber] = traffic
            
        self.traffic += traffic
        print "Traffic of " + self.id + ": " + str( self.traffic )

    def getPrice( self, index ):
        #may need to improve
        return self.price[ index ]

    def calculateGamma(self):
        gamma1 = 0
        gamma2 = 0
        for i in range(predictPeriod):
            sigmaAik = 0
            mu = self.ptRitio[i]
            for k in range(predictPeriod):
                if i == k:
                    continue
                sigmaAik += calculateAik(i,k)
            sigmaDeleyIn = 0
            for j in range(ptClassCount):
                sigmaWaiting = 0
                for k in range(predictPeriod):
                    if i == k:
                        continue
                    d = self.discount[k]
                    t = (k - i) % predictPeriod
                    sigmaWaiting += waitingFunction(j, d, t)
                sigmaDeleyIn += mu[j] * sigmaWaiting
            gamma1 += networkcostFunction(self.TIP[i] * (1 - sigmaDeleyIn)
                                          + sigmaAik - capacity[i])
            gamma2 += self.discount[i] + sigmaAik
        return gamma1 + gamma2

    def minimizeGamma(self, time):
        lowPrice = 0
        highPrice = self.baseline
        self.discount[time] = self.baseline - lowPrice
        lowGamma = this.calculateGamma()
        self.discount[time] = self.baseline - highPrice
        highGamma = this.calculateGamma()                
        return this.minimizeGammaHelper(
            time, lowPrice, lowGamma, highPrice, highGamma)
    
    def minimizeGammaHelper(self, time,
                            lowPrice, lowGamma, highPrice, highGamma):
        delta = 0.01
        roundDigit = 2
        if (highPrice - lowPrice) < delta:
            return round((highPrice + lowPrice)/2, roundDigit)
        midlowPrice = (highPrice - lowPrice) / 3 + lowPrice
        self.discount[time] = self.baseline - midlowPrice
        midlowGamma = this.calculateGamma()
        midhighPrice = highPrice - (highPrice - lowPrice) / 3
        self.discount[time] = self.baseline - midhighPrice
        midhighGamma = this.calculateGamma()
        if (midlowGamma == midhighGamma):
            # must be the case: lowGamma > midlowGamma = midhighGamma < high
            return this.minimizeGammaHelper(
                time, midlowPrice, midlowGamma, midhighPrice, midhighGamma)
        elif (midlowGamma < midhighGamma):
            if (lowGamma > midlowGamma):
                return this.minimizeGammaHelper(
                    time, lowPrice, lowGamma, midhighPrice, midhighGamma)
            else: # (lowGamma <= midlowGamma)
                return this.minimizeGammaHelper(
                    time, lowPrice, lowGamma, midlowPrice, midlowGamma)
        else: # (midlowGamma > midhighGamma)
            if (midhighGamma < highGamma):
                return this.minimizeGammaHelper(
                    time, midlowPrice, midlowGamma, highPrice, highGamma)
            else: # (midhighGamma >= highGamma)
                return this.minimizeGammaHelper(
                    time, midhighPrice, midhighGamma, highPrice, highGamma)
        

    def waitingFunction(self, ptClass, d, t):
        return d / (self.ptConst[ptClass] * (t+1)**self.ptIndex[ptClass])

    def findLamda(self, D):
        for ptClass in ptClassCount:
            p = ptIndex[ptClass]
            lamda = 0
            for i in range(predictPeriod):
                d = D[i]
                lamda += d/((i+1)**p)
            self.ptConst[ptClass] = lamda
        return

    def calculateAik(self, i, k):
        sigma = 0
        mu = self.ptRitio[i]
        d = self.discount[k]
        t = (k - i) % predictPeriod
        for j in range(ptClassCount):
            sigma += mu[j] * waitingFunction(j, d, t)
        return sigma * self.TIP[i]

    def networkcostFunction(traffic):
        increaseRate = 1
        noTrafficBase = 1
        return noTrafficBase * exp(increaseRate * traffic)

    

        
