# Request Stim Change
## The objective of this program is to hit the box with, requesting
## not 1 but 2 different stim configuration groups, so we can see
## what the returned JSON looks like, so we can incorporate this into
## our mock box. 
import websockets
import asyncio
import json

async def SendStim():
    ip_addr = "192.168.42.1"
    port = "7890"
    url = "ws://" + ip_addr + ":" + port

    async with websockets.connect(url) as ws:
        # connect and provide ID - determine the class of listener.
        while True:                                     # ID check loop
            msg = await ws.recv()                       # Non-blocking, waits for a new message to arrive from the server
            if msg == "ID_REQ":                         # If the message is an ID Request
                my_client_id = 11                        # Fetch this client's ID, in this case it's hardcoded
                await ws.send(str(my_client_id))        # Non-blocking, sends the client ID
                print("connected Successfully as stim")
                break                                   # out of ID check loop
        
        #send a stim request forever 
        while True: 
            #first stim request dictionary
            sd1 = {} #stim dictionary
            sd1["elecCath"] = [1, 12]
            sd1["elecAno"] = [3,4]
            sd1["amp"] = 300
            sd1["freq"] = 20 
            sd1["pulseWidth"] = 100 
            sd1["isContinuous"] = 0

            #second stim request dictionary
            sd2 = {}
            sd2["elecCath"] = [7, 8]
            sd2["elecAno"] = [9,10]
            sd2["amp"] = 200
            sd2["freq"] = 30
            sd2["pulseWidth"] = 150 
            sd2["isContinuous"] = 0

            #stim clear dictionary
            sdc = {}
            sdc["elecCath"] = []
            sdc["elecAno"] = []
            sdc["amp"] = 0
            sdc["freq"] = 20 
            sdc["pulseWidth"] = 100 
            sdc["isContinuous"] = 0

            stimPacket = [sd1, sd2]
            Clear = True 
            if Clear:
                stimPacket = [sdc]

            #send stim packet
            await ws.send(json.dumps(stimPacket))
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(SendStim())  # Set the listen() function to run once
        print("stim send finished normally")
    except KeyboardInterrupt:
        print("Process canceled by user, quitting...")
    except Exception as e:
        print("ERROR")
        print(e)