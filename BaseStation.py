import Cell

class BaseStation( Cell.Cell ):
    def __init__( self, center, radius, id ):
        Cell.Cell.__init__( self, center, radius )
        self.id = id
        self.nearbyBs = {}

    def addNearbyBs( self, baseStation ):
        self.nearbyBs[ baseStation.id ] = baseStation

    def clearNearbyBs( self ):
        self.nearbyBs.clear()
