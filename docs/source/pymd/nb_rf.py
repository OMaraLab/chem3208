import ipywidgets as widgets
import numpy as np
from .base import BaseNonBonded

class NonBondedRF(BaseNonBonded):

    num = 1000

    title = 'Non-bonded potential (Reaction-Field)'

    def __init__(self):
        super().__init__()
        self.cutoff = 0


        self.eps_slider = widgets.FloatSlider(value=1, min=-2, max=2, step=0.1, 
                                         description='epsilon:',
                                         continuous_update=True,
                                         readout=True)
        self.sigma_slider = widgets.FloatSlider(value=1, min=0, max=10, step=0.1, 
                                          description='sigma:',
                                          continuous_update=True,
                                          readout=True)
        self.qa_slider = widgets.FloatSlider(value=1, min=-2, max=2, step=0.1, 
                                          description='qa:',
                                          continuous_update=True,
                                          readout=True)
        self.qb_slider = widgets.FloatSlider(value=1, min=-2, max=2, step=0.1, 
                                           description='qb:',
                                           continuous_update=True,
                                           readout=True)
        self.epsrf_slider = widgets.FloatSlider(value=60, min=-30, max=150, step=0.5, 
                                           description='epsilon (RF):',
                                           continuous_update=True,
                                           readout=True)



        self.eps_slider.observe(self.update, names='value')
        self.sigma_slider.observe(self.update, names='value')
        self.qa_slider.observe(self.update, names='value')
        self.qb_slider.observe(self.update, names='value')
        self.epsrf_slider.observe(self.update, names='value')
        self._init_graph()

        hbox1 = widgets.HBox(children=[self.eps_slider, self.sigma_slider])
        hbox3 = widgets.HBox(children=[self.qa_slider, self.qb_slider])
        self.widget = widgets.VBox(children=[hbox1, hbox3, self.epsrf_slider, self.titlebox, self.g])

    @property
    def y(self):
        rf = self.calculate(self.eps_slider.value, self.sigma_slider.value, 
                              self.qa_slider.value, self.qb_slider.value, 
                              self.cutoff, self.epsrf_slider.value, self.x)
        return np.where(self.x<=self.cutoff, rf, 0)




nb_rf_potential = NonBondedRF()

