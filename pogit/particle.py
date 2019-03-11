from mako.template import Template
import numpy as np
from scipy.constants import c

from .codelets.particle import StartPosition, Manipulators
from .codelets.speciesDefinition import speciesDefinition
from .codelets.speciesInitialization import CreateDensity, SetIonCharge
from .codelets.density import densityProfile
from .codelets.species import speciesNumericalParam

class Particle:
    """
    Class that contains parameters of the particle species
    Main attributes
    ---------------
    List of `templates`, which are to be rendered in the
    following files:
        include/picongpu/param/species.param
        include/picongpu/param/speciesDefinition.param
        include/picongpu/param/particle.param
        include/picongpu/param/speciesInitialization.param
        include/picongpu/param/density.param
    """
    def __init__( self, name, type,
                  initial_positions=('Random', 3),
                  typicalNppc=None, density_profile=None,
                  base_density=None, relative_density=1.0,
                  element='Hydrogen', initial_charge=0,
                  mass_ratio=1836.152672, charge_ratio=-1,
                  target_species=None, ionizer_polarisation='Circ',
                  initial_temperature=None,
                  shape_order=1, pusher='Boris',
                  current_deposition='Esirkepov' ):

        """
        Initialize the Particle object
        Parameters
        ----------
        name : string
            Name of the particle species

        type : string
            Type of the species. Presently supported types:
                'electron'
                'proton'
                'generic_ionizable'

        initial_positions : list
            Method to initialize particles in cell. First element
            is a string, which can be:
                'Ordered' : ordered positions with numbers of particles
                            per direction defined by a tuple of integers
                            (NppcX,NppcX,NppcZ)
                'Random': random positions in cell, with total number
                          defined as an integer Nppc

        typicalNppc : integer
            `Typical` total number of particles per cell used for internal
            PIConGPU normalization. Should account for all species, and be
            defined only for the one of them.

        density_profile : dictionary
            Parameters for the density profile defined as a codelet
            (see example)

        base_density : float (1/m^3)
            Base value of number density used for normalization of
            profile functors

        relative_density : float
            Normalisation density relative to the base_density

        element : string
            Name of the element from periodic table

        initial_charge : integer
            Initial charge state of the species

        mass_ratio : float (in elementary mass)
            Mass of the species in units of electron mass

        charge_ratio : float
            Total charge of the species in units of electron charge

        target_species : Particle object
            Species to which ionized electrons are attributed

        ionizer_polarization: string
            Polarization of ionizing radiation, 'Circ' or 'Lin'

        initial_temperature : float
            Initial temperature of the species in keV

        shape_order : integer
            Order of particle interpolation shape.
            Can be 1, 2, 3 or 4

        pusher : string
            Particle pusher method. Can be:
                "Boris": standard pusher (default)
                "Vay": better suited relativistic boris pusher
                "ReducedLandauLifshitz": 4th order RungeKutta pusher with
                                         classical radiation reaction
                "Free": free propagation
                "Photon": propagate with c along momentum
                "Probe": Probe particles that interpolate E & B
                "Axel": a pusher developed at HZDR during 2011 (testing)

        current_deposition : string
            Sheme of current deposition. Can be:
                "Esirkepov" : charge conservative deposition (1st to 4th order)
                "VillaBune": (1st order)
                "EmZ": (1st to 4th order)
                "ZigZag": (1st to 4th order)
        """
        self.name = name

        params = {}
        params['name'] = name
        params['type'] = type
        params['ParticleShape'] = {1: "CIC",
                                   2: "TSC",
                                   3: "PCS",
                                   4: "P4S"}[shape_order]

        params['CurrentSolver'] =  current_deposition
        params['ParticlePusher'] = pusher
        params['Temperature'] = initial_temperature

        if initial_positions[0] == 'Ordered':
            params['NppcX'] = initial_positions[1][0]
            params['NppcY'] = initial_positions[1][1]
            params['NppcZ'] = initial_positions[1][2]
        elif initial_positions[0] == 'Random':
            params['Nppc'] = initial_positions[1]

        if typicalNppc is None:
            params['TYPICAL_PARTICLES_PER_CELL'] = np.prod(initial_positions[1])
        else:
            params['TYPICAL_PARTICLES_PER_CELL'] = typicalNppc

        params['DensityRatio'] = relative_density

        if base_density is not None:
            params["BASE_DENSITY"] = base_density

        if type=='generic_ionizable':
            params["Element"] = element
            params["TargetSpeciesName"] = target_species.name
            params["InitialCharge"] = initial_charge
            params["pol"] = laser_polarisation
            params["MassRatio"] = mass_ratio
            params["ChargeRatio"] = charge_ratio

        # Main generic parameters
        template_species = {}
        template_species['filename'] = 'species.template'
        template_species['AppendableArgs'] = {}
        template_species['AppendableArgs']['speciesNumericalParam']=\
            Template(speciesNumericalParam).render(**params)

        # particular species definition:
        template_speciesDefinition = {}
        template_speciesDefinition['filename'] = 'speciesDefinition.template'
        template_speciesDefinition['AppendableArgs'] = {}
        template_speciesDefinition['AppendableArgs']['SpeciesDefinition'] = \
            Template(speciesDefinition[type]).render(**params)

        template_speciesDefinition['CommaAppendableArgs'] = {}
        template_speciesDefinition['CommaAppendableArgs']\
            ['SpeciesRuntimeName'] = 'PIC_' + name

        # Initialization parameters
        template_particle = {}
        template_particle['filename'] = 'particle.template'
        if typicalNppc is not None:
            template_particle['MainArgs'] = params

        template_particle['AppendableArgs'] = {}
        template_particle['AppendableArgs']['StartPosition'] = Template( \
            StartPosition[initial_positions[0]] ).render(**params)

        manipulator_list = []

        if type=='generic_ionizable':
            manipulator_list.append( Template( Manipulators['SetIonCharge'] )\
                .render(**params) )

        if initial_temperature is not None:
            manipulator_list.append( Template( Manipulators['Temperature'])\
                .render(**params) )

        template_particle['AppendableArgs']['Manipulators'] = \
            "\n".join(manipulator_list)

        # Initialization procedure
        template_speciesInitialization = {}
        template_speciesInitialization['filename'] = \
            'speciesInitialization.template'

        template_speciesInitialization['CommaAppendableArgs'] = {}

        createManipulate_list = []
        if density_profile is not None:
            createManipulate_list.append( Template(CreateDensity).render(**params))

        if type=='generic_ionizable':
            createManipulate_list.append( Template(SetIonCharge).render(**params))

        if len(createManipulate_list) != 0:
            template_speciesInitialization['CommaAppendableArgs']\
                ['CreateManipulate']  = ",\n".join(createManipulate_list)

        # Define density profile
        template_density = {}
        template_density['filename'] = 'density.template'
        template_density['AppendableArgs'] = {}

        if base_density is not None:
            template_density['MainArgs'] = params

        if density_profile is not None:
            template_density['AppendableArgs']['densityProfile'] = Template( \
                densityProfile[density_profile['type']] ).\
                render(**{**density_profile, **params})

        # final set of templates and variables
        self.templates = [ template_species,
                           template_particle,
                           template_speciesDefinition,
                           template_speciesInitialization,
                           template_density,
                         ]
