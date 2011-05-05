#!/usr/bin/env python
import libxml2
import sys
import os

def readLocFile(locFilePath):
    locFile = libxml2.parseFile(locFilePath);
    xpath = locFile.xpathNewContext();
    waypoints = xpath.xpathEval("//loc/waypoint");

    for waypoint in waypoints:
        print waypoint;
    
sys.argv = ['route-distance.py', 'testingFiles/robbos.loc'];

if not os.path.exists(sys.argv[1]):
    sys.exit('File specified not valid');

locFilePath = sys.argv[1];

if __name__ == "__main__":
    readLocFile(locFilePath);


