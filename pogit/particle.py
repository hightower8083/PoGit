from mako.template import Template
import numpy as np
from scipy.constants import c, atomic_mass, m_e, m_p
from mendeleev import element as table_element

from .codelets.particle import StartPosition, Manipulators
from .codelets.density import densityProfile
from .codelets.species import speciesNumericalParam
from .codelets.speciesDefinition import speciesDefinition
from .codelets.speciesInitialization import CreateDensity 
from .codelets.speciesInitialization import SetIonCharge
from .codelets.speciesInitialization import SetIonNeutral

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
    def __init__( self, name, species, initial_positions=None,
                  typicalNppc=None, density_profile=None,
                  base_density=None, relative_density=1.0,
                  element=None, initial_charge=0,
                  mass_ratio=m_p/m_e, charge_ratio=-1,
                  target_species=None, ionizer_polarization='Lin',
                  initial_temperature=None,
                  shape_order=1, pusher='Boris',
                  current_deposition='Esirkepov' ):

        """
        Initialize the Particle object
        Parameters
        ----------
        name : string
            Name of the particle species.
            NB: These names are given to the code variables, and usage of special
            symbols (interpreted by compiler), e.g. `+`, `-` or spaces is not 
            allowed

        species : string
            Type of the species. Presently supported types:
                'electron' : simple electron
                'proton' : simple proton
                'ion' : ion from periodic table
                'generic_ionizable' : ion from periodic table with custom
                                      `mass_ratio` and `charge_ratio`
                'generic_nonionizable' : fully ionized ion with custom
                                         `mass_ratio` and `charge_ratio`

            Note : 'ion'and 'generic_ionizable' need `element` name


        initial_positions : list
            Method to initialize particles in cell. First element
            is a string, which can be:
                'Ordered' : ordered positions with numbers of particles
                            per direction defined by a tuple of integers
                            (NppcX,NppcX,NppcZ)
                'Random': random positions in cell, with total number
                          defined as an integer Nppc
                'OnePosition': put all particles at the same position in the
                               cell, needs an integer for number of particles
                               per cell and tuple for the normalized [0.0, 1.0)
                               in-cell offset [Nppc, (offX, offY, offZ)]

        typicalNppc : integer
            `Typical` total number of particles per cell used for internal
            PIConGPU normalization. Should account for all species, and be
            defined only for the one of them

        density_profile : dictionary or list of dictionaries
            Parameters for the density profile defined as a codelet
            (see example). Can be the list of profiles, in which case
            each profile will be generated independently, i.e. summed

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
            Charge of the fully ionized species in units of electron charge

        target_species : Particle object
            Species to which ionized electrons are attributed

        ionizer_polarization: string
            Polarization of ionizing radiation, 'Circ' or 'Lin' (for ADK)

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
            Scheme of current deposition. Can be:
                "Esirkepov" : charge conservative deposition (1st to 4th order)
                "VillaBune": (1st order)
                "EmZ": (1st to 4th order)
                "ZigZag": (1st to 4th order)
        """
        self.name = name

        params = {}
        params['name'] = name
        params['type'] = species
        params['ParticleShape'] = {1: "CIC",
                                   2: "TSC",
                                   3: "PCS",
                                   4: "P4S"}[shape_order]

        params['CurrentSolver'] =  current_deposition
        if params['type']=='probe':
            params['ParticlePusher'] = 'Probe'
        else:
            params['ParticlePusher'] = pusher
        params['Temperature'] = initial_temperature

        if initial_positions is not None:
            if initial_positions[0] == 'Ordered':
                params['NppcX'] = initial_positions[1][0]
                params['NppcY'] = initial_positions[1][1]
                params['NppcZ'] = initial_positions[1][2]
            elif initial_positions[0] == 'Random':
                params['Nppc'] = initial_positions[1]
            elif initial_positions[0] == 'OnePosition':
                params['Nppc'] = initial_positions[1]
                params['offX'] = initial_positions[2][0]
                params['offY'] = initial_positions[2][1]
                params['offZ'] = initial_positions[2][2]

        if typicalNppc is not None:
            params['TYPICAL_PARTICLES_PER_CELL'] = typicalNppc

        if base_density is not None:
            params["BASE_DENSITY"] = base_density

        params['DensityRatio'] = relative_density

        if species=='generic_ionizable' or species=='ion':
            if element is None:
                raise ValueError(f'{species} needs `element` argument')

            params["Element"] = element
            params["TargetSpeciesName"] = target_species.name
            params["InitialCharge"] = initial_charge
            params["pol"] = ionizer_polarization

        if species=='generic_ionizable' or species=='generic_nonionizable':
            params["MassRatio"] = mass_ratio
            params["ChargeRatio"] = charge_ratio
        elif species=='ion':
            el = table_element(element)
            params["MassRatio"] = el.mass * atomic_mass / m_e
            params["ChargeRatio"] = -el.atomic_number

        # Converting float and integer arguments to strings
        for arg in params.keys():
            if type(params[arg]) == float:
                # Imposing a fixed float format
                params[arg] = f"{params[arg]:.15e}"
            if type(params[arg]) == int:
                params[arg] = f"{params[arg]:d}"

        # NOW GO TEMPLATES
        # Generic parameters
        template_species = {}
        template_species['filename'] = 'species.template'
        template_species['Appendable'] = {}
        template_species['Appendable']['\n'] = {}
        template_species['Appendable']['\n']['speciesNumericalParam']= \
            Template(speciesNumericalParam).render(**params)

        # Species definition
        template_speciesDefinition = {}
        template_speciesDefinition['filename'] = 'speciesDefinition.template'
        template_speciesDefinition['Appendable'] = {}
        template_speciesDefinition['Appendable']['\n'] = {}
        template_speciesDefinition['Appendable'][',\n'] = {}

        template_speciesDefinition['Appendable']['\n']['SpeciesDefinition'] = \
            Template(speciesDefinition[species]).render(**params)
        template_speciesDefinition['Appendable'][',\n']['SpeciesRuntimeName'] =\
            'PIC_' + name

        # Initialization features and manipulators
        template_particle = {}
        template_particle['filename'] = 'particle.template'
        if typicalNppc is not None:
            template_particle['Main'] = params

        template_particle['Appendable'] = {}
        template_particle['Appendable']['\n'] = {}

        if initial_positions is not None:
            template_particle['Appendable']['\n']['StartPosition'] = Template( \
                StartPosition[initial_positions[0]] ).render(**params)

        manipulator_list = []

        # configure initial charge manipulator for ionizable
        if species=='generic_ionizable' or species=='ion':
            manipulator_list.append( Template( Manipulators['SetIonCharge'] )\
                .render(**params) )

        # configure temperature manipulator
        if initial_temperature is not None:
            manipulator_list.append( Template( Manipulators['Temperature'])\
                .render(**params) )

        # add manipulators
        template_particle['Appendable']['\n']['Manipulators'] = \
            "\n".join(manipulator_list)

        # Species initialization
        template_speciesInitialization = {}
        template_speciesInitialization['filename'] = \
            'speciesInitialization.template'

        template_speciesInitialization['Appendable'] = {}
        template_speciesInitialization['Appendable'][',\n'] = {}

        createManipulate_list = []
        if density_profile is not None:
            if type(density_profile) in (list, tuple):
                # if multiple entries create with enumerated indices
                for profile_index, prof in enumerate(density_profile):
                    params['profile_index'] = str(profile_index)
                    createManipulate_list.append( Template(CreateDensity)\
                                                  .render(**params))
            else:
                # if single entry set index to 0
                params['profile_index'] = '0'
                createManipulate_list.append( Template(CreateDensity)\
                                              .render(**params))

        # apply initial charge manipulator for ionizable
        if species=='generic_ionizable' or species=='ion':
            if initial_charge==0:
                createManipulate_list.append( Template(SetIonNeutral)\
                                              .render(**params))
            else:
                createManipulate_list.append( Template(SetIonCharge)\
                                              .render(**params))

        # add manipulator applications
        if len(createManipulate_list) != 0:
            template_speciesInitialization['Appendable'][',\n']\
                ['CreateManipulate']  = ",\n".join(createManipulate_list)

        # Density profile
        template_density = {}
        template_density['filename'] = 'density.template'
        template_density['Appendable'] = {}
        template_density['Appendable']['\n'] = {}

        if base_density is not None:
            template_density['Main'] = params

        # Process density profiles
        if density_profile is not None:
            if type(density_profile) in (list, tuple):
                # if multiple entries join with enumerated indices and add
                tmpt_loc = []
                for profile_index, prof in enumerate(density_profile):
                    params['profile_index'] = str(profile_index)
                    tmpt_loc.append( Template(densityProfile[prof['name']] )\
                        .render(**{**prof, **params}) )

                tmpt_loc = '\n'.join(tmpt_loc)
            else:
                # if single entry set index to 0
                params['profile_index'] = '0'
                tmpt_loc = Template( densityProfile[density_profile['name']] )\
                    .render(**{**density_profile, **params})

            # add density profiles
            template_density['Appendable']['\n']['densityProfile'] = tmpt_loc

        # final set of templates
        self.templates = [ template_species,
                           template_particle,
                           template_speciesDefinition,
                           template_speciesInitialization,
                           template_density,
                         ]
