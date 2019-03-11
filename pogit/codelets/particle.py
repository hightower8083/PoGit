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
Manipulator = {}

Manipulator['Temperature'] = \
"""
    struct TemperatureParam${name}
    {
        static constexpr float_64 temperature = ${Temperature};
    };
    using AddTemperature${name} = unary::Temperature< TemperatureParam${name} >;"""
