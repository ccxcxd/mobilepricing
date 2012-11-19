import Cell

class BaseStation( Cell.Cell ):
    def __init__( self, center, radius, id ):
        Cell.Cell.__init__( self, center, radius )
        self.id = id
