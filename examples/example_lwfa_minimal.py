from pogit.laser import Laser
from pogit.grid import GridSolver
from pogit.particle import Particle
from pogit.writer import WriteSimulationFiles

# Sizes of the simulation box and grid
xmax, ymax, zmax = 30e-6, 70e-6, 30e-6
Nx, Ny, Nz = 128, 2048, 128

# Number of simulations steps
Nsteps = 6000

## Laser parameters
ctau = 4e-6                 # Laser duration in meters
a0 = 3.0                    # Laser normalized amplitude
waist = 5.0e-6              # Laser waist in meters
cdelay = -3 * ctau          # Delay of laser centroid in meters
iy_antenna = 72             # Position of antenna # (8 cells from absorber)

## Plasma
ne = 8e18 * 1e6
density_profile = { 'type': 'Gaussian', 'vacuumCellsY': 100,
         'gasFactor': -1.0, 'gasPower': 4.0,
         'gasCenterLeft': 40e-6, 'gasCenterRight': 60e-6,
         'gasSigmaLeft': 20e-6, 'gasSigmaRight': 80e-6 }

## Construct simulation
gridSolver = GridSolver( xmax, ymax, zmax, Nx, Ny, Nz,
                         Nsteps, movingWindow=True)

laser = Laser( a0=a0, ctau=ctau, waist=waist, cdelay=cdelay,
               iy_antenna=iy_antenna )

eons = Particle( name='Electrons', type='electron', base_density=ne,
                 density_profile=density_profile, typicalNppc=3 )

WriteSimulationFiles( (eons, gridSolver, laser) )
