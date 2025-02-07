import websockets
import asyncio
import json

async def hello(websocket):
    #handshake
    while 1:
        await websocket.send("ID_REQ")
        name = await websocket.recv()
        if name == str(1):
            print("connected to mock-box as listner")
            break

    # trickle dictionary.
    while 1:
        await asyncio.sleep(2)
        # configure a SOH message.
        soh_d = {}
        soh_d['Gnd'] = [20,21,129]
        soh_d['Ref'] = [30,31,130]

        msg = {}
        msg['msg'] = soh_d
        msg['msg_type'] = 'soh_json'

        await websocket.send(json.dumps(msg))
        await asyncio.sleep(.2)

        # configure multiple stim group packets
        sg1 = {}
        sg1["elecCath"] = [1,12,14,31,28,29]
        sg1["elecAno"]  = [3]
        sg1["amp"] = 300
        sg1["freq"] = 20 
        sg1["pulseWidth"] = 100 
        sg1["isContinuous"] = 0

        sg2 = {}
        sg2["elecCath"] = [4,6]
        sg2["elecAno"]  = [2,13,15,27]
        sg2["amp"] = 100
        sg2["freq"] = 15 
        sg2["pulseWidth"] = 70
        sg2["isContinuous"] = 0

        sg3 = {}
        sg3["elecCath"] = [129,130,131]
        sg3["elecAno"]  = [159,160]
        sg3["amp"] = 100
        sg3["freq"] = 25 
        sg3["pulseWidth"] = 120 
        sg3["isContinuous"] = 0

        msg = {}
        msg['msg'] = [sg1, sg2, sg3]  # list of dictionaries
        msg['msg_type'] = 'stim_ack_json'
        
        await websocket.send(json.dumps(msg))
        print("sending dict messages!",flush=True)

async def main():
    async with websockets.serve(hello, "localhost", 7890):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())



# #!/usr/bin/env python

# import asyncio
# from websockets.server import serve

# async def echo(websocket):
#     async for message in websocket:

#         await websocket.send(message)

# async def main():
#     async with serve(echo, "localhost", 7890):
#         await asyncio.Future()  # run forever

# asyncio.run(main())

