#!/usr/bin/env -S python3 -u
"""
This is heavily based on the NtripPerlClient program written by BKG.
Then heavily based on a unavco original.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""

import socket
import sys
import datetime
import base64
import time
import threading
#import ssl
from optparse import OptionParser

import serial
from pynmeagps import NMEAReader

version=0.2
useragent="NTRIP JCMBsoftPythonClient/%.1f" % version

# reconnect parameter (fixed values):
factor=2 # How much the sleep time increases with each failed attempt
maxReconnect=1
maxReconnectTime=1200
sleepTime=1 # So the first one is 1 second




class NtripClient(object):
    def __init__(self,
                 buffer=50,
                 user="",
                 out=sys.stdout,
                 port=2101,
                 caster="",
                 mountpoint="",
                 host=False,
                 lat=46,
                 lon=122,
                 height=1212,
                 ssl=False,
                 verbose=False,
                 UDP_Port=None,
                 V2=False,
                 headerFile=sys.stderr,
                 headerOutput=False,
                 maxConnectTime=0
                 ):
        self.buffer=buffer
        self.user=base64.b64encode(bytes(user,'utf-8')).decode("utf-8")
#        print(self.user)
        self.out=out
        self.port=port
        self.caster=caster
        self.mountpoint=mountpoint
        self.setPosition(lat, lon)
        self.height=height
        self.verbose=verbose
        self.ssl=ssl
        self.host=host
        self.UDP_Port=UDP_Port
        self.V2=V2
        self.headerFile=headerFile
        self.headerOutput=headerOutput
        self.maxConnectTime=maxConnectTime
        self.socket=None
        self.stream = serial.Serial('/dev/ttyS0', 115200, timeout=3)
        self.nmr = NMEAReader(self.stream)
        

        if UDP_Port:
            self.UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.UDP_socket.bind(('', 0))
            self.UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        else:
            self.UDP_socket=None


    def setPosition(self, lat, lon):
        self.flagN="N"
        self.flagE="E"
        if lon>180:
            lon=(lon-360)*-1
            self.flagE="W"
        elif (lon<0 and lon>= -180):
            lon=lon*-1
            self.flagE="W"
        elif lon<-180:
            lon=lon+360
            self.flagE="E"
        else:
            self.lon=lon
        if lat<0:
            lat=lat*-1
            self.flagN="S"
        self.lonDeg=int(lon)
        self.latDeg=int(lat)
        self.lonMin=(lon-self.lonDeg)*60
        self.latMin=(lat-self.latDeg)*60

    def getMountPointBytes(self):
        mountPointString = "GET %s HTTP/1.1\r\nUser-Agent: %s\r\nAuthorization: Basic %s\r\n" % (self.mountpoint, useragent, self.user)
#        mountPointString = "GET %s HTTP/1.1\r\nUser-Agent: %s\r\n" % (self.mountpoint, useragent)
        if self.host or self.V2:
           hostString = "Host: %s:%i\r\n" % (self.caster,self.port)
           mountPointString+=hostString
        if self.V2:
           mountPointString+="Ntrip-Version: Ntrip/2.0\r\n"
        mountPointString+="\r\n"
        if self.verbose:
           print (mountPointString)
        return bytes(mountPointString,'ascii')

    def getGGABytes(self):
        while True:
            (raw_data, parsed_data) = self.nmr.read()
            if bytes("GNGGA",'ascii') in raw_data :
                 # print(parsed_data)
                 return raw_data

    def readData(self):
        reconnectTry=1
        sleepTime=1
        reconnectTime=0
        if self.maxConnectTime > 0 :
            EndConnect=datetime.timedelta(seconds=maxConnectTime)
        try:
            while reconnectTry<=maxReconnect:
                found_header=False
                if self.verbose:
                    sys.stderr.write('Connection {0} of {1}\n'.format(reconnectTry,maxReconnect))

                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if self.ssl:
                    self.socket=ssl.wrap_socket(self.socket)

                error_indicator = self.socket.connect_ex((self.caster, self.port))
                if error_indicator==0:
                    sleepTime = 1
                    connectTime=datetime.datetime.now()

                    self.socket.settimeout(10)
                    self.socket.sendall(self.getMountPointBytes())
                    while not found_header:
                        casterResponse=self.socket.recv(4096) #All the data
                        # print(casterResponse)
                        header_lines = casterResponse.decode('utf-8').split("\r\n")
                        
# header_lines empty, request fail,exit while loop
                        for line in header_lines:
                            if line=="":
                                if not found_header:
                                    found_header=True
                                    if self.verbose:
                                        sys.stderr.write("End Of Header"+"\n")
                            else:
                                if self.verbose:
                                    sys.stderr.write("Header: " + line+"\n")
                            if self.headerOutput:
                                self.headerFile.write(line+"\n")



#header_lines has content
                        for line in header_lines:
                            if line.find("SOURCETABLE")>=0:
                                sys.stderr.write("Mount point does not exist")
                                sys.exit(1)
                            elif line.find("401 Unauthorized")>=0:
                                sys.stderr.write("Unauthorized request\n")
                                sys.exit(1)
                            elif line.find("404 Not Found")>=0:
                                sys.stderr.write("Mount Point does not exist\n")
                                sys.exit(2)
                            elif line.find("ICY 200 OK")>=0:
                                #Request was valid
                                self.socket.sendall(self.getGGABytes())
                            elif line.find("HTTP/1.0 200 OK")>=0:
                                #Request was valid
                                self.socket.sendall(self.getGGABytes())
                            elif line.find("HTTP/1.1 200 OK")>=0:
                                #Request was valid
                                self.socket.sendall(self.getGGABytes())



                    data = "Initial data"
                    while data:
                        try:
                            data=self.socket.recv(self.buffer)
                            # self.out.buffer.write(data)
                            self.stream.write(data)
                            (raw_data, parsed_data) = self.nmr.read()
                            if bytes("GNGGA",'ascii') in raw_data :
                                return (raw_data)

                            if self.UDP_socket:
                                self.UDP_socket.sendto(data, ('<broadcast>', self.UDP_Port))
#                            print datetime.datetime.now()-connectTime
                            if maxConnectTime :
                                if datetime.datetime.now() > connectTime+EndConnect:
                                    if self.verbose:
                                        sys.stderr.write("Connection Timed exceeded\n")
                                    sys.exit(0)
#                            self.socket.sendall(self.getGGAString())



                        except socket.timeout:
                            if self.verbose:
                                sys.stderr.write('Connection TimedOut\n')
                            data=False
                        except socket.error:
                            if self.verbose:
                                sys.stderr.write('Connection Error\n')
                            data=False

                    if self.verbose:
                        sys.stderr.write('Closing Connection\n')
                    self.socket.close()
                    self.socket=None

                    if reconnectTry < maxReconnect :
                        sys.stderr.write( "%s No Connection to NtripCaster.  Trying again in %i seconds\n" % (datetime.datetime.now(), sleepTime))
                        time.sleep(sleepTime)
                        sleepTime *= factor

                        if sleepTime>maxReconnectTime:
                            sleepTime=maxReconnectTime
                    else:
                        sys.exit(1)


                    reconnectTry += 1
                else:
                    self.socket=None
                    if self.verbose:
                        print ("Error indicator: ", error_indicator)

                    if reconnectTry < maxReconnect :
                        sys.stderr.write( "%s No Connection to NtripCaster.  Trying again in %i seconds\n" % (datetime.datetime.now(), sleepTime))
                        time.sleep(sleepTime)
                        sleepTime *= factor
                        if sleepTime>maxReconnectTime:
                            sleepTime=maxReconnectTime
                    reconnectTry += 1

        except KeyboardInterrupt:
            if self.socket:
                self.socket.close()
            self.stream.close()
            sys.exit()
            
def RTK_Init():
    ntripArgs = {}
    ntripArgs['user'] = "xxxxx:xxxxxx"
    ntripArgs['caster'] = "192.148.213.42"
    ntripArgs['port'] = 2101
    ntripArgs['mountpoint'] = VRS3M
    ntripArgs['ssl'] = False
    n = NtripClient(**ntripArgs)
    
    x = threading.Thread(target=thread_function(readData()), args=
        n.readData()
    finally:
        if fileOutput:
            f.close()
        if options.headerFile:
            h.close()
