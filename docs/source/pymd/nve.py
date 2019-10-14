import ase
from ase.md.verlet import VelocityVerlet
import ase.units as units
import numpy as np
import pandas as pd
import os
import nglview as nv

from ase.calculators.emt import EMT
from ase.io import Trajectory

def dummy(self, *args):
    pass

class NVE(VelocityVerlet):

    name = 'nve'
    tmp_pdb = '#tmp.pdb'

    @property
    def trajectory(self):
        return Trajectory(self.traj)

    @property
    def traj(self):
        return self.name + '.traj'
    
    @property
    def _log(self):
        return self.name + '.log'
    
    @property
    def pdb(self):
        return self.name + '.pdb'
    
    def __init__(self, filename='2beg_solv_ions.gro', 
                 timestep=0, cutoff=0, name=None):
        if name is None:
            name = type(self).name
        self.name = name
        self.atoms = ase.io.read(filename)
#         self.atoms.set_calculator(LennardJones(rc=cutoff))
        self.atoms.set_calculator(EMT(rc=cutoff))
        self.dt = timestep
        self.masses = self.atoms.get_masses()[:, np.newaxis]
        self.dct = {'Temperature': [], 'Pressure': [],
                    'Kinetic energy': [], 'Potential energy': [],
                    'Total energy': [], 'Time': []}
    
    @property
    def pressures(self):
        return self.dct['Pressure']
    
    @property
    def temperatures(self):
        return self.dct['Temperature']

    def get_properties(self):
        df = pd.DataFrame(self.dct)
        df = df.rename(columns={'Temperature': 'Temperature (K)',
                                'Pressure': 'Pressure (bar)',
                                'Kinetic energy': 'Kinetic energy (eV)',
                                'Potential energy': 'Potential energy (eV)',
                                'Total energy': 'Total energy (eV)',
                                'Time': 'Time (fs)'})
        df.to_csv(self.name + '.csv')
        return df
    
    @property
    def traj_view(self):
        return nv.show_asetraj(self.trajectory)
    
    @property
    def atom_view(self):
        return nv.show_ase(self.atoms)#, gui=True)

    def set_initial_velocities(self, distribution, energy):
        distribution(self.atoms, energy)
        try:
            os.remove(self.traj)
        except:
            pass
        try:
            os.remove(self._log)
        except:
            pass
        VelocityVerlet.__init__(self, atoms=self.atoms, timestep=self.dt,
                                trajectory=self.traj, loginterval=1,
                                logfile=self._log,
                                append_trajectory=False)
        self.update_properties()
    
    def update_properties(self):
        self.dct['Temperature'].append(self.atoms.get_temperature())
        self.dct['Pressure'].append(self.get_pressure())
        epot = self.atoms.get_potential_energy()
        ekin = self.atoms.get_kinetic_energy()
        self.dct['Potential energy'].append(epot)
        self.dct['Kinetic energy'].append(ekin)
        self.dct['Total energy'].append(epot+ekin)
        self.dct['Time'].append(len(self.dct['Time'])*self.dt)

    
    def set_atom_velocities(self, velocities):
        self.atoms.set_momenta(self.masses * velocities)
    
    def get_pressure(self):
        stress = self.atoms.get_stress(voigt=False)
        bar = -stress.trace()/3 
        # pa = bar * 1e-5/units.Pascal
        return bar
    
    def step(self, f=None):
        if f is None:
            f = self.atoms.get_forces()
        out = self.next_step(self, f)
        self.update_properties()
        return out

    def print_energy(self):
        a = self.atoms
        epot = a.get_potential_energy() / len(a)
        ekin = a.get_kinetic_energy() / len(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
            'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))

    def run(self, nsteps):
        super().run(nsteps)
        self.traj_to_pdb()

    def traj_to_pdb(self):
        traj = self.trajectory
        cont = ''
        for i in range(len(traj)):
            with open(self.tmp_pdb, 'w') as f:
                traj[i].write(f.name)
            with open(self.tmp_pdb, 'r') as f:
                cont += f.read()
        os.remove(self.tmp_pdb)
        
        with open(self.pdb, 'w') as f:
            f.write(cont)
