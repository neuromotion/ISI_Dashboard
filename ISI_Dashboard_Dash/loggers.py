## loggers.py
## loggers are print statments that can be conditionally activated if needed
## in the main code with a simple line toggle. this keep the application code
## in app.py clean, while having conditional logging ability. 

import dash


def parseMessage(outs):
        """
        log the incoming messages
        input: 
            outs: list of outputs, with default value of 
        """
        if type(outs[1]) != type(dash.no_update):
            soh = outs[1]      
            print("soh Type: " + str(type(soh)))
            print("soh length: " + str(len(soh)))
            print("soh value:" + str(soh),flush=True)
            print("    ")
        
        if type(outs[2]) != type(dash.no_update):
            stim = outs[2] 
            print("stim Type: " + str(type(stim)))
            print("stim length: " + str(len(stim)))
            print("stim value:" + str(stim),flush=True)
            print("     ")

