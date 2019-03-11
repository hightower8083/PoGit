speciesNumericalParam = \
"""
using UsedParticleShape${name} = particles::shapes::${ParticleShape};

using UsedField2Particle${name} = FieldToParticleInterpolation<
    UsedParticleShape${name},
    AssignedTrilinearInterpolation>;

using UsedParticleCurrentSolver${name} = currentSolver::${CurrentSolver}< UsedParticleShape${name} >;
using UsedParticlePusher${name} = particles::pusher::${ParticlePusher};"""
