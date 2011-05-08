#!/usr/bin/env python
import libxml2
import sys
import os

workingWaypointList = {};
visitedWaypoints = {};

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
            'lat': float(lat),
            'lon': float(lon)
        };
        
    return waypointList;

def getNextNotVisited(waypoint, workingWaypointList):
    #visitedWaypoints[waypoint[0]] = {};

    closestPoint = [];
    if (len(workingWaypointList) > 0):
        #TODO: Actually calculate the closest waypoint.
        for k, v in workingWaypointList.iteritems():
            distance = distance_on_unit_sphere( 
                waypoint[1]['lat'], 
                waypoint[1]['lon'], 
                v['lat'],
                v['lon']
                );
            if len(closestPoint) == 0:
                closestPoint = [k, distance];
            else:
                if (distance < closestPoint[1]):
                    closestPoint = [k, distance];

        item = [closestPoint[0], workingWaypointList.pop(closestPoint[0])];
        visitedWaypoints[closestPoint[0]] = {'distance': distance};
        #print visitedWaypoints[closestPoint[0]];
 
        getNextNotVisited(item, workingWaypointList);

def getRoute(waypoints):
    workingWaypointList = waypoints.copy();
    
    print 'Getting Route';
    item = workingWaypointList.popitem();
    getNextNotVisited(item, workingWaypointList);
    print "Distance: ", (sum([i['distance'] for i in visitedWaypoints.values()]) * 3960);

sys.argv = ['route-distance.py', 'testingFiles/robbos.loc'];

if not os.path.exists(sys.argv[1]):
    sys.exit('File specified not valid');

locFilePath = sys.argv[1];

if __name__ == "__main__":
    waypoints = readLocFile(locFilePath);

    getRoute(waypoints);
    print 'Finish';
