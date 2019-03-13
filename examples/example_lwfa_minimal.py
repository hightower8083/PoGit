from pogit.laser import Laser
from pogit.grid import GridSolver
from pogit.particle import Particle
from pogit.writer import WriteSimulationFiles

# Sizes of the simulation box and grid
xmax, ymax, zmax = 25e-6, 35e-6, 25e-6
Nx, Ny, Nz = 128, 1024, 128

# Total number of simulations steps
Nsteps = 6000

# Number of steps between diagnostics
N_diag = 2000

## Laser parameters
ctau = 4e-6                 # Laser duration in meters
a0 = 3.0                    # Laser normalized amplitude
waist = 5.0e-6              # Laser waist in meters
cdelay = 3 * ctau           # Delay of laser centroid in meters

## Plasma
n_e = 8e18 * 1e6
initial_positions = ('Random', 2)
density_profile = { 'type': 'Gaussian', 'vacuumCellsY': 100,
         'gasFactor': -1.0, 'gasPower': 4.0,
         'gasCenterLeft': 40e-6, 'gasCenterRight': 60e-6,
         'gasSigmaLeft': 20e-6, 'gasSigmaRight': 80e-6 }

## Construct simulation
gridSolver = GridSolver( xmax, ymax, zmax, Nx, Ny, Nz,
                         Nsteps, N_diag, movingWindow=True)

laser = Laser( a0=a0, ctau=ctau, waist=waist, cdelay=cdelay )

eons = Particle( name='Electrons', species='electron',
                 base_density=n_e, typicalNppc=initial_positions[1],
                 initial_positions=initial_positions,
                 density_profile=density_profile )

WriteSimulationFiles( (eons, gridSolver, laser) )
