## particle start positions codelets

StartPosition = {}

StartPosition["Random"] = \
"""
    struct RandomParameter${name}
    {
        static constexpr uint32_t numParticlesPerCell = ${Nppc};
    };
    using startPosition${name} = RandomImpl< RandomParameter${name} >;"""

StartPosition["Ordered"] = \
"""
    struct QuietParam${name}
    {
        using numParticlesPerDimension = mCT::shrinkTo<
            mCT::Int<
                ${NppcX},
                ${NppcY},
                ${NppcZ}
                >,
            simDim
        >::type;
    };

    using startPosition${name} = QuietImpl< QuietParam${name} >;"""

## particle manipulators codelets
Manipulators = {}

Manipulators['Temperature'] = \
"""
    struct TemperatureParam${name}
    {
        static constexpr float_64 temperature = ${Temperature};
    };
    using AddTemperature${name} = unary::Temperature< TemperatureParam${name} >;"""

Manipulators['SetIonCharge'] = \
"""
    struct SetIonChargeImpl${name}
    {
        template< typename T_Particle >
        DINLINE void operator()(
            T_Particle& particle
        )
        {
            constexpr float_X protonNumber = GetAtomicNumbers< T_Particle >::type::numberOfProtons;
            particle[ boundElectrons_ ] = protonNumber - ${InitialCharge}._X;
        }
    };
    using SetIonCharge${name} = generic::Free< SetIonChargeImpl${name} >;"""
