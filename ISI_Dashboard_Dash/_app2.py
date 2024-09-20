### exploration with dash extensions: 

# from dash_extensions.enrich import DashProxy
# from dash_extensions import Lottie

# app = DashProxy()
# app.layout = Lottie(
#     options=dict(loop=True, autoplay=True), width="25%",
#     url="https://assets6.lottiefiles.com/packages/lf20_rwwvwgka.json"
# )

# if __name__ == '__main__':
#     app.run_server()

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



### an application to read a stream from the quart server over websockets. 
import dash
from dash_extensions import WebSocket
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy

# Client-side function (for performance) that updates the graph.
update_graph = """function(msg) {
    if(!msg){return {};}  // no data, just return
    const data = JSON.parse(msg.data);  // read the data
    return {data: [{y: data, type: "scatter"}]}};  // plot the data
"""
# Create small example app.
app = DashProxy(__name__)
app.layout = html.Div([
    WebSocket(id="ws", url="ws://192.168.42.1:7890"),
    dcc.Graph(id="graph"),
    dcc.Textarea(id = 'dbg',value="debug1")
])
# app.clientside_callback(update_graph, Output("graph", "figure"), Input("ws", "message"))

# @app.callback(
#         Output("ws", "send"),
#         Output("dbg", "value"),
#         [Input("ws", "message")])
# def message(e):
#     if e['data'] == "ID_REQ":
#           return str(11) , dash.no_update
#     else: 
#         #   print(e['data'])
#           return dash.no_update , 'no problem'# json.dumps(e['data'])
          
@app.callback(
        Output("dbg", "value"),
        [Input("ws", "message")])
def message(e):
    if e is not None:
        return "was none"
    return 'work please damit'
if __name__ == "__main__":
    app.run_server()