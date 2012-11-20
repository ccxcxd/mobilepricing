import CelluarSystem
import Tkinter

stationsInfo = [ { 'center': [ 0, 0 ], 'radius': 5, 'id': 'BS1' },
                 { 'center': [ 5, 5 ], 'radius': 5, 'id': 'BS2' },
                 { 'center': [ 5, -5 ], 'radius': 5, 'id': 'BS3' },
                 { 'center': [ -5, 5 ], 'radius': 5, 'id': 'BS4' },
                 { 'center': [ -5, -5 ], 'radius': 5, 'id': 'BS5' }
            ]

handler = Tkinter.Tk() # handler for the display

clientsInfo = [ { 'id': 'Tom', 'startPosition': [ -5, -5], 'speed': [ [ 5, 5 ] ] }

                ]

celluarSystem = CelluarSystem.CelluarSystem( stationsInfo, clientsInfo, handler )

#Tkinter.mainloop() # starting the display loop
