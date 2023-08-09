"""
MockBox.py
a Mocked version code on the box that can be served over localhost, and which I can 
manipulate ideally via a scripting interface

this could / should run in a jupyter notebook so I can use it interactively
although maybe this will contain the class definition and then the notebook
will import the class and manipulate the parameters. 


"""
import websockets
import asyncio


class MockBox():
    """
    MockBox serves a JSON object over localhost
    """
    def __init__(self):
        self.message = {}  # this is the dictionary that gets served over websocket.
        self.ws = []       # this is the websocket instance 
        



