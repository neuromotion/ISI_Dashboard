# import plotly.graph_objects as go
# import numpy as np

# # Create figure
# fig = go.Figure()

# # Grid parameters 
# rows, cols = 3, 3
# spacing = 2

# # Simple triangle SVG path
# base_path = 'M 0,0 L 1,1 L 2,0 Z'

# # Create grid of triangles
# shapes = []
# for i in range(rows):
#    for j in range(cols):
#        shapes.append({
#            'type': 'path',
#            'path': base_path,
#         #    'path_transform': f'translate({j*spacing}, {i*spacing})',
#            'path_transform': f'translate({j*spacing}, {i*spacing})',
#            'fillcolor': f'rgba({i*50},{j*50},100,0.5)',
#            'line': {'color': 'black'},
#            'xref': 'x',
#            'yref': 'y'
#        })

# # Update layout with shapes
# fig.update_layout(
#    shapes=shapes,
#    xaxis_range=[-1, cols*spacing+1],
#    yaxis_range=[-1, rows*spacing+1],
#    showlegend=False
# )

# fig.show()

#%%

import plotly.graph_objects as go
import numpy as np

fig = go.Figure()

rows, cols = 3, 3
spacing = 2

shapes = []
for i in range(rows):
    for j in range(cols):
        # Apply translation by modifying coordinates
        x_offset = j * spacing
        y_offset = i * spacing
        # path = f'M {x_offset},{y_offset} L {x_offset+1},{y_offset+1} L {x_offset+2},{y_offset} Z'
        # path = f'M {x_offset},{y_offset} h 8.92 q 1.26 0 1.26 1.26 v 14.95 q 0 1.26 -1.26 1.26 h -8.92 q -1.26 0 -1.26 -1.26 v -14.95 q 0 -1.26 1.26 -1.26 Z'
        # path = f'M {x_offset},{y_offset} ' + \
        # f'h 8.92 ' + \
        # f'v 17.47 ' + \
        # f'h -8.92 ' + \
        # f'Z'
        path="m 38.055213,19.329161 h 6.410221 c 0.695528,0 1.255466,0.559937 1.255466,1.255465 v 14.959658 c 0,0.695528 -0.559938,1.255465 -1.255466,1.255465 h -6.410221 c -0.695528,0 -1.255466,-0.559937 -1.255466,-1.255465 V 20.584626 c 0,-0.695528 0.559938,-1.255465 1.255466,-1.255465 z"

        
        shapes.append({
            'type': 'path',
            'path': path,
            'fillcolor': f'rgba({i*50},{j*50},100,0.5)',
            'line': {'color': 'black'},
            'xref': 'x',
            'yref': 'y'
        })

fig.update_layout(
    shapes=shapes,
    xaxis_range=[-1, cols*spacing+3],
    yaxis_range=[-1, rows*spacing+1],
    showlegend=False
)

fig.show()
# %%
