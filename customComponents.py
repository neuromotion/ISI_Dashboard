
import pandas as pd
import numpy as np
import dash
import plotly.express as px
import plotly.graph_objects as go

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
        x, y = np.meshgrid(np.arange(0, 4), np.arange(0, 8))
        color = 32 * ["gray"]                                                     # init all off
        df = pd.DataFrame({'x': x.ravel(), 'y': y.ravel(), 'color': color})       # 
        df['index'] = df['y'] + 8 * df['x'] + 1                                   # set pin numbers
        df['index'] += PinShift[ElecLoc]                                          # pin index compensation
        df.loc[df['y'] > 3, 'y'] += 1                                             # apply visual shift

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
                marker={'size': 40}))
        fig.update_layout({
            'template': 'simple_white',
            'width': 400,
            'height': 650,
            'showlegend': False,
            'title': ElecLoc,
            'title_x':0.5,
            'title_y':0.9,
            'title_font_size':28
        })
        fig.update_xaxes(mirror=True, showticklabels=False, ticks='')
        fig.update_yaxes(mirror=True, showticklabels=False, ticks='')
    
        # update self 
        self.df = df
        self.fig = fig 

    def update(self,Pins): 
        """
        update the state the electrode array figure 
        inputs: 
            a dictionary with the following fields:
                eleCath 
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
            'eleCath' - list of cathode electrodes
            'eleAno'  - list of cathode electrodes
            'amplitude' - amplitude of stimulation
            'freq' - frequency of stimulation
            'phase' - phase of stimulation
        groupNum - index of the stim group
        """ 
        # layout electrodes and cathodes in rows
        ncols = 4
        eleCath = sgdict['eleCath']
        eleAno  = sgdict['eleAno']

        nrows = int(np.ceil(len(eleCath)/ncols) + np.ceil(len(eleAno)/ncols))
        padding = lambda n: ncols*int(np.ceil(n/ncols)) - n
        eleCathPadded = eleCath + [-1] * padding(len(eleCath))         # pad with -1's for spacing
        eleAnoPadded  = eleAno  + [-1] * padding(len(eleAno ))         # pad with -1's

        colorCath = ['red'] *  len(eleCathPadded)
        colorAno =  ['blue'] * len(eleAnoPadded)

        x, y = np.meshgrid(np.arange(0, 4), np.arange(0, nrows))
        y = nrows -(y + 1) # reverse points along y axis

        df = pd.DataFrame({'x': x.ravel(),
                        'y': y.ravel(),
                        'color':colorCath + colorAno,
                        'label':eleCathPadded + eleAnoPadded})

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
                marker={'size': 40}
            ))

        # annotate amplitude, freq and phase for SG
        afp = (int(sgdict['amplitude']) , int(sgdict['freq']), int(sgdict['phase']))
        fig.add_annotation(
                    xref="paper",
                    yref="paper",
                    align="center",
                    x=0.5,   # on center
                    y=-0.25,  # hand tuned
                    text="<b>Amp=%i, Freq=%i, Phase: %i" %afp,
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

        fig.update_xaxes(mirror=True,ticks="",showticklabels=False)
        fig.update_yaxes(mirror=True,ticks="",showticklabels=False)

        fig.update_xaxes(range=xrange)
        fig.update_yaxes(range=yrange)

        self.fig = fig
