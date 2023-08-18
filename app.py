import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Button('Refresh Inputs', id='refresh_button'),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Store(id='data_store'),
                html.P('Use the figure below to select channel data'),
                dcc.Graph(id='input_figure', style={'height': 650}),
            ])
        ], width=3),
        dbc.Col([
            html.Div([
                html.P('Channel data will show on the figure below'),
                dcc.Store(id='active_channels'),
                dcc.Graph(id='output_figure', style={'height': 650, 'width': '100%'}),
            ]),
        ], width=9)
    ])
])


@app.callback(
    Output('data_store', 'data'),
    Input('refresh_button', 'n_clicks'),
)
def populate_data(n_clicks):
    # n_clicks just increments, we only need it to re-generate the data
    x, y = np.meshgrid(np.arange(0, 4), np.arange(0, 8))
    colors = np.random.randint(0, 3, size=8*4)

    df = pd.DataFrame({'x': x.ravel(), 'y': y.ravel(), 'color': colors})
    df['index'] = df['y'] + 8 * df['x']
    df.loc[df['y'] > 3, 'y'] += 1
    df['signal_data'] = [np.random.randn(50) for i in range(32)]

    return df.to_dict()

@app.callback(
    Output('input_figure', 'figure'),
    Input('data_store', 'data'),
    prevent_initial_call=True
)
def render_figure(data):
    if not data:
        return dash.no_update
    df = pd.DataFrame(data)
    fig = go.Figure()
    for color, _df in df.groupby('color'):
        fig.add_trace(
            go.Scatter(
                x=_df['x'].to_list(), 
                y=_df['y'].to_list(), 
                text=_df['index'].to_list(), 
                textfont=dict(
                    family="sans serif",
                    size=18,
                    color="White"
                ),
                mode='markers+text',
                marker={'size': 40}))
    fig.update_layout({
        'template': 'simple_white',

        'showlegend': False
    })
    fig.update_xaxes(mirror=True, showticklabels=False, ticks='')
    fig.update_yaxes(mirror=True, showticklabels=False, ticks='')
    return fig

@app.callback(
    Output('active_channels', 'data'),
    Input('input_figure', 'clickData'),
    State('active_channels', 'data'),
)
def populate_active_channels(clickData, data):
    data = data or []
    if not clickData:
        return dash.no_update
    index = clickData['points'][0]['text']
    print(index, data)
    if index in data:
        print('removing index')
        data = [i for i in data if i != index]
    else:
        data.append(index)
    return data

@app.callback(
    Output('output_figure', 'figure'),
    Input('active_channels', 'data'),
    Input('data_store', 'data'),
    prevent_initial_call=True
)
def populate_output_figure(active_channels, data):
    if not data or not active_channels:
        return go.Figure()
    df = pd.DataFrame(data)
    if active_channels:
        signal_data = df[df['index'].astype(str).isin(active_channels)]
        fig = go.Figure()
        for i, _signal in signal_data.iterrows():
            fig.add_trace(go.Scatter(x=np.arange(0, len(_signal['signal_data'])), y=_signal['signal_data'], name=f'Signal Data {_signal["index"]}'))

        fig.update_layout({
            'template': 'simple_white',
        })
        return fig
    return go.Figure()



app.run_server(debug=True, use_reloader=False) 