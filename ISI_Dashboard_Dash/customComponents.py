
#%% 
import pandas as pd
import numpy as np
import dash
import plotly.express as px
import plotly.graph_objects as go

# class ElectrodeArray():
#     def __init__(self,ElecLoc="Caudal"):
#         self.df = {}
#         self.fig = []
#         self.build(ElecLoc)
        
#     def build(self,ElecLoc="Caudal"):
#         """
#         constructs an empty electrode array figure
#         """
#         # initialize plotting dataframe
#         PinShift = {"Rostral":128 , "Caudal":0}
#         x, y = np.meshgrid(np.arange(0, 4), np.arange(0, 8))                      # x and you are coordinates
#         color = 32 * ["gray"]                                                     # init all off
#         df = pd.DataFrame({'x': x.ravel(), 'y': y.ravel(), 'color': color})       # 
#         df['index'] = df['y'] + 8 * df['x'] + 1                                   # set pin numbers
#         df['index'] += PinShift[ElecLoc]                                          # pin index compensation
#         df.loc[df['y'] > 3, 'y'] += 1                                             # apply visual shift

#     # scatter plot dataframe 
#         fig = go.Figure()
#         fig.add_trace(
#             go.Scatter(
#                 x = df['x'].to_list(), 
#                 y = df['y'].to_list(), 
#                 text = df['index'].to_list(), 
#                 textfont=dict(
#                     family="sans serif",
#                     size=18,
#                     color="White"
#                 ),
#                 marker_color=df['color'],
#                 mode='markers+text',
#                 # marker={'size': 40}))
#         fig.update_layout({
#             'template': 'simple_white',
#             'width': 400,
#             'height': 650,
#             'showlegend': False,
#             'title': ElecLoc,
#             'title_x':0.5,
#             'title_y':0.9,
#             'title_font_size':28
#         })
#         fig.update_xaxes(mirror=True, showticklabels=False, ticks='')
#         fig.update_yaxes(mirror=True, showticklabels=False, ticks='')
    
#         # update self 
#         self.df = df
#         self.fig = fig 

#     def update(self,Pins): 
#         """
#         update the state the electrode array figure 
#         inputs: 
#             a dictionary with the following fields:
#                 elecCath 
#                 elecAno
#                 Gnd
#                 Ref
#         """
#         EleGroupsNames = ['elecCath','elecAno','Gnd','Ref']
#         EleGroupColors = {'elecCath':'red','elecAno':'blue','Gnd':'green','Ref':'purple'}
#         self.df['color'] = 'gray' # blank the electrodes
        
#         # update df with proper colors
#         for groupName in Pins: 
#             if groupName in EleGroupsNames:
#                 self.df.loc[self.df['index'].isin(Pins[groupName]),'color'] = EleGroupColors[groupName]
        
#        # redraw: 
#         self.fig.data[0]['marker']['color'] = self.df['color']




class ElectrodeArray():
    def __init__(self,ElecLoc="Caudal"):
        self.df = {}
        self.fig = []
        self.build(ElecLoc)
        
    def build(self,ElecLoc="Caudal"):
        """
        constructs an empty electrode array figure
        """
        # initialize plotting dataframe
        PinShift = {"Rostral":128 , "Caudal":0}
        x, y = np.meshgrid(np.arange(0, 4), np.arange(0, 8))                      # x and you are coordinates
        color = 32 * ["gray"]                                                     # init all off
        df = pd.DataFrame({'x': x.ravel(), 'y': y.ravel(), 'color': color})       # 
        df['index'] = df['y'] + 8 * df['x'] + 1                                   # set pin numbers
        df['index'] += PinShift[ElecLoc]                                          # pin index compensation
        df.loc[df['index'].between(9+PinShift[ElecLoc], 24+PinShift[ElecLoc], inclusive='both'), 'y'] += .5  # shift inner rows up in y

    # scatter plot dataframe 
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x = df['x'].to_list(), 
                y = df['y'].to_list(), 
                text = df['index'].to_list(), 
                textfont=dict(
                    family="sans serif",
                    size=18,
                    color="White"
                ),
                marker_color=df['color'],
                mode='markers+text',
                marker={'size': 40,'symbol':'square'}))
        fig.update_layout({
            'template': 'simple_white',
            # 'width': 250,
            'width': 350,
            # 'height': 650,
            'height': 1000,
            # 'height': 650 if ElecLoc=="Rostral" else 650*2,
            'showlegend': False,
            # 'title': ElecLoc,
            # 'title_x':0.5,
            # 'title_y':0.9,
            # 'title_font_size':28
        })

        # First get your plot's x and y ranges
        x_min = min(fig.data[0].x)
        x_max = max(fig.data[0].x)
        y_min = min(fig.data[0].y)
        y_max = max(fig.data[0].y)
        
        xpad = 2
        ypad = 4
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            # xaxis=dict(domain=[0.0, 1.0]),  # Plot takes up 60% of width
            # yaxis=dict(domain=[0.0, 1.0]),   # Plot takes up 60% of height
            xaxis=dict(range=[x_min-xpad, x_max+xpad]),
            yaxis=dict(range=[y_min-ypad, y_max+1])
        )
        fig.update_xaxes(mirror=True, showticklabels=False,showline=False,ticks='')
        fig.update_yaxes(mirror=True, showticklabels=False,showline=False,ticks='')

        #add background for swag points
        # img_width = 400
        # img_height = 650 if ElecLoc=="Rostral" else 650*1.2
        # img_width = 4
        # img_height = 8
        # fig.add_layout_image(
        #     x=0,
        #     sizex=img_width,
        #     y=0,
        #     sizey=img_height,
        #     xref="x",
        #     yref="y",
        #     opacity=1.0,
        #     layer="below",
        #     source="./svgs/paddleBackground.png"
        # ) 

        # fig.add_layout_image(
        #     dict(
        #         source="./svgs/paddleBackground.png",
        #         x=x_max,
        #         y=y_max,
        #         sizex=x_max - x_min,
        #         sizey=y_max -y_min,
        #         xref="x",
        #         yref="y",
        #         opacity=1.0,
        #         layer="below",
        #     )
        # )
        fig.add_layout_image(
            dict(
                source="/assets/paddleBackground.png",
                x=(x_min + x_max)/2,  # Center x-coordinate
                y=(y_min + y_max)/2 - 2.2,   # Center y-coordinate
                sizex=(x_max-x_min)+ 2,  # Width in data coordinates
                # sizey=(y_min + y_max) +10 ,  # Height in data coordinates
                sizey= (y_max - y_min) + 6,  # make it really big so that x drives size
                # sizey=   # make it really big so that x drives size
                xref="x",
                yref="y",
                xanchor="center",  # Center the image horizontally
                yanchor="middle",  # Center the image vertically
                sizing="stretch",
                # sizing="contain",  # Maintains aspect ratio
                layer="below"
            )
        )



        # fig.add_layout_image(
        #     dict(
        #         source="./svgs/paddleBackground.png",
        #         x=.5,
        #         y=.35,
        #         sizex=1.5,
        #         sizey=1.5,
        #         xref="paper",
        #         yref="paper",
        #         xanchor="center",
        #         yanchor="middle",
        #         opacity=1.0,
        #         layer="below",
        #     )
        # )

    
        # update self 
        self.df = df
        self.fig = fig 

    def update(self,Pins): 
        """
        update the state the electrode array figure 
        inputs: 
            a dictionary with the following fields:
                elecCath 
                elecAno
                Gnd
                Ref
        """
        EleGroupsNames = ['elecCath','elecAno','Gnd','Ref']
        EleGroupColors = {'elecCath':'red','elecAno':'blue','Gnd':'green','Ref':'purple'}
        self.df['color'] = 'gray' # blank the electrodes
        
        # update df with proper colors
        for groupName in Pins: 
            if groupName in EleGroupsNames:
                self.df.loc[self.df['index'].isin(Pins[groupName]),'color'] = EleGroupColors[groupName]
        
       # redraw: 
        self.fig.data[0]['marker']['color'] = self.df['color']


class backImage():
    def __init__(self):
        self.build()
        self.fig
        
    def build(self):
        """
        constructs an empty electrode array figure
        """
        # scatter plot dataframe 
        fig = go.Figure()
        fig.update_layout({
            'template': 'simple_white',
            'width': 1000,
            # 'height': 650*2,
            'height': 1000,
            # 'height': 650 if ElecLoc=="Rostral" else 650*2,
            'showlegend': False,
            # 'title': ElecLoc,
            # 'title_x':0.5,
            # 'title_y':0.9,
            # 'title_font_size':28
        })
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            # xaxis=dict(domain=[0.0, 1.0]),  # Plot takes up 60% of width
            # yaxis=dict(domain=[0.0, 1.0]),   # Plot takes up 60% of height
            # xaxis=dict(range=[x_min-xpad, x_max+xpad]),
            # yaxis=dict(range=[y_min-ypad, y_max+1])
        )
        fig.update_xaxes(mirror=True, showticklabels=False,showline=False,ticks='')
        fig.update_yaxes(mirror=True, showticklabels=False,showline=False,ticks='')

        # fig.add_layout_image(
        #     dict(
        #         source="/assets/paddleBackground.png",
        #         x=0
        #         y=0
        #         sizex=1
        #         sizey= 1
        #         xref="paper",
        #         yref="y",
        #         xanchor="center",  # Center the image horizontally
        #         yanchor="middle",  # Center the image vertically
        #         sizing="stretch",
        #         # sizing="contain",  # Maintains aspect ratio
        #         layer="below"
        #     )
        # )



        fig.add_layout_image(
            dict(
                source="/assets/backDrawing.png",
                x=.5,
                y=.35,
                sizex=1.5,
                sizey=1.5,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="middle",
                opacity=1.0,
                layer="below",
            )
        )
        self.fig = fig

#%%
import pandas as pd
import numpy as np
import dash
import plotly.express as px
import plotly.graph_objects as go


class StimGroup():
    def __init__(self):
        self.df = {}
        self.fig = []
        self.build()

    def build(self):
        fig = go.Figure()
        fig.update_layout({
            'template': 'simple_white',
            'width': 400,
            'height': 400,
            'showlegend': False
        })
        fig.update_xaxes(mirror=True, showticklabels=False, ticks='')
        fig.update_yaxes(mirror=True, showticklabels=False, ticks='')

        # update self 
        self.fig = fig 
        
    def update(self,sgdict,groupNum):
        """
        input:
        stim group dictionary with fields: 
            'elecCath' - list of cathode electrodes
            'elecAno'  - list of cathode electrodes
            'amplitude' - amplitude of stimulation
            'freq' - frequency of stimulation
            'phase' - phase of stimulation
        groupNum - index of the stim group
        """ 
        # layout electrodes and cathodes in rows
        ncols = 4
        elecCath = sgdict['elecCath']
        elecAno  = sgdict['elecAno']

        nrows = int(np.ceil(len(elecCath)/ncols) + np.ceil(len(elecAno)/ncols))
        padding = lambda n: ncols*int(np.ceil(n/ncols)) - n
        elecCathPadded = elecCath + [-1] * padding(len(elecCath))         # pad with -1's for spacing
        elecAnoPadded  = elecAno  + [-1] * padding(len(elecAno))         # pad with -1's

        colorCath = ['red'] *  len(elecCathPadded)
        colorAno =  ['blue'] * len(elecAnoPadded)

        x, y = np.meshgrid(np.arange(0, 4), np.arange(0, nrows))
        y = nrows -(y + 1) # reverse points along y axis

        df = pd.DataFrame({'x': x.ravel(),
                        'y': y.ravel(),
                        'color':colorCath + colorAno,
                        'label':elecCathPadded + elecAnoPadded})

        # pop the rows with -1 padding, everything will be properly aligned
        df = df.loc[~df['label'].isin([-1])]

        # plot the points
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x = df['x'].to_list(), 
                y = df['y'].to_list(), 
                text = df['label'].to_list(), 
                textfont=dict(
                    family="sans serif",
                    size=18,
                    color="White"
                ),
                marker_color=df['color'],
                mode='markers+text',
                marker={'size': 40,'symbol':'square'}
            ))

        # annotate amplitude, freq and phase for SG
        afp = (int(sgdict['amp']) , int(sgdict['freq']), int(sgdict['pulseWidth']))
        fig.add_annotation(
                    xref="paper",
                    yref="paper",
                    align="center",
                    x=0.5,   # on center
                    y=-0.25,  # hand tuned
                    text="<b>Amp=%i, Freq=%i, PW: %i" %afp,
                    showarrow=False,
                    font=dict(
                        size=18,
                    ),
                )


        # make figure parametric based on contents:
        pixelsPerXunit = 50        # [pixels/unit]
        pixelsPerYunit = 50        # [pixels/unit]

        axisMargin = .5             # [units]
        xrange = [0-axisMargin, (ncols-1)+axisMargin] 
        yrange = [0-axisMargin, (nrows-1)+axisMargin]

        xAxisWidth  = pixelsPerXunit * (xrange[1] - xrange[0])
        yAxisHeight = pixelsPerYunit * (yrange[1] - yrange[0])

        margins = dict(b=80,t=100,l=80,r=80)
        figWidth  = margins['r'] + margins['l'] + xAxisWidth
        figHeight = margins['t'] + margins['b'] + yAxisHeight

        # update figure layout
        fig.update_layout({
                    'margin_autoexpand':False,
                    'template': 'simple_white',
                    'width':figWidth,
                    'height':figHeight,
                    'showlegend': False,
                    'title':'Stim Group %i' %groupNum,
                    'title_x':0.5,
                    'title_y':0.83,
                    'title_font_size':24,
                    'margin':margins
                })

        fig.update_xaxes(mirror=True,ticks="",showticklabels=False,showline=False)
        fig.update_yaxes(mirror=True,ticks="",showticklabels=False,showline=False)

        fig.update_xaxes(range=xrange)
        fig.update_yaxes(range=yrange)

        self.fig = fig


# sgdict1 = {
#     'elecCath':[1,14,23],
#     'elecAno':[2,15,24],
#     'amp':150,
#     'freq':130,
#     'pulseWidth':50,
# }

# sg = StimGroup()
# sg.update(sgdict1,1)
# sg.fig.show()
    
import plotly.graph_objs as go
import numpy as np
from collections import deque

class stimScope():
    """
    provides a small scope to see when the last stim occured
    """
    def __init__(self):
        self.stimFlag = False
        self.queLen = 50
        self.stims = deque(maxlen=self.queLen)
        for i in range(self.queLen):
            self.stims.append(0)
        self.fig = None
        self.build()


    def build(self):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=list(range(self.queLen)),
                y=list(self.stims),
                marker_color='blue',
                mode='lines+markers',
                marker={'size': 5},
                line=dict(shape='hv')
            )
        )

        fig.update_layout({
            'template': 'simple_white',
            'title':'Stim Scope',
            'width': 400,
            'height': 300,
            'showlegend': False,
            'margin':dict(l=0, r=0, t=0, b=0),
        })

        fig.update_layout(
            title={
                'text': 'Stim Scope',
                'y': 0.95,  # Adjust vertical position
                'x': 0.5,  # Adjust horizontal position
                'xanchor': 'center',  # Anchor horizontally in the middle
                'yanchor': 'top',  # Anchor vertically at the top
                'font': {'size': 20, 'color': 'black'}  # Customize font
            }
        )

        fig.update_xaxes(mirror=True, showticklabels=False,showline=False,ticks='')
        fig.update_yaxes(mirror=True, showticklabels=False,showline=False,ticks='')
        
        self.fig = fig


    def stimDetected(self):
        """
        when stim happens call this function externally to register it 
        in the scope application
        """
        self.StimFlag = True

    def update(self): 
        """
        This is called at 5Hz by the timer interrupt
        """
        #pole stim flag
        if self.stimFlag:
            self.stims.append(1)
            self.stimFlag = False
        else:
            self.stims.append(0)

        # update figure with new data. 
        self.fig.data[0]['y'] = list(self.stims)




# %%
