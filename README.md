## PIConGPU input templater (PoGit)

Utility to generate the [PIConGPU](https://github.com/ComputationalRadiationPhysics/picongpu) input files using a Pythonic API, simillar as used in the python-based codes (e.g.  [WARP](https://bitbucket.org/berkeleylab/warp), [FBPIC](https://github.com/fbpic/fbpic), [CHIMERA](https://github.com/hightower8083/chimera)/[CHIMERA.CL](https://github.com/hightower8083/chimeraCL)).

This is an early development and its purpose is to search a robust strategy for PIConGPU templating. In future it may merge [PICME](https://github.com/picmi-standard/picmi) project.

Currently the following basic functionality is covered:
- grid-solver class defines and adjusts the simulation domain, solver scheme and parameters, handles the simulation run and diagnostics.
- mupltiple definitions and creation of species of basic (`electron`, `proton`) and generic (`ion`) sorts
- support for native PIConGPU laser implementation
- low-level model of a current-driven laser antenna (to enable multiple lasers)

## Dependencies

PoGit is based on template manager [Mako](https://github.com/sqlalchemy/mako), but also uses [mendeleev](https://bitbucket.org/lukaszmentel/mendeleev), and the standard scientific python tools (scipy and numpy)

## Installation

Clone and install with dependencies:
```sh
git clone https://github.com/hightower8083/PoGit.git
cd PoGit
python setup.py install
```

## Usage

To get an idea of how it works -- clone a PIConGPU example, remove `param` files, execute a PoGit script:
```sh
pic-create $PIC_EXAMPLES/LaserWakefield pogit-test-run
cd pogit-test-run
rm -r include/picongpu/param/* .build/
python example_lwfa.py
```

Script will generate input files at `./include/picongpu/param` and a launcher configuration `./etc/picongpu/run.cfg`. Here is simplest example as input for a case of laser plasma acceleration of electrons:
```python
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
```

This and more detailed examples can be found in this repository. More information on the main classes and default parameters can be found in their documentation. In order to just read it type something like:
```sh
python -c "from pogit.grid import GridSolver as _; help(_)"
python -c "from pogit.particle import Particle as _; help(_)"
```

## Contributing

Everybody interested is greatly welcome to contribute. Many things are to be done: manipulators, filters, diagnoctics etc.
