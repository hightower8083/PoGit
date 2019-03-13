speciesDefinition = {}

speciesDefinition['ion'] = \
"""
value_identifier( float_X, MassRatio${name}, ${MassRatio} );
value_identifier( float_X, ChargeRatio${name}, ${ChargeRatio} );
value_identifier( float_X, DensityRatio${name}, ${DensityRatio} );

using ParticleFlags${name} = MakeSeq_t<
    particlePusher< UsedParticlePusher${name} >,
    shape< UsedParticleShape${name} >,
    interpolation< UsedField2Particle${name} >,
    current< UsedParticleCurrentSolver${name} >,
    massRatio< MassRatio${name} >,
    chargeRatio< ChargeRatio${name} >,
    densityRatio< DensityRatio${name} >,
    ionizers<
        MakeSeq_t<
            particles::ionization::BSIEffectiveZ< PIC_${TargetSpeciesName} >,
            particles::ionization::ADK${pol}Pol< PIC_${TargetSpeciesName} >
        >
    >,
    ionizationEnergies< ionization::energies::AU::${Element}_t >,
    effectiveNuclearCharge< ionization::effectiveNuclearCharge::${Element}_t >,
    atomicNumbers< ionization::atomicNumbers::${Element}_t >
>;

using PIC_${name} = Particles<
    PMACC_CSTRING( "${name}" ),
    ParticleFlags${name},
    IonParticleAttributes
>;"""

speciesDefinition['generic_ionizable'] = speciesDefinition['ion']

speciesDefinition['generic_nonionizable'] = \
"""
value_identifier( float_X, MassRatio${name}, ${MassRatio} );
value_identifier( float_X, ChargeRatio${name}, ${ChargeRatio} );
value_identifier( float_X, DensityRatio${name}, ${DensityRatio} );

using ParticleFlags${name} = MakeSeq_t<
    particlePusher< UsedParticlePusher${name} >,
    shape< UsedParticleShape${name} >,
    interpolation< UsedField2Particle${name} >,
    current< UsedParticleCurrentSolver${name} >,
    massRatio< MassRatio${name} >,
    chargeRatio< ChargeRatio${name} >,
    densityRatio< DensityRatio${name} >
>;

using PIC_${name} = Particles<
    PMACC_CSTRING( "${name}" ),
    ParticleFlags${name},
    DefaultParticleAttributes
>;"""

speciesDefinition['electron'] = \
"""
value_identifier( float_X, MassRatio${name}, 1.0 );
value_identifier( float_X, ChargeRatio${name}, 1.0 );
value_identifier( float_X, DensityRatio${name}, ${DensityRatio} );

using ParticleFlags${name} = MakeSeq_t<
    particlePusher< UsedParticlePusher${name} >,
    shape< UsedParticleShape${name} >,
    interpolation< UsedField2Particle${name} >,
    current< UsedParticleCurrentSolver${name} >,
    massRatio< MassRatio${name} >,
    chargeRatio< ChargeRatio${name} >,
    densityRatio< DensityRatio${name} >
>;

/* define species electrons */
using PIC_${name} = Particles<
    PMACC_CSTRING( "${name}" ),
    ParticleFlags${name},
    DefaultParticleAttributes
>;"""

speciesDefinition['proton'] = \
"""
value_identifier( float_X, MassRatio${name}, 1836.152672 );
value_identifier( float_X, ChargeRatio${name}, -1.0 );
value_identifier( float_X, DensityRatio${name}, ${DensityRatio} );

using ParticleFlags${name} = MakeSeq_t<
    particlePusher< UsedParticlePusher${name} >,
    shape< UsedParticleShape${name} >,
    interpolation< UsedField2Particle${name} >,
    current< UsedParticleCurrentSolver${name} >,
    massRatio< MassRatio${name} >,
    chargeRatio< ChargeRatio${name} >,
    densityRatio< DensityRatio${name} >
>;

/* define species ions */
using PIC_${name} = Particles<
    PMACC_CSTRING( "${name}" ),
    ParticleFlags${name},
    DefaultParticleAttributes
>;"""

speciesDefinition['photon'] = \
"""
/*--------------------------- photons -------------------------------------------*/

value_identifier( float_X, MassRatio${name}, 0.0 );
value_identifier( float_X, ChargeRatio${name}, 0.0 );

using ParticleFlags${name} = MakeSeq_t<
    particlePusher< UsedParticlePusher${name} >,
    shape< UsedParticleShape${name} >,
    interpolation< UsedField2Particle${name} >,
    massRatio< MassRatio${name} >,
    chargeRatio< ChargeRatio${name} >
>;

/* define species photons */
using PIC_${name} = Particles<
    PMACC_CSTRING( "${name}" ),
    ParticleFlags${name},
    DefaultParticleAttributes
>;"""
