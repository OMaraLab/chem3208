import ipywidgets as widgets
import numpy as np

import plotly.graph_objects as go

def lj(*args):
    return args[-1]

class BaseNonBonded:

    num = 1000
    title = ''
    ymin = -10
    ymax = 15

    def __init__(self):
        self.calculate = lj
        self.x = np.linspace(0.01, 10.01, num=self.num)

        self.xtitle = widgets.Text(description='x-axis title', continuous_update=False)
        self.ytitle = widgets.Text(description='y-axis title', continuous_update=False)

        self.xtitle.observe(self.update, names='value')
        self.ytitle.observe(self.update, names='value')

        self.titlebox = widgets.HBox(children=[self.xtitle, self.ytitle])

    @property
    def y(self):
        return self.calculate(self.x)

    def _init_graph(self):
        trace0 = go.Scatter(x=self.x, y=[0]*self.num, mode='lines')
        trace1 = go.Scatter(x=self.x, y=self.y, mode='lines')

        self.g = go.FigureWidget(data=[trace0, trace1],
                                 layout=go.Layout(title={'text': self.title}))
        self.g.update_yaxes(range=[self.ymin, self.ymax])
        self.g.update_layout(showlegend=False)
    

    def update(self, *args):
        with self.g.batch_update():
            self.g.data[1].y = self.y
            self.g.layout.xaxis.title = self.xtitle.value
            self.g.layout.yaxis.title = self.ytitle.value
