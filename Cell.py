import math

class Cell( object ):
    def __init__( self, center, radius ):
        # 1 == 1 km
        self.center = center
        self.xPosition = center[0]
        self.yPosition = center[1]
        self.radius = radius

    def getCenter( self ):
        return self.center

    def getXPosition( self ):
        return self.xPosition

    def getYPosition( self ):
        return self.yPosition

    def getRadius( self ):
        return self.radius

    def distanceFromCenter( self, position ):
        x = self.xPosition - position[0]
        y = self.yPosition - position[1]
        distance = math.pow( x, 2 ) + math.pow( y, 2 )
        distance = math.sqrt( distance )
        return distance

    def isInRange( self, position ):
        distance = self.distanceFromCenter( position )
        if distance < self.radius:
            return True
        else:
            return False
