import plotly.graph_objects as go
import numpy as np

# Generate some sample data
x = np.linspace(0, 10, 5)
y = np.sin(x)

# Create an SVG path for a rounded rectangle
# M: Move to starting point
# h: horizontal line (relative)
# a: arc (rx ry x-axis-rotation large-arc-flag sweep-flag dx dy)
# v: vertical line (relative)
# z: close path
rounded_rect = """
    M-10,-10
    h20
    a10,10 0 0 1 10,10
    v20
    a10,10 0 0 1 -10,10
    h-20
    a10,10 0 0 1 -10,-10
    v-20
    a10,10 0 0 1 10,-10
    z
"""

# Create the figure
fig = go.Figure()

# Add scatter trace with custom marker
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='markers',
    marker=dict(
        symbol='path',
        path=rounded_rect,
        size=30,  # Size of the marker
        color='blue',
        line=dict(color='darkblue', width=2)
    ),
    name='Rounded Rectangles'
))

# Update layout for better visualization
fig.update_layout(
    title='Scatter Plot with Custom Rounded Rectangle Markers',
    xaxis_title='X Axis',
    yaxis_title='Y Axis',
    showlegend=True,
    width=800,
    height=500,
    template='plotly_white'
)

# Display the figure
fig.show()

# You can also modify the roundness by adjusting the arc radius in the SVG path
# For less rounded corners, reduce the '10,10' values in the arc commands
# For more rounded corners, increase them
# Example with less rounded corners:
less_rounded = """
    M-10,-10
    h20
    a5,5 0 0 1 5,5
    v20
    a5,5 0 0 1 -5,5
    h-20
    a5,5 0 0 1 -5,-5
    v-20
    a5,5 0 0 1 5,-5
    z
"""

# Example with more rounded corners:
more_rounded = """
    M-10,-10
    h20
    a15,15 0 0 1 15,15
    v20
    a15,15 0 0 1 -15,15
    h-20
    a15,15 0 0 1 -15,-15
    v-20
    a15,15 0 0 1 15,-15
    z
"""