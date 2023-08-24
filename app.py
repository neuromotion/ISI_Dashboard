import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import json

#from dash.dependencies import Input, Output, State
from dash import Dash #, dcc, html
from dash_extensions import WebSocket
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy,State

# custom components library.
from customComponents import ElectrodeArray
from customComponents import StimGroup
import loggers as log
import utils

# initialize plotting objects
CaudalArray = ElectrodeArray("Caudal")
RostralArray = ElectrodeArray("Rostral")


app = DashProxy(external_stylesheets=[dbc.themes.BOOTSTRAP]) #does this need to be dash proxy?
app.layout = html.Div([
    #WebSocket(id="ws", url="ws://192.168.42.150:7890"),
    WebSocket(id="ws", url="ws://127.0.0.1:7890"),
    dcc.Store(id='soh_json'),
    dcc.Store(id='stim_ack_json'),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(figure=CaudalArray.fig,id='Caudal_array', style={'height': 650,'width':'100%'}),
            ])
        ], width=3),
        dbc.Col([
                html.Div(id='CaudalStimGroups')
        ], width=3,style={'padding': 10, 'flex': 1}),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(figure=RostralArray.fig,id='Rostral_array', style={'height': 650,'width':'100%'}),
            ])
        ], width=3),
        dbc.Col([
                html.Div(id='RostralStimGroups')
        ], width=3,style={'padding': 10, 'flex': 1}),
    ]),
    # dbc.Col([
    #     html.Div(id="StimGroups")
    # ])
])

@app.callback(
        Output("ws", "send"),
        Output("soh_json", "data"),
        Output("stim_ack_json","data"),
        Input("ws", "message"),
        prevent_initial_call=False
    )
def parseMessage(e):
    """
    handshake with the box, and store
    each message that arrives in the appropriate 
    container. 
    """
    # return data vector
    out = 3 * [dash.no_update]  

    # first call guard
    if e is None:               
        return out
    
    # handshake guard
    if e['data'] == "ID_REQ":   
        out[0] = str(1)
        return out
    
    # parse and store messages
    ed = json.loads(e['data'])

    if ed['msg_type'] == "soh_json":
        out[1] = ed['msg']
    
    elif ed['msg_type'] == "stim_ack_json":
        out[2] = ed['msg']

    #log.parseMessage(out)
    
    return out


@app.callback( 
        Output("Caudal_array", "figure"),
        Output("Rostral_array", "figure"),
        Input("stim_ack_json", "data"),
        Input("soh_json"     , "data"),  
    )
def updateElectrodeArrays(stim,soh):
    """
    update the Caudal and Rostral Electrode
    arrays based on data becoming availble in
    the dcc.store objects
    inputs:
        stim is a list of dictionaries
        soh is a dictionary
    """
    # guard clause (startup may have some extra Nones)
    if stim is None or soh is None: 
        print("hit",flush=True)
        return dash.no_update , dash.no_update
    
    # repackage pins
    Pins = {}
    Pins['Gnd']       = soh['Gnd']
    Pins['Ref']       = soh['Ref']
    Pins['elecCath']  = utils.dictCollect(stim,'elecCath')
    Pins['elecAno']    = utils.dictCollect(stim,'elecAno')

    #pass all pins in, arrays handle rendering
    CaudalArray = ElectrodeArray("Caudal")
    CaudalArray.update(Pins)
    RostralArray = ElectrodeArray("Rostral")
    RostralArray.update(Pins)
    
    return CaudalArray.fig , RostralArray.fig


@app.callback( 
        Output("CaudalStimGroups", "children"),
        Output("RostralStimGroups", "children"),
        Input("stim_ack_json", "data"),
    )
def updateStimGroups(stimGroups):
    """
    update Stim Groups graphs based on data
    becoming availble in the dcc.store objects
    inputs:
        stimGroups is a list of dictionaries
    outputs:
        a list of graph objects
    """
    # guard clause 
    if stimGroups is None:
        return dash.no_update , dash.no_update
     
    # there should never be mixed pins, be we will define 
    # the side of the stim group to which location has more
    # pins
    def determineSGloc(sgPacket):
        pins = []
        pins.extend(sgPacket['elecCath']) 
        pins.extend(sgPacket['elecAno'])
        
        nCpins = 0; nRpins = 0
        for pin in pins: 
            if pin > 128: 
                nRpins+= 1
            else: 
                nCpins+=1 
        
        if nCpins >= nRpins: 
            return "Caudal"
        else:
            return "Rostral"
        return pins
    

    # parse stim packet
    caudalFigs = [] ; rostralFigs = []
    for groupNum,sgPacket in enumerate(stimGroups):
        sg = StimGroup()
        sg.update(sgPacket,groupNum) 
        loc = determineSGloc(sgPacket)
        if loc == "Caudal":
            caudalFigs.append(dcc.Graph(figure=sg.fig))
        elif loc == "Rostral":
            rostralFigs.append(dcc.Graph(figure=sg.fig))

    return caudalFigs , rostralFigs 




# @app.callback( 
#         Output("Caudal_array", "figure"),
#         Output("Rostral_array", "figure"),
#         Input("stim_ack_json", "data"),
#         Input("soh_json"     , "data"),  
#     )
# def updateElectrodeArrays(stim,soh):
#     """
#     update the Caudal and Rostral Electrode
#     arrays based on data becoming availble in
#     the dcc.store objects
#     """
#     # guard clause (startup has some extra nones)
#     if stim is None or soh is None: 
#         print("hit",flush=True)
#         return dash.no_update , dash.no_update

#     # array filts (we don't need to filter strictly speaking)
#     cfilt = lambda pins: [pin for pin in pins if pin < 128]
#     rfilt = lambda pins: [pin for pin in pins if pin > 128]

#     # Caudal Array:
#     cPins = {}
#     cPins['Gnd']       = cfilt(soh['Gnd'])
#     cPins['Ref']       = cfilt(soh['Ref'])
#     cPins['elecCath']  = cfilt(stim['elecCath'])
#     cPins['elecAno']   = cfilt(stim['elecAno'])
    
#     CaudalArray = ElectrodeArray("Caudal")
#     CaudalArray.update(cPins)

#     # Rostral Array:
#     rPins = {}
#     rPins['Gnd']       = rfilt(soh['Gnd'])
#     rPins['Ref']       = rfilt(soh['Ref'])
#     rPins['elecCath']  = rfilt(stim['elecCath'])
#     rPins['elecAno']   = rfilt(stim['elecAno'])
    
#     RostralArray = ElectrodeArray("Rostral")
#     RostralArray.update(rPins)

#     return CaudalArray.fig , RostralArray.fig


### where am I at: 

## upgrade to handle multiple stim groups
## finish parameterizing plot
## add some text / labels / make things look nicer.
    
    



## no global vars that will be mutated, you can have read only globals.
## all callbacks are pure functions - so instead of modifying older graphs, you build new ones. 
## you don't get a global reference to the app.layout object, instead if you want to modify it in a callback, you need to pass it in. 
## thus, the state of the program is encapsulated in the components, which get passed into the callbacks.
## to get app information into your callback without having it change, you need to use the state 
## pass along information
## you can't have side-effects that access or modify the layout.
## you can null and output - this is a critical insight, as it enables certian design patterns.
## don't modify a figure, build a new one and replace the old figure. 
## for flexability, write a group of figures into a div.

## 1 to handle reading the message and writing it into state
## 1 callback to handle to handle hand shaking.  
## 1 callback per conceptual block update
## follow above principles, not the approach below. 

## the approach we will take will be to have 

## where does this leave us? 
## next week -> get websockets working in dash, get data streaming in 
## design: 
# have a websocket listener callback
# handshaking code goes inside this callback
# message parsing also goes in here. 
# establishment of connection is done by dash extensions. 
# we define our custom graphics components in Custom components library
# these components encapsulate their own state. 
# the callback reads the messages 1 by 1, then for each type of message, it mutates the state.
# might have to have this callback fire off other callbacks? 
# not sure how to handle the variable number of graphs yet. 
# this architecture seems right



# import websockets
# import asyncio
# import json

# async def SendStim():
#     ip_addr = "192.168.42.1"
#     port = "7890"
#     url = "ws://" + ip_addr + ":" + port

#     async with websockets.connect(url) as ws:
#         # connect and provide ID - determine the class of listener.
#         while True:                                     # ID check loop
#             msg = await ws.recv()                       # Non-blocking, waits for a new message to arrive from the server
#             if msg == "ID_REQ":                         # If the message is an ID Request
#                 my_client_id = 11                        # Fetch this client's ID, in this case it's hardcoded
#                 await ws.send(str(my_client_id))        # Non-blocking, sends the client ID
#                 print("connected Successfully as stim")
#                 break                                   # out of ID check loop
        
#         #send a stim requests forever 
#         while True: 
#             await ws.send(json.dumps(refs))
#             await ws.send(json.dumps(stimPacket))
#             await asyncio.sleep(1)


# loop = asyncio.get_event_loop()
# serverTask = loop.create_task(SendStim())
# serverTask


# ### an application to read a stream from the quart server over websockets. 
# from dash_extensions import WebSocket
# from dash_extensions.enrich import html, dcc, Output, Input, DashProxy

# # Client-side function (for performance) that updates the graph.
# update_graph = """function(msg) {
#     if(!msg){return {};}  // no data, just return
#     const data = JSON.parse(msg.data);  // read the data
#     return {data: [{y: data, type: "scatter"}]}};  // plot the data
# """
# # Create small example app.
# app = DashProxy(__name__)
# app.layout = html.Div([
#     WebSocket(id="ws", url="ws://127.0.0.1:5000/random_data"),
#     dcc.Graph(id="graph")
# ])
# app.clientside_callback(update_graph, Output("graph", "figure"), Input("ws", "message"))

# if __name__ == "__main__":
#     app.run_server()

# @app.callback(
#     Output('data_store', 'data'),
#     Input('refresh_button', 'n_clicks'),
# )
# def populate_data(n_clicks):
#     # n_clicks just increments, we only need it to re-generate the data
#     x, y = np.meshgrid(np.arange(0, 4), np.arange(0, 8))
#     colors = np.random.randint(0, 3, size=8*4)

#     df = pd.DataFrame({'x': x.ravel(), 'y': y.ravel(), 'color': colors})
#     df['index'] = df['y'] + 8 * df['x']
#     df.loc[df['y'] > 3, 'y'] += 1
#     df['signal_data'] = [np.random.randn(50) for i in range(32)]

#     return df.to_dict()

# @app.callback(
#     Output('input_figure', 'figure'),
#     Input('data_store', 'data'),
#     prevent_initial_call=True
# )
# def render_figure(data):
#     if not data:
#         return dash.no_update
#     df = pd.DataFrame(data)
#     fig = go.Figure()
#     for color, _df in df.groupby('color'):
#         fig.add_trace(
#             go.Scatter(
#                 x=_df['x'].to_list(), 
#                 y=_df['y'].to_list(), 
#                 text=_df['index'].to_list(), 
#                 textfont=dict(
#                     family="sans serif",
#                     size=18,
#                     color="White"
#                 ),
#                 mode='markers+text',
#                 marker={'size': 40}))
#     fig.update_layout({
#         'template': 'simple_white',

#         'showlegend': False
#     })
#     fig.update_xaxes(mirror=True, showticklabels=False, ticks='')
#     fig.update_yaxes(mirror=True, showticklabels=False, ticks='')
#     return fig

# @app.callback(
#     Output('active_channels', 'data'),
#     Input('input_figure', 'clickData'),
#     State('active_channels', 'data'),
# )
# def populate_active_channels(clickData, data):
#     data = data or []
#     if not clickData:
#         return dash.no_update
#     index = clickData['points'][0]['text']
#     print(index, data)
#     if index in data:
#         print('removing index')
#         data = [i for i in data if i != index]
#     else:
#         data.append(index)
#     return data

# @app.callback(
#     Output('output_figure', 'figure'),
#     Input('active_channels', 'data'),
#     Input('data_store', 'data'),
#     prevent_initial_call=True
# )
# def populate_output_figure(active_channels, data):
#     if not data or not active_channels:
#         return go.Figure()
#     df = pd.DataFrame(data)
#     if active_channels:
#         signal_data = df[df['index'].astype(str).isin(active_channels)]
#         fig = go.Figure()
#         for i, _signal in signal_data.iterrows():
#             fig.add_trace(go.Scatter(x=np.arange(0, len(_signal['signal_data'])), y=_signal['signal_data'], name=f'Signal Data {_signal["index"]}'))

#         fig.update_layout({
#             'template': 'simple_white',
#         })
#         return fig
#     return go.Figure()



# app.run_server(debug=True, use_reloader=False) 
app.run_server(debug=False, use_reloader=False) 


