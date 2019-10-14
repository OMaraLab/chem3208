import ipywidgets as widgets
from .base import BaseNonBonded

class LennardJones(BaseNonBonded):

    num = 1000
    
    title = 'Lennard-Jones potential'

    def __init__(self):
        super(LennardJones, self).__init__()
        self.eps_slider = widgets.FloatSlider(value=1, min=-2, max=2, step=0.1, 
                                         description='epsilon:',
                                         continuous_update=True,
                                         readout=True)
        self.sigma_slider = widgets.FloatSlider(value=1, min=0, max=10, step=0.1, 
                                          description='sigma:',
                                          continuous_update=True,
                                          readout=True)

        self.eps_slider.observe(self.update, names='value')
        self.sigma_slider.observe(self.update, names='value')
        self._init_graph()

        hbox1 = widgets.HBox(children=[self.eps_slider, self.sigma_slider])
        self.widget = widgets.VBox(children=[hbox1, self.titlebox, self.g])

    @property
    def y(self):
        return self.calculate(self.eps_slider.value, self.sigma_slider.value, self.x)
    

lj_potential = LennardJones()

