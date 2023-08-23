
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
            'showlegend': False
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
       
