## PIConGPU input templater (PoGit)

Utility to generate the [PIConGPU](https://github.com/ComputationalRadiationPhysics/picongpu) input files using a Pythonic API, simillar as used in the python-based codes (e.g.  [WARP](https://bitbucket.org/berkeleylab/warp), [FBPIC](https://github.com/fbpic/fbpic), [CHIMERA](https://github.com/hightower8083/chimera)/[CHIMERA.CL](https://github.com/hightower8083/chimeraCL)).

## Notes

- This is a very-very early and raw version
- Purpose of this development is to search a robust strategy for PIConGPU templating
- current release covers only basic demonstrational functionality
- May contain bugs and memory non-optimal operations
- Laser is implemented via a current-driven antenna, defined as a background field (native laser to be added)

## Installation

Clone and install with dependances ([Mako](https://github.com/sqlalchemy/mako)) via:
```
python setup.py install
```

## Using

To get an idea of how it works clone some PIConGPU example, remove all `param` filed, and then create and execute a PoGit script in the simulation folder:
```bash
pic-create $PIC_EXAMPLES/LaserWakefield pogit-test-run
cd pogit-test-run
rm -r include/picongpu/param/* .build/
python example_lwfa.py
```
Code will generate input and configuration files, and put them to `./include/picongpu/param` and `./etc/picongpu`.

Here is simplset example of the input file:
```python
from pogit.laser import Laser
from pogit.grid import GridSolver
from pogit.particle import Particle
from pogit.writer import WriteSimulationFiles

# Sizes of the simulation box and grid
xmax, ymax, zmax = 30e-6, 70e-6, 30e-6
Nx, Ny, Nz = 128, 2048, 128

# Number of simulations steps
Nsteps = 8000

## Laser parameters
ctau = 4e-6                 # Laser duration in meters
a0 = 3.0                    # Laser normalized amplitude
waist = 5.0e-6              # Laser waist in meters
y0 = -2.5 * ctau            # Initial position of laser centroid
y_antenna = 3e-6            # Position of antenna in meters
i_center = (Nx//2, Nz//2)   # Transverse position of antenna in cells

## Plasma
ne = 8e18 * 1e6
density_profile = { 'type': 'Gaussian', 'vacuumCellsY': 100,
         'gasFactor': -1.0, 'gasPower': 4.0,
         'gasCenterLeft': 40e-6, 'gasCenterRight': 60e-6,
         'gasSigmaLeft': 20e-6, 'gasSigmaRight': 80e-6 }

## Construct simulation
gridSolver = GridSolver( xmax, ymax, zmax, Nx, Ny, Nz,
                         Nsteps, movingWindow=True)

laser = Laser( a0=a0, ctau=ctau, waist=waist, y0=y0,
               y_antenna=y_antenna, i_center=(Nx//2, Nz//2), )

eons = Particle( name='Electrons', type='electron', base_density=ne,
                 density_profile=density_profile, typicalNppc=3 )

WriteSimulationFiles( (eons, gridSolver, laser) )
```

This and more detailed examples can be found in this repository.

## Contributing

Everybody interested is greatly welcome to contribute. If this one is to become a good API, there is a huge work to be done (manipulators, filters, diagnoctics etc).
