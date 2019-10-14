import ipywidgets as widgets
from .base import BaseNonBonded

class Coulomb(BaseNonBonded):

    title='Coulomb potential'

    def __init__(self):
        super().__init__()

        self.qa_slider = widgets.FloatSlider(value=1, min=-2, max=2, step=0.1, 
                                         description='qa:',
                                         continuous_update=True,
                                         readout=True)
        self.qb_slider = widgets.FloatSlider(value=1, min=-2, max=2, step=0.1, 
                                          description='qb:',
                                          continuous_update=True,
                                          readout=True)

        self.qa_slider.observe(self.update, names='value')
        self.qb_slider.observe(self.update, names='value')
        self._init_graph()

        hbox1 = widgets.HBox(children=[self.qa_slider, self.qb_slider])
        self.widget = widgets.VBox(children=[hbox1, self.titlebox, self.g])

    @property
    def y(self):
        return self.calculate(self.qa_slider.value, self.qb_slider.value, self.x)

coulomb_potential = Coulomb()

