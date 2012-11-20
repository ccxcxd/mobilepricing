import BaseStation
import Client
import Tkinter
import time

MapWidth = 1000
MapHeight = 500
ZoomIn = 50
NearbyRange = 10

class CelluarSystem:
    def __init__ ( self, stationsInfo, clientsInfo, handler ):
        # stations initialization
        self.stations = {}
        for stationInfo in stationsInfo:
            self.stations[ stationInfo[ 'id' ] ] = BaseStation.BaseStation( stationInfo[ 'center' ], stationInfo[ 'radius' ], stationInfo[ 'id' ] )

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
        time.sleep( 0.5 )
        self.timer = self.timer + 1
        for client in self.clients.itervalues():
            result = client.intervalUpdate( self.timer )
            self.drawLine( result )
            position = client.getPosition()
            baseStationId = self.allocateBaseStation( position )
            print "Client " + client.id + " is connected to Base Station " + baseStationId

    def allocateBaseStation( self, position ):
        # find the cell the client is in range
        potentialBS = {}
        for station in self.stations.itervalues():
            if station.isInRange( position ):
                potentialBS[ station.id ] = station.distanceFromCenter( position )

        # chose the closest BS
        minDist = None
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
