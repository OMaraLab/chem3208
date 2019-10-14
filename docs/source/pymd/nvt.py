from ase.md.nvtberendsen import NVTBerendsen
from .nve import NVE


class NVT(NVE, NVTBerendsen):

    name = 'nvt'
    tmp_pdb = '#tmpnvt.pdb'


    
    def __init__(self, filename='2beg_solv_ions.gro', 
                 timestep=0, cutoff=0, temperature=300, tau=0.05):
        super(NVT, self).__init__(filename=filename, timestep=timestep, cutoff=cutoff)
        self.target_temperature = temperature
        self.tau = tau
    
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
        NVTBerendsen.__init__(self, atoms=self.atoms, timestep=self.dt,
                                trajectory=self.traj, loginterval=1,
                                logfile=self._log, temperature=self.target_temperature,
                                taut=self.tau,
                                append_trajectory=False)
        self.update_properties()
    

    def step(self, f=None):
        self.rescale_velocities(self)
        if f is None:
            f = self.atoms.get_forces()
        out = self.next_step(self, f)
        self.update_properties()
        return out
