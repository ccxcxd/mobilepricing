import random

class ClientGenerator( object ):
    def __init__ ( self, staticNum, straightNum, randomNum, positionRange, speedRange ):
        self.static = staticNum
        self.straight = straightNum
        self.random = randomNum
        self.positionRange = positionRange # [ max x, max y, min x, min y ]
        self.speedRange = speedRange # [ max speed, min speed ]
        #random.seed()

    def generateRandomPosition( self ):
        x = random.uniform( self.positionRange[2], self.positionRange[0] )
        y = random.uniform( self.positionRange[3], self.positionRange[1] )
        return [ x, y ]
    
    def generateDefaultClient( self, id, startPosition, speed ):
        # put info into format
        client = { 'id': id, 'startPosition': startPosition, 'speed': speed }
        return client

    def generateSingleStatic( self, id, startPosition ):
        # create a static client
        client = self.generateDefaultClient( id, startPosition, [ [ 0, 0 ] ] )
        return client

    def generateStatic( self, idPrefix ):
        # create all static clients
        self.staticClients = []
        for i in xrange( self.static ):
            id = idPrefix + str( i )
            position = self.generateRandomPosition()
            self.staticClients.append( self.generateSingleStatic( id, position ) )
        return self.staticClients

    def generateRandomSpeed( self ):
        speed = random.uniform( self.speedRange[0], self.speedRange[1] )
        return speed

    def generateSingleStraight( self, id, startPosition ):
        # create a straight client
        client = self.generateDefaultClient( id, startPosition, [ [ self.generateRandomSpeed(), self.generateRandomSpeed() ] ] )
        return client

    def generateStraight( self, idPrefix ):
        # create all straight clients
        self.straightClients = []
        for i in xrange( self.straight ):
            id = idPrefix + str( i )
            position = self.generateRandomPosition()
            self.straightClients.append( self.generateSingleStraight( id, position ) )
        return self.straightClients

    def generateRandomSpeedSequence( self, sequenceLength ):
        speed = []
        for i in xrange( sequenceLength ):
            speed.append( [ self.generateRandomSpeed(), self.generateRandomSpeed() ] )
        return speed

    def generateSingleRandom( self, id, startPosition ):
        # create a single random client
        speed = self.generateRandomSpeedSequence( 100 )
        client = self.generateDefaultClient( id, startPosition, speed )
        return client

    def generateRandom( self, idPrefix ):
        # create all random clients
        self.randomClients = []
        for i in xrange( self.random ):
            id = idPrefix + str( i )
            position = self.generateRandomPosition()
            self.randomClients.append( self.generateSingleRandom( id, position ) )
        return self.randomClients

    def generateClient( self ):
        # create all clients
        self.clients = []
        self.clients.extend( self.generateStatic( 'static' ) )
        self.clients.extend( self.generateStraight( 'straight' ) )
        self.clients.extend( self.generateRandom( 'random' ) )
        return self.clients
            
            

    
    
