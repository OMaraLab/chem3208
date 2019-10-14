import nglview as nv
import ipywidgets as widgets
import MDAnalysis as mda

class MolWidget:

    def __init__(self, filename, atom_index=39):
        self.atom_index = atom_index
        self.view = nv.show_file(filename, default=False)
        self.u = mda.Universe(filename)
        self.cutoff = widgets.FloatText(value=0, description='Cutoff (nm):')
        self._n = widgets.Label(value='0')
        self._atom = widgets.Label(value='atoms within cutoff')
        self.natom_label = widgets.HBox(children=[self._n, self._atom])

        self.cutoff.observe(self.update, names='value')

        self.hbox = widgets.HBox(children=[self.cutoff, self.natom_label])
        self.widget = widgets.VBox(children=[self.cutoff, self.natom_label, self.view])
        self.update()
    
    def update(self, *args):
        self.view.representations = self.get_nv_representations()
        self._n.value = str(len(self.radius_atoms)-1)

    @property
    def radiusA(self):
        return self.cutoff.value * 10
    
    @property
    def radius_atoms(self):
        return self.u.select_atoms('around {:f} (index {:d})'.format(self.radiusA, self.atom_index))


    def get_nv_representations(self):
        sele = ','.join(map(str, self.radius_atoms.indices))
        return [
                {'type': 'ball+stick',
                'params': {
                    'sele': 'water',
                    'opacity': 0.1
                }},
                {'type': 'ball+stick',
                'params': {
                    'sele': 'protein',
                    'opacity': 0.3,
                }},
                {'type': 'spacefill',
                'params': {
                    'sele': '@'+str(self.atom_index),
                    'opacity': 1,
                }},
                {'type': 'ball+stick',
                'params': {
                    'sele': '@'+sele,
                    'opacity': 1,
                }},
                
            ]