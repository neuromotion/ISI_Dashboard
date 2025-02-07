# from dash import Dash, html
# import dash_bootstrap_components as dbc

# # Initialize the Dash app with Bootstrap theme
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # Create the layout
# app.layout = dbc.Container([
#     dbc.Row([
#         # First Column
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     html.H4("Column 1"),
#                     html.P("Content for column 1")
#                 ])
#             ])
#         ], width=3),  # width=4 makes each column take up 1/3 of the space (12/3 = 4)
        
#         # Second Column
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     html.H4("Column 2"),
#                     html.P("Content for column 2")
#                 ])
#             ])
#         ], width=3),
        
#         # Third Column
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     html.H4("Column 3"),
#                     html.P("Content for column 3")
#                 ])
#             ])
#         ], width=3)
#     ], className="mt-4")  # Add margin top for spacing
# ], fluid=True)  # fluid=True makes the container take up the full width

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Create three sample graphs
graph1 = dcc.Graph(figure=px.scatter(x=[1, 2, 3], y=[4, 5, 6]))
graph2 = dcc.Graph(figure=px.scatter(x=[1, 2, 3], y=[4, 5, 6]))
graph3 = dcc.Graph(figure=px.scatter(x=[1, 2, 3], y=[4, 5, 6]))

# Simple flexbox layout
app.layout = html.Div([
    html.Div([
        graph1,
        graph2,
        graph3
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'gap': '20px'
    })
])

if __name__ == '__main__':
    app.run_server(debug=True)