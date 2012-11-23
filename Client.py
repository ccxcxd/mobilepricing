import random

class Client( object ):
    def __init__( self, id, startPosition, speed ):
        self.id = id
        self.position = startPosition # 1 = 1 km
        self.speed = speed # 1 = 1 km/h
        self.previousPosition = None
        random.seed()

    def positionUpdate( self, i ):
        # interval is 5 min
        divide = 12.0
        self.previousPosition = self.position[:]
        speedLength = len( self.speed )
        i = i % speedLength # if not long enough or use constant speed
        self.position = [ self.position[0] + self.speed[i][0] / divide,
                          self.position[1] + self.speed[i][1] / divide
                          ]
        return [ self.previousPosition, self.position ]

    def getPosition( self ):
        return self.position

    def predictBs( self, baseStation, slot ):
        predictSpeed = self.predictSpeed( slot )
        potentialBs = self.predictPotentialBs( baseStation, predictSpeed ) # delete some impossible choice to decrease computation overhead
        predict = self.traversalPredictBs( predictSpeed, potentialBs )
        if predict[0] is None:
                print "No new BS within 1 hour"
        else:
                print "Predict to reach " + predict[0] + " in " + str( predict[1] * 5 ) + "mins"
        return predict

    def predictSpeed( self, slot ):
        weight = [ 0.6, 0.3, 0.1 ] # choose randomly... only the sum need to be 1
        predictSpeed = [ 0, 0 ]
        speedLength = len( self.speed )
        for i in xrange( len( weight ) ):
            if i > slot: # no previous speed when start
                pass
            predictSpeed = [ predictSpeed[0] + self.speed[ ( slot - i ) % speedLength ][0] * weight[ i ], predictSpeed[1] + self.speed[ ( slot - i ) % speedLength ][1] * weight[ i ] ]

        return predictSpeed

    def predictPotentialBs( self, baseStation, predictSpeed ):
        potentialBs = {}
        for station in baseStation.nearbyBs.iteritems():
            if ( station[1].getXPosition() - baseStation.getXPosition() ) * predictSpeed[0] < 0:
                continue
            if ( station[1].getYPosition() - baseStation.getYPosition() ) * predictSpeed[1] < 0:
                continue
            potentialBs[ station[0] ] = station[1]

        return potentialBs

    def traversalPredictBs( self, predictSpeed, potentialBs ):
        maxSlot = 12 # only care for the prediction within 1 hour ( 1 slot = 5 min )
        start = self.position[:] # avoid using same data
        for i in xrange( maxSlot ):
            start[0] = start[0] + predictSpeed[0] / 12
            start[1] = start[1] + predictSpeed[1] / 12
            minDistance = None
            nextBs = None
            for station in potentialBs.iteritems():
                if station[1].isInRange( start ):
                    distance = station[1].distanceFromCenter( start )
                    if ( minDistance is None ) or ( distance < minDistance ):
                        minDistance = distance
                        nextBs = station[0]
            if nextBs is not None:
                break
        return [ nextBs, i + 1 ]

    def generateTraffic(self):
        # may not generate traffic for every interval
        if (random.random() < 0.3):
            return random.randint(1, 20)   # some random number
        else:
            return 0

    def intervalCommunication( self, baseStation, slot ):
        self.station = baseStation
        
        predict = self.predictBs( baseStation, slot )
        traffic = self.generateTraffic()
        self.station.recordTraffic(traffic)
        
        
                
    
