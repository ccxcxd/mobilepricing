import CelluarSystem
import ClientGenerator
import Tkinter


stationsInfo = [ { 'center': [ 0, 0 ], 'radius': 5, 'id': 'BS1' },
                 { 'center': [ 5, 5 ], 'radius': 5, 'id': 'BS2' },
                 { 'center': [ 5, -5 ], 'radius': 5, 'id': 'BS3' },
                 { 'center': [ -5, 5 ], 'radius': 5, 'id': 'BS4' },
                 { 'center': [ -5, -5 ], 'radius': 5, 'id': 'BS5' }
            ]

handler = Tkinter.Tk() # handler for the display

clientGenerator = ClientGenerator.ClientGenerator( 60, 20, 20, [ 5, 5, -5, -5 ], [ 10, -10 ] )
clientsInfo = clientGenerator.generateClient()


#clientsInfo = [ { 'id': 'Tom', 'startPosition': [ -5, -5], 'speed': [ [ 5, 5 ] ] }
#
#                ]

celluarSystem = CelluarSystem.CelluarSystem( stationsInfo, clientsInfo, handler )

Tkinter.mainloop() # starting the display loop
