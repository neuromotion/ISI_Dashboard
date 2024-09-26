"""
ISI-Dash-backend.py

this is the backend for the ISI dashboard. It retrieves data from sources such as
the web-logger, the myocycle, Vicon, etc, and performs processing on that data in python,
getting it prepped for visualization in the react frontend.
"""
#imports: 
import numpy as np
from enum import Enum
import json
import time
import asyncio
import websockets
from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware

# class Logger:
#     """
#     the logger periodically sends data to the code-on-the-box logger server by getting it 
#     from the kinematics data buffer and shipping it out. It's main responsibility is maintaining
#     a websocket client.
#     """
#     def __init__(self):
#         self.enabled = False            # should logging be enabled?
#         self.logTask = None             # link to the asyncio task object that will run the log task.
#         self.isActivelyLogging = False  # is data actively being sent to the logging server after a successful connection?
#         self.loggingPeriod = 1          # [secs]
#         self.clientID = "2"             # client ID to communicate with code-on-the-box as a logger

#     async def log(self):
#         """
#         communicate with code-on-the-box websocket server.
#         """
#         # init - information about where the remote logging server on the network!
#         print("Entered Log Function")
#         # ip_addr = "192.168.42.150"
#         ip_addr = "127.0.0.1"
#         port = "7890"
#         url = "ws://" + ip_addr + ":" + port

#         # continuously issue connection attempts that timeout until we connect
#         # with the the code-on-the-box websocket server
#         nConnectionAttempts = 0
#         while 1: 
#             print(f"connection Attempt {nConnectionAttempts}")
#             nConnectionAttempts += 1
#             try:
#                 async with websockets.connect(url,open_timeout=5) as websocket: #if timeout < 5, this method fails as it doesn't throw an error.
#                     print("sucessfully Connected to Server!")

#                     # ID check to request class of client
#                     while 1:                                         
#                         msg = await websocket.recv()                 # Non-blocking, waits for a new message to arrive from the server
#                         if msg == "ID_REQ":                          # If the message is an ID Request
#                             await websocket.send(self.clientID)      # Non-blocking, sends the client ID
#                             print("connected Successfully as logger")
#                             break                                    # out of ID check loop

#                     #stream logging data back to server
#                     while 1:
#                             if self.enabled:
#                                 self.isActivelyLogging = True
#                                 self.healthStatusLED.toggle()
#                                 dataBuffer = sampler.kinematicsDataBuffer.getJSON()
#                                 await websocket.send(dataBuffer)
#                             else:
#                                 # we need to ping the log server when logging is
#                                 #  not eanbled to effectively to "check" that 
#                                 # the remote logger is alive, then we will see 
#                                 # if / when the connection is closed.
#                                 await websocket.ping() 
#                             #wait
#                             await asyncio.sleep(1)

#             # when connection cancelled by server
#             except websockets.ConnectionClosed as e:
#                 print(f"WebSocket error: {e}")
#                 print("disconnected from server.")
#                 print("Attempting Reconnection in 5 seconds ....")
#                 await asyncio.sleep(2)

#             # can't find server
#             except Exception as e:
#                 print(f" error: {e}")
#                 print("can't find server")
#                 print("Attempting Reconnection in 5 seconds ....")
#                 await asyncio.sleep(2)

#--------------------- define web API's --------------------
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#--------- register other coroutines with the fastAPI event loop ----------
# @app.on_event("startup")
# async def startup_event():
#     asyncio.get_event_loop().create_task(sampler.sample())
#     logger.logTask = asyncio.get_event_loop().create_task(logger.log())  #store ref incase reboot required.

#--------------------------- define HTTP API -----------------------------
# check API is up
@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/ScatterExample")
# async def SA():
#     packet = {}
#     packet["x"] = range(2)
#     packet["y"] = np.random.randint(low=0,high=5,size=3)
#     return json.dumps(packet)



# @app.get("/ScatterExample")







# # useful for calibration
# @app.get("/Counts")
# async def getCounts():
#     return {"counts": str(crank.encoderCounter.fetchCount())}

# @app.get("/Offset/")
# def updateOffset(offset: int = 0):
#     #sets offset
#     cpr = crank.encoderCounter.CPR
#     if offset > cpr or offset < -cpr:
#         raise HTTPException(status_code=422, detail="count offset should be < CPR and > -CPR")

#     crank.encoderCounter.countOffset = offset
#     crank.encoderCounter.writeDTR()

#     return {"offset": str(crank.encoderCounter.countOffset)}

# # rebooting from system malfunction
# @app.get("/rebootWSclient")
# async def rebootWSclient():
#     """
#     if the websocket client hasn't connected in a long time (days) it may
#     fail to connect to the logging client, or take a very long time to do so. 
#     this API function allows for a quick reboot of the logging system, without
#     having reboot the entire system (linux)
#     """
#     try:
#         logger.logTask.cancel() # cancel the logging task
#         logger.logTask = asyncio.get_event_loop().create_task(logger.log())
#         return {"reboot":"success"}
#     except Exception as e:
#         return {"reboot":f"{e}"}

# # main API
# @app.get("/enableLogging/")
# async def updateLogging(logging: bool = False):
#     logger.enabled = logging
#     return {"logging": logging}

# @app.get("/isActivelyLogging")
# async def updateLogging():
#     return {"logging": logger.isActivelyLogging}

# @app.get("/getKinematics")
# async def getKinematics():
#     """
#     get kinematics is called at a max of 7Hz, sometimes asynchronously.
#     """
#     #since we are sampling asynchronously, we won't use this call to 
#     # update crank state (velocity) but we will but get freshest possible position.
#     # pos = crank.computePos() # if we want freshest data
#     return {"position": str(crank.pos),"velocity":str(crank.vel)} #use cached velocity info, sampled regularly at 100Hz


#-------------------------------- debugging ----------------------------------
import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)