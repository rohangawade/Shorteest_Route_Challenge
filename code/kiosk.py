# -*- coding: utf-8 -*-
"""
@author: rohan
"""
import numpy as np
import pandas as pd


def haversinedistance(lat1,lon1,lat2,lon2):
    """
    This function calculates the distance between two points given by their latitude and longitude
    Paramenters:
    lat1: latitude of the first location
    lon1: longitude of the first location
    lat2: latitude of the second location
    lon2: longitude of the second location
    Returns the distance in kilometers.
    """
    #Earths Radius in km
    radius = 6371 
    #Converting the latitude and longitude degress into radians.
    rlat1 = np.radians(lat1)
    rlat2 = np.radians(lat2)
    rlon1 = np.radians(lon1)
    rlon2 = np.radians(lon2)
    
    #Finding the differences between the two latitudes and longitudes
    dlat = rlat2-rlat1
    dlon = rlon2-rlon1
    
    #Haversine formula to calculate the distance.
    a = ((np.sin(dlat/2) ** 2) +
        (np.cos(rlat1) * np.cos(rlat2) * 
        (np.sin(dlon/2) **2)))
    c = 2*np.arcsin(np.sqrt(a))
    distance = radius * c

    return distance

   
    
def getLatLong(df_latlon,name):
    """
    This function returns the Latitude and Longitude with respect to the name of the Kiosk from the dataframe.
    Parameters:
        df_latlon: The dataframe containing the name, latitude and longitude of all Kiosk Co-ordinates
        name:  The name of the kiosk
    Returns the latitude and longitude.
    """
    dfLL = df_latlon[df_latlon.name == name]
    lat = float(dfLL['latitude (N)'])
    lon = float(dfLL['longitude (N)'])
    return lat,lon
    
    
    
def calculateDistance(route,distarray):
    """
    The method calculates the distance of the route using the distance matrix
    Parameters:
        route: List of the index positions of the kiosk centers in the route
        distarray: 2D distance matrix
    Returns total distance 
    """
    total_dist = 0
    for i in range(0,len(route)-1):
        total_dist = total_dist + distarray[route[i]][route[i+1]]
    return total_dist

    

def findShortestDist(vDist,argpos,visitedList):
    """
    This method is used by shortestRoute_Greedy method to return the kiosk center(node) with the shortest distance.
    If the node is already in the visited list we fnd the next minimum distance.
    Parameters:
        vDist: array of distances corresponding to the current Kiosk center(node)
        argpos: Initial value passed to the function is one. If the node is in the visitedList, we increament
                argpos to find the next minimum distance.
        visitedList: List of kiosk centers(nodes) visited.
    Returns the shortest node and the distance from current node.
    """
    #print("visited array",vDist)
    shortNode = np.argsort(vDist)[argpos]
    #print("Short Node ",shortNode,"Current visitedset ",visitedList)
    # Check if the next node to be traversed is in the visitedList. If yes find the next minimum center distance.
    if shortNode in visitedList:
        #print("node in list")
        shortNode,sndist = findShortestDist(vDist,argpos+1,visitedList) 
    sndist = vDist[shortNode]

    return shortNode,sndist
    
    
    
def shortestRoute_Greedy(distarray,listind):
    """
    This method finds the next minimum distance Kiosk center from the current center and follows the greedy approach
    to create the path.
    Parameters:
        distarray: It is the two dimensional matrix consisting of distances between the Kiosk Centers.
        listind: It is the index positions of the Kiosk Center.
    Returns the visited list which is the shortest route according to this approach,
    totaldist which is the total distance covered and the distance_List which is the list of minimum distance from
    one node to the other.
    """
    # Inititalization
    visited = []
    distance_List = []
    totaldist = 0
    #print(distarray)
    
    #Adding the start position to the list
    if len(visited) == 0: 
        visited.append(listind[0])
        visitedDist = distarray[0]
   
    for i in range(0,len(distarray)-1):
        # Finding the shortest distance from the current kiosk to the next kiosk center.
        short_Node,distance = findShortestDist(visitedDist,1,visited)
        visited.append(short_Node)
        distance_List.append(distance)
        #print("in main function short_node = ",short_Node,"Distance= ",distance)
        totaldist = totaldist + distance
        visitedDist = distarray[short_Node]
        #print("visited ",visited)
    #add the path from the last visited kiosk to original destination
    distEndToFirst = distarray[short_Node][0]
    visited.append(0)
    totaldist = totaldist +distEndToFirst
    distance_List.append(distEndToFirst)
    
    return visited,totaldist,distance_List

    
    
    
def print_route(route,distance,names):
    """
    The method displays the route from the first kiosk center to the next center and displays the total distance
    Parameters: 
        route:list of the index positions of the kiosk centers in the route
        distance:total distance for this route
        names:List of names of the centers
    """
    print("The route to be followed :")
    print("Route ", end=" "),
    for i in route:
        print(" -> ",names[i],end = " "),
    print()
    print("Total Distance = ",distance, " km")
    
  
    

def two_opt_swap(route, i, k):
    """
    The method eliminates the crossover paths by swapping the two edges reversing a section of nodes in the path
    and a new route is returned by 2opt swapping
    Paramters:
        route: The list of index positions of the kiosk centers in the route
        i: the index from which the part of the route is reversed
        k: the index till which the part of the route is reversed
   Returns the new route to the two_opt function
    """
    #Precondition
    assert i >= 0 and i < (len(route) - 1)
    assert k > i and k < len(route)
    
    #Add the route from 0 to i-1 to the new route
    new_route = route[0:i]
    #reverse the route from i to k and add it the the new route
    new_route.extend(reversed(route[i:k + 1]))
    #add the route from k+1 to the end to the new route 
    new_route.extend(route[k+1:])
    
    #Postcondition to check the length of the new route = old route
    assert len(new_route) == len(route)
    
    return new_route
    
    
    
    
def two_opt(route,distarray):
    """
    The method improves the existing route using the 2-opt swap method. It removes the
    crossover paths in the route and improves the route until no improvement can be done.
    The algorithm used is : https://en.wikipedia.org/wiki/2-opt
    
    Parameters:
        route: The list of index positions of the kiosk centers in the route
        distarray: It is the two dimensional matrix consisting of distances between the Kiosk Centers. This is used
        as parameter to calculate the total distance of the route.
    Returns the best route and the next best route for the two drivers with the total distances
    """
    #Initialization
    improvement = True
    best_route = route
    prev_route = route
    best_distance = calculateDistance(route,distarray)
    prev_distance = best_distance
    while improvement: 
        improvement = False
        for i in range(1,len(best_route)):
            for k in range(i+1, len(best_route)-1):
                #Call two_opt_swap to find the new route
                new_route = two_opt_swap(best_route, i, k)
                #Calculate the new distance
                new_distance = calculateDistance(new_route,distarray)
                if new_distance < best_distance:
                    #if new distance is less than the old distance, assign the best_route to the prev_route
                    # and assign new_route to the best_route
                    prev_route = best_distance
                    prev_route = best_route
                    best_distance = new_distance
                    best_route = new_route
                    improvement = True
                    break
                    #improvement found, return to the top of the while loop
            if improvement:
                break
    #Postcondition: Check the best route length = length of the route passed to the method.
    assert len(best_route) == len(route)
    
    return best_route,best_distance,prev_route,prev_distance