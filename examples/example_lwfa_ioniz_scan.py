"""
This is an eample of using PoGit to setup and run a series of simulations
(scan) for a LWFA case in electron-proton plasma, with varying doping
of N+5 ions.
"""

from pogit.laser import Laser
from pogit.grid import GridSolver
from pogit.particle import Particle
from pogit.plugins import Plugin
from pogit.writer import WriteAndSubmit

# Sizes of the simulation box and grid
xmax, ymax, zmax = 25e-6, 35e-6, 25e-6
Nx, Ny, Nz = 128, 1024, 128
mpi_decomposition = (1, 2, 1)

# Total number of simulations steps
Nsteps = 6000

# Number of steps between diagnostics
N_diag = 2000

## Laser parameters
ctau = 4e-6                 # Laser duration in meters
a0 = 3.0                    # Laser normalized amplitude
waist = 5.0e-6              # Laser waist in meters
cdelay = 3 * ctau          # Delay of laser centroid in meters

## Plasma parameters
# Base density
n_p = 8e18 * 1e6

# Density profile defined in `codelets/density.py`
density_profile = { 'name': 'Gaussian', 'vacuumCellsY': 100,
         'gasFactor': -1.0, 'gasPower': 4.0,
         'gasCenterLeft': 40e-6, 'gasCenterRight': 60e-6,
         'gasSigmaLeft': 20e-6, 'gasSigmaRight': 80e-6 }

initial_positions = ('Random', 2)

## Creating simulation objects and writing files

gridSolver = GridSolver( xmax, ymax, zmax, Nx, Ny, Nz, Nsteps,
                         mpi_decomposition, movingWindow=True,
                         movePoint=1. )

laser = Laser( a0=a0, ctau=ctau, waist=waist, cdelay=cdelay)

eons = Particle( name='e', species='electron',
                 base_density=n_p, typicalNppc=2*initial_positions[1],
                 density_profile=density_profile,
                 initial_positions=initial_positions )

protons = Particle( name='p', species='proton',
                    density_profile=density_profile,
                    initial_positions=initial_positions )

diags = Plugin( period=N_diag, source='E, e_chargeDensity, e_all' )


for doping_ratio in [0.01, 0.02, 0.03]:
    ions = Particle( name='N5', species='ion',
                     density_profile=density_profile,
                     initial_positions=initial_positions,
                     element='Nitrogen', initial_charge=5,
                     target_species=eons,
                     relative_density=doping_ratio )

    WriteAndSubmit( (eons, protons, ions, gridSolver, laser, diags),
      sim_name=f'ioniz-lwfa-{doping_ratio}', output_path='$PIC_SCRATCH' )
