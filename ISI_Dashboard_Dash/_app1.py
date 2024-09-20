# from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback

# app = Dash(__name__)

# app.layout = html.Div(
#     [
#         html.Button("Add Filter", id="add-filter-btn", n_clicks=0),
#         html.Div(id="dropdown-container-div", children=[]),
#         html.Div(id="dropdown-container-output-div"),
#     ]
# )


# @callback(
#     Output("dropdown-container-div", "children"), Input("add-filter-btn", "n_clicks")
# )
# def display_dropdowns(n_clicks):
#     patched_children = Patch()
#     new_dropdown = dcc.Dropdown(
#         ["NYC", "MTL", "LA", "TOKYO"],
#         id={"type": "city-filter-dropdown", "index": n_clicks},
#     )
#     patched_children.append(new_dropdown)
#     return patched_children


# @callback(
#     Output("dropdown-container-output-div", "children"),
#     Input({"type": "city-filter-dropdown", "index": ALL}, "value"),
# )
# def display_output(values):
#     return html.Div(
#         [html.Div(f"Dropdown {i + 1} = {value}") for (i, value) in enumerate(values)]
#     )


# if __name__ == "__main__":
#     app.run(debug=True)

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

        html.Br(),
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                     ['Montréal', 'San Francisco'],
                     multi=True),

        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
    ], style={'padding': 10, 'flex': 1}),

    html.Div(children=[
        html.Label('Checkboxes'),
        dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                      ['Montréal', 'San Francisco']
        ),

        html.Br(),
        html.Label('Text Input'),
        dcc.Input(value='MTL', type='text'),

        html.Br(),
        html.Label('Slider'),
        dcc.Slider(
            min=0,
            max=9,
            marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
            value=5,
        ),
    ], style={'padding': 10, 'flex': 1})
], style={'display': 'flex', 'flex-direction': 'row'})

if __name__ == '__main__':
    app.run(debug=True)