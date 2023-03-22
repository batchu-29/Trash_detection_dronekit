import json
from websockets import connect as wsconnect
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import argparse
import asyncio
from mission import do_mission
from server_request import make_request
from util_funs import arm_and_takeoff, create_mission, distance_to_current_waypoint
parser=argparse.ArgumentParser(description='Demonstrates basic mission operations')
parser.add_argument('--connect',help="vehicle connection target string. if not specified,SITL automaticall started and used")
args=parser.parse_args()
connection_string="tcp:127.0.0.1:5763"
#connection to vehicle
print('GCS:connecting to vehicle on :%s'% connection_string)
vehicle=connect(connection_string,wait_ready=True)
WSS_URL=r"ws://127.0.0.1:3001/socket/command?device=drone"
async def connecting(url):
    async with wsconnect(url) as websocket:
        print("connected")
        await websocket.send(json.dumps({"message":"gs_update","status":"unarmed"}))
        print("connecting to the server")
        while True:
            message=await websocket.recv()
            print(message)
            print("waiting for commands")
            message=json.loads(message)
            if("command" in message):
                if(message["command"]=="LAUNCH"):
                    print("LAUNCH")
                    mission_id=message["id"]
                    await websocket.send(json.dumps({"message":"gs_update","status":"armed"}))
                    do_mission(vehicle=vehicle,data=message["waypoints"])
                    mission_id=message["id"]
                    print("making a request to server to generate a flight id")
                    make_request(mission_id)
                    asyncio.sleep(8)
                    await websocket.send(json.dumps({"message":"gs_update","status":"unarmed"}))
asyncio.run(connecting(WSS_URL))

    
    


