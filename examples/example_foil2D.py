from pogit.laser import Laser
from pogit.grid import GridSolver
from pogit.particle import Particle
from pogit.plugins import Plugin
from pogit.writer import WriteSimulationFiles, WriteAndSubmit

dim = '2d'

# Sizes of the simulation box and grid
xmax, ymax, zmax = 8e-6, 12e-6, 6e-6
Nx, Ny, Nz = 2048, 3072, 1
mpi_decomposition = (2, 1, 1)

# Total number of simulations steps
Nsteps = 40000

# Number of steps between diagnostics
N_diag = 2000

## Laser parameters
ctau = 6e-6                 # Laser duration in meters
a0 = 18.0                    # Laser normalized amplitude
waist = 2.0e-6              # Laser waist in meters
cdelay = 3 * ctau          # Delay of laser centroid in meters
polarisation = 'x'         # laser polarisation
iy_antenna = 72            # Position of antenna # (8 cells from absorber)

## Plasma parameters
# Base density
n_p = 100 * 1.73e21 * 1e6

# Density profile defined in `codelets/density.py`
e_profile = { 'name': 'Gaussian', 'vacuumCellsY': 100,
              'gasFactor': -1.0, 'gasPower': 4.0,
              'gasCenterLeft': 3.5e-6, 'gasCenterRight': 5e-6,
              'gasSigmaLeft': 0.2e-6, 'gasSigmaRight': 0.2e-6 }

p_profile_left = { 'name': 'Gaussian', 'vacuumCellsY': 100,
                   'gasFactor': -1.0, 'gasPower': 4.0,
                   'gasCenterLeft': 3.5e-6, 'gasCenterRight': 3.5e-6,
                   'gasSigmaLeft': 0.2e-6, 'gasSigmaRight': 1e-29 }

p_profile_right = { 'name': 'Gaussian', 'vacuumCellsY': 100,
                    'gasFactor': -1.0, 'gasPower': 4.0,
                    'gasCenterLeft': 5e-6, 'gasCenterRight': 5e-6,
                    'gasSigmaLeft': 1e-29, 'gasSigmaRight': 0.2e-6 }

C_profile = { 'name': 'Gaussian', 'vacuumCellsY': 100,
              'gasFactor': -1.0, 'gasPower': 4.0,
              'gasCenterLeft': 3.5e-6, 'gasCenterRight': 5e-6,
              'gasSigmaLeft': 1e-29, 'gasSigmaRight': 1e-29 }

initial_positions = ('Random', 32)

## Creating simulation objects and writing files

gridSolver = GridSolver( xmax, ymax, zmax, Nx, Ny, Nz, Nsteps,
                         mpi_decomposition, dim=dim )

laser = Laser( a0=a0, ctau=ctau, waist=waist, cdelay=cdelay,
               iy_antenna=iy_antenna, pol=polarisation)

eons = Particle( name='e', species='electron',
                 base_density=n_p, typicalNppc=2*initial_positions[1],
                 density_profile=e_profile,
                 initial_positions=initial_positions )

protons = Particle( name='p', species='proton',
                    density_profile=[ p_profile_right, p_profile_left ],
                    initial_positions=initial_positions )

carbon = Particle( name='C6', species='ion', element='Carbon',
                   initial_charge=6, density_profile=C_profile,
                   target_species=eons, relative_density=1./6,
                   initial_positions=initial_positions )

diags = Plugin( period=N_diag, source='E, e_chargeDensity, ' + \
                'p_chargeDensity, p_chargeDensity, p_all' )

WriteAndSubmit( ( eons, carbon, protons, gridSolver, laser, diags),
    sim_name=f'foil2d_run', output_path='$PIC_SCRATCH' )
