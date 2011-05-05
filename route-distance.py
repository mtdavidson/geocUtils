#!/usr/bin/env python
import libxml2
import sys
import os

workingWaypointList = {};
visitedWaypoints = [];

import math

# http://www.johndcook.com/python_longitude_latitude.html
def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
	
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
	
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
	
    # Compute spherical distance from spherical coordinates.
	
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

def readLocFile(locFilePath):
    waypointList = {};
    locFile = libxml2.parseFile(locFilePath);
    xpath = locFile.xpathNewContext();
    waypoints = xpath.xpathEval("//loc/waypoint");

    for waypoint in waypoints:
        gcCode = waypoint.xpathEval('name/@id')[0].content;
        lat = waypoint.xpathEval('coord/@lat')[0].content;
        lon = waypoint.xpathEval('coord/@lon')[0].content;
        waypointList[gcCode] = {
            'lat': lat,
            'lon': lon
        };
        
    return waypointList;

def getNextNotVisited(waypoint, workingWaypointList):
    visitedWaypoints.append(waypoint[0]);

    if (len(workingWaypointList) > 0):
        #TODO: Actually calculate the closest waypoint.
        item = workingWaypointList.popitem();
        getNextNotVisited(item, workingWaypointList);

def getRoute(waypoints):
    workingWaypointList = waypoints.copy();
    
    print 'Getting Route';
    item = workingWaypointList.popitem();
    getNextNotVisited(item, workingWaypointList);

def calcDistance(visitedWaypoints, waypoints):
    wl = len(visitedWaypoints);
    for x in range(wl):
        currentWaypoint = waypoints.get(visitedWaypoints[x]);
        print currentWaypoint;
        for z in range(wl - x):
            workingWaypoint = waypoints.get(visitedWaypoints[z]);
            print " - " + visitedWaypoints[z] + ": " + \
                  str(workingWaypoint) + \
                  str(distance_on_unit_sphere(float(currentWaypoint['lat']), float(currentWaypoint['lon']), float(workingWaypoint['lat']), float(workingWaypoint['lon'])));
    
sys.argv = ['route-distance.py', 'testingFiles/robbos.loc'];

if not os.path.exists(sys.argv[1]):
    sys.exit('File specified not valid');

locFilePath = sys.argv[1];

if __name__ == "__main__":
    waypoints = readLocFile(locFilePath);
    print waypoints;
    print len(waypoints);

    getRoute(waypoints);
    calcDistance(visitedWaypoints, waypoints);
