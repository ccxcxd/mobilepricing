class Client( object ):
    def __init__( self, id, startPosition, speed ):
        self.id = id
        self.position = startPosition # 1 = 1 km
        self.speed = speed # 1 = 1 km/h
        self.previousPosition = None

    def intervalUpdate( self, i ):
        # interval is 5 min
        divide = 12.0
        self.previousPosition = self.position
        speedLength = len( self.speed )
        i = i % speedLength # if not long enough or use constant speed
        self.position = [ self.position[0] + self.speed[i][0] / divide,
                          self.position[1] + self.speed[i][1] / divide
                          ]
        return [ self.previousPosition, self.position ]

    def getPosition( self ):
        return self.position
    
