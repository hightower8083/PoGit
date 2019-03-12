from pogit.laser import Laser
from pogit.grid import GridSolver
from pogit.particle import Particle
from pogit.writer import WriteSimulationFiles

## Grid and Solver parameters
# Dimensionality
dim = '3d'

# Solver choice and features
solver_type = 'Lehe'
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

## Plasma parameters
# Base density
ne = 1e18 * 1e6

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
                         movingWindow=True, movePoint=1.)

laser = Laser( a0=a0, ctau=ctau, waist=waist, iy_antenna=iy_antenna,
               cdelay=cdelay)

eons = Particle( name='Electrons', type='electron',
                 initial_positions=initial_positions, pusher=pusher,
                 current_deposition=current_deposition,
                 shape_order=shape_order)

ions = Particle( name='Ions', type='generic_ionizable',
                 density_profile=density_profile, base_density=ne,
                 element='Nitrogen', initial_charge=5,
                 mass_ratio=1836.152672*14.007, charge_ratio=-7,
                 target_species=eons, ionizer_polarization='Lin',
                 initial_positions=initial_positions,
                 pusher=pusher, shape_order=shape_order,
                 current_deposition=current_deposition,
                 typicalNppc = initial_positions[1]*3 )
# Note: only one species can define `base_density` and `typicalNppc`

WriteSimulationFiles( ( eons, ions, gridSolver, laser ) )
