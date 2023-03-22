from __future__ import print_function
import codecs
import json
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
from util_funs import arm_and_takeoff, create_mission, distance_to_current_waypoint, parse_json
def do_mission(vehicle,data):
    print('GCS:validating JSON')
    data=json.loads(data)
    print('GCS:Sorting JSON by waypoint order')
    data=sorted(data,key=lambda d: d['index'])
    n_points=len(data)
    print(*data)
    #parsing the JSON file for waypoint
    waypoints=parse_json(data)
    #creating a mission from given waypoints
    create_mission(vehicle=vehicle,waypoints=waypoints)
    #Arm the drone and take off with the specified altitude
    print('GCS:starting to arm')
    altitude=10
    arm_and_takeoff(aTargetAltitude=altitude,vehicle=vehicle)
    print('GCS:starting mission')
    #reseting to 0th waypoint
    vehicle.command.next=0
    vehicle.mode=VehicleMode("AUTO")
    # Mission Monitoring 
    while True:
        nextwaypoint=vehicle.commands.next
        print('GCS:Distance to waypoint (%s): %s' % (nextwaypoint, distance_to_current_waypoint(vehicle=vehicle)))
        
    
        if nextwaypoint==n_points+1: #Dummy waypoint - as soon as we reach waypoint 4 this is true and we exit.
            print("Exit 'standard' mission when start heading to final waypoint (5)")
            break
        time.sleep(1)