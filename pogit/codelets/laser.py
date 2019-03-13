LaserProfile = {}

LaserProfile["Gaussian"] = \
"""
namespace gaussianBeam
{
    static constexpr uint32_t MODENUMBER = ${MODENUMBER};
    PMACC_CONST_VECTOR(float_X, MODENUMBER + 1, LAGUERREMODES, ${LAGUERREMODES}
    );
}
    struct GaussianBeamParam
    {
        static constexpr float_64 WAVE_LENGTH_SI = ${WAVE_LENGTH};
        static constexpr float_64 AMPLITUDE_SI = -2.0*PI / ::picongpu::SI::ELECTRON_CHARGE_SI * ${A0} / WAVE_LENGTH_SI * ::picongpu::SI::ELECTRON_MASS_SI * ::picongpu::SI::SPEED_OF_LIGHT_SI * ::picongpu::SI::SPEED_OF_LIGHT_SI;
        static constexpr float_64 PULSE_LENGTH_SI = ${PULSE_LENGTH};
        static constexpr float_64 W0_SI = ${W0};
        static constexpr float_64 FOCUS_POS_SI = ${FOCUS_POS};
        static constexpr float_64 PULSE_INIT = ${PULSE_INIT};
        static constexpr float_X LASER_PHASE = ${LASER_PHASE};
        static constexpr uint32_t initPlaneY = ${initPlaneY};
        using LAGUERREMODES_t = gaussianBeam::LAGUERREMODES_t;
        static constexpr uint32_t MODENUMBER = gaussianBeam::MODENUMBER;
        enum PolarisationType
        {
            LINEAR_X = 1u,
            LINEAR_Z = 2u,
            CIRCULAR = 4u,
        };
        static constexpr PolarisationType Polarisation = ${Polarisation};
    };
    using Selected = GaussianBeam< GaussianBeamParam >;
"""
