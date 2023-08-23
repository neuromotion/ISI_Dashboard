import websockets
import asyncio
import json

async def hello(websocket):
    #handshake
    while 1:
        await websocket.send("ID_REQ")
        name = await websocket.recv()
        if name == str(1):
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

        # configure stim group packet
        sd1 = {}
        sd1["elecCath"] = [1,12,13,144]
        sd1["elecAno"]  = [3,4,145]
        sd1["amp"] = 300
        sd1["freq"] = 20 
        sd1["pulseWidth"] = 100 
        sd1["isContinuous"] = 0

        msg = {}
        msg['msg'] = sd1
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

