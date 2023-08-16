import websockets
import asyncio
import json

async def listen():
    # ip_addr = "192.168.42.1"
    ip_addr = "192.168.42.150"
    port = "7890"
    url = "ws://" + ip_addr + ":" + port

    async with websockets.connect(url) as ws:
        # connect and provide ID - determine the class of listener.
        while True:                                     # ID check loop
            msg = await ws.recv()                       # Non-blocking, waits for a new message to arrive from the server
            if msg == "ID_REQ":                         # If the message is an ID Request
                my_client_id = 1                        # Fetch this client's ID, in this case it's hardcoded
                await ws.send(str(my_client_id))        # Non-blocking, sends the client ID
                print("connected Successfully as logger")
                break                                   # out of ID check loop
        
        #read a single message then break
        while True:
            msg = await ws.recv()                       # Non-blocking, waits for a new message to arrive from the server
            if canDecodeJSON(msg):
                #msgDict = json.loads(msg)
                #print(msgDict, flush=True)
                #print(msg,flush = True)
                print(msg.replace("\\n","\n"), flush=True)
                print('\n')
        #await ws.close()

def canDecodeJSON(string):
    try:
        _ = json.loads(string)
        return True
    except:
        return False           


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(listen())  # Set the listen() function to run once
        print("Listen loop finished normally")
    except KeyboardInterrupt:
        print("Process canceled by user, quitting...")
    except Exception as e:
        print("ERROR")
        print(e)