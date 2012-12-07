import BaseStation
import Client
import Tkinter
import time

SLEEPTIME = 0.01

MapWidth = 1000
MapHeight = 500
ZoomIn = 50
NearbyRange = 15
SlotPerUpdate = 12  # number of slots per price update
UpdatePerDay = 4    # N, number of update until loop back
PtClassCount = 3    # M, number of patient index class

class CelluarSystem:
    def __init__ ( self, stationsInfo, clientsInfo, handler ):
        
        # stations initialization
        self.stations = {}
        for stationInfo in stationsInfo:
            capacity = [50000] * UpdatePerDay
            self.stations[ stationInfo[ 'id' ] ] = BaseStation.BaseStation( self, stationInfo[ 'center' ], stationInfo[ 'radius' ], stationInfo[ 'id' ], capacity )

        self.calculateNearbyBs( NearbyRange )

        # clients initialization
        self.clients = {}
        for clientInfo in clientsInfo:
            self.clients [ clientInfo[ 'id' ] ] = Client.Client( clientInfo[ 'id' ], clientInfo[ 'startPosition' ], clientInfo[ 'speed' ] )

        # map initialization
        self.tkHandler = handler
        self.map = Tkinter.Canvas( self.tkHandler, width=MapWidth, height=MapHeight )
        self.map.pack()
        self.showBaseStations()

        self.timer = -1
        while( 1 ):
            self.mainProcess()

    def showBaseStations( self ):
        for station in self.stations.itervalues():
            x = station.getXPosition() * ZoomIn
            y = station.getYPosition() * ZoomIn
            radius = station.getRadius() * ZoomIn
            self.map.create_oval( x + MapWidth/2 - radius, y + MapHeight/2 - radius, x + MapWidth/2 + radius, y + MapHeight/2 + radius )
        self.tkHandler.update()

    def drawLine( self, input ):
        x1 = input[0][0] * ZoomIn + MapWidth/2
        y1 = input[0][1] * ZoomIn + MapHeight/2
        x2 = input[1][0] * ZoomIn + MapWidth/2
        y2 = input[1][1] * ZoomIn + MapHeight/2
        self.map.create_line( x1, y1, x2, y2, fill="red", dash=( 4, 4 ) )
        self.tkHandler.update()

    def mainProcess( self ):
        time.sleep( SLEEPTIME )
        self.timer = self.timer + 1
        print "\n*****Timer = "+ str(self.timer) + "*****"
        
        if self.timer % SlotPerUpdate == 0 and self.timer != 0:
            for station in self.stations.itervalues():
                station.updatePrice()
                if self.timer == (SlotPerUpdate * UpdatePerDay * 5):
                    station.changeMode("TDPTrain")
        
        for clientId in self.clients.keys():
            result = self.clients[ clientId ].positionUpdate( self.timer )
            self.drawLine( result )
            position = self.clients[ clientId ].getPosition()
            baseStationId = self.allocateBaseStation( position )
            if baseStationId is None:
                del( self.clients[ clientId ] )
                continue
            #print "Client " + self.clients[ clientId ].id + " is connected to Base Station " + baseStationId
            self.clients[ clientId ].intervalCommunication( self.stations[ baseStationId ], self.timer )
        
    def getPtClassCount( self ):
        return PtClassCount
        
    def getUpdatePerDay( self ):
        return UpdatePerDay
        
    def getSlotPerUpdate( self ):
        return SlotPerUpdate
        
    def getCurrentUpdateIndex( self ):
        return (self.timer / SlotPerUpdate) % UpdatePerDay

    def allocateBaseStation( self, position ):
        # find the cell the client is in range
        potentialBS = {}
        for station in self.stations.itervalues():
            if station.isInRange( position ):
                potentialBS[ station.id ] = station.distanceFromCenter( position )

        # chose the closest BS
        minDist = None
        bs = None
        for station in potentialBS.iteritems():
            if minDist is None:
                minDist = station[1]
                bs = station[0]
            else:
                if station[1] < minDist:
                    minDist = station[1]
                    bs = station[0]

        return bs

    def calculateNearbyBs( self, radius ):
        for station1 in self.stations.itervalues():
            station1.clearNearbyBs()
            for station2 in self.stations.itervalues():
                if cmp( station1.id, station2.id ) == 0:
                    continue
                if station1.distanceFromCenter( station2.center ) < radius:
                    station1.addNearbyBs( station2 )

        
