import Cell

class BaseStation( Cell.Cell ):
    def __init__( self, center, radius, id ):
        Cell.Cell.__init__( self, center, radius )
        self.id = id
        self.nearbyBs = {}
        self.price = 0
        self.traffic = 0

    def addNearbyBs( self, baseStation ):
        self.nearbyBs[ baseStation.id ] = baseStation

    def clearNearbyBs( self ):
        self.nearbyBs.clear()

    def getPrice(self):
        return self.price

    def updatePrice(self):
        self.price = self.calculatePrice()
        self.traffic = 0
        print "Price of " + self.id + ": " + str( self.price )

    def calculatePrice(self):
        # need to beimplemented
        return self.traffic

    def recordTraffic(self, traffic):
        self.traffic += traffic
        print "Traffic of " + self.id + ": " + str( self.traffic )
        
