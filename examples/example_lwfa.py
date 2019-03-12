from pogit.laser import Laser
from pogit.grid import GridSolver
from pogit.particle import Particle
from pogit.writer import WriteSimulationFiles

## Grid and Solver parameters
# Dimensionality
dim = '3d'

# Solver choice and features
solver_type = 'Yee'
J_smoothing = 'Binomial'

# Sizes of the simulation box and grid
xmax, ymax, zmax = 30e-6, 70e-6, 30e-6
Nx, Ny, Nz = 128, 2048, 128

# Number of simulations steps
Nsteps = 6000

# MPI decomposition over devices
mpi_decomp = (1, 2, 1)

## Laser parameters
ctau = 4e-6                 # Laser duration in meters
a0 = 3.0                    # Laser normalized amplitude
waist = 5.0e-6              # Laser waist in meters
cdelay = -3 * ctau          # Delay of laser centroid in meters
iy_antenna = 72             # Position of antenna # (8 cells from absorber)
laser_profile = 'Gaussian'  # laser profile name
polarisation = 'x'          # laser polarisation

## Plasma parameters
# Base density
ne = 8e18 * 1e6

# Density profile defined in `codelets/density.py`
density_profile = { 'type': 'Gaussian', 'vacuumCellsY': 100,
         'gasFactor': -1.0, 'gasPower': 4.0,
         'gasCenterLeft': 40e-6, 'gasCenterRight': 60e-6,
         'gasSigmaLeft': 20e-6, 'gasSigmaRight': 80e-6 }

initial_positions = ('Random', 2)
shape_order = 2
pusher = 'Vay'
current_deposition = 'Esirkepov'

## Creating simulation objects and writing files

gridSolver = GridSolver( xmax, ymax, zmax, Nx, Ny, Nz, Nsteps,
                         decomposition=mpi_decomp, dim=dim,
                         type=solver_type, J_smoothing=J_smoothing,
                         movingWindow=True, movePoint=1)

laser = Laser( a0=a0, ctau=ctau, waist=waist, iy_antenna=iy_antenna,
               cdelay=cdelay, profile=laser_profile, pol=polarisation)

eons = Particle( name='Electrons', type='electron',
                 density_profile=density_profile, base_density=ne,
                 initial_positions=initial_positions, pusher=pusher,
                 current_deposition=current_deposition,
                 typicalNppc=initial_positions[1] )

ions = Particle( name='Protons', type='proton', pusher=pusher,
                 density_profile=density_profile,
                 initial_positions=initial_positions,
                 current_deposition=current_deposition )
# Note: only one species can define `base_density` and `typicalNppc`

WriteSimulationFiles( ( eons, ions, gridSolver, laser ) )
