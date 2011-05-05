#!/usr/bin/env python
import libxml2
import sys
import os

def readLocFile(locFilePath):
    waypointList = {};
    locFile = libxml2.parseFile(locFilePath);
    xpath = locFile.xpathNewContext();
    waypoints = xpath.xpathEval("//loc/waypoint");

    for waypoint in waypoints:
        gcCode = waypoint.xpathEval('name/@id')[0].content;
        lat = waypoint.xpathEval('coord/@lat')[0].content;
        lon = waypoint.xpathEval('coord/@lon')[0].content;
        waypointList[gcCode] = [lat,lon];
        
    return waypointList;
    
sys.argv = ['route-distance.py', 'testingFiles/robbos.loc'];

if not os.path.exists(sys.argv[1]):
    sys.exit('File specified not valid');

locFilePath = sys.argv[1];

if __name__ == "__main__":
    waypoints = readLocFile(locFilePath);
