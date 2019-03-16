# Laser profiles library for native implementation

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
        static constexpr float_64 WAVE_LENGTH_SI = ${wavelength};
        static constexpr float_64 AMPLITUDE_SI = -2.0*PI / ::picongpu::SI::ELECTRON_CHARGE_SI * ${a0} / WAVE_LENGTH_SI * ::picongpu::SI::ELECTRON_MASS_SI * ::picongpu::SI::SPEED_OF_LIGHT_SI * ::picongpu::SI::SPEED_OF_LIGHT_SI;
        static constexpr float_64 PULSE_LENGTH_SI = ${tau};
        static constexpr float_64 W0_SI = ${w0};
        static constexpr float_64 FOCUS_POS_SI = ${y_foc};
        static constexpr float_64 PULSE_INIT = ${injection_duration};
        static constexpr float_X LASER_PHASE = ${CEP};
        static constexpr uint32_t initPlaneY = ${iy_antenna};
        using LAGUERREMODES_t = gaussianBeam::LAGUERREMODES_t;
        static constexpr uint32_t MODENUMBER = gaussianBeam::MODENUMBER;
        enum PolarisationType
        {
            LINEAR_X = 1u,
            LINEAR_Z = 2u,
            CIRCULAR = 4u,
        };
        static constexpr PolarisationType Polarisation = ${pol};
    };
    using Selected = GaussianBeam< GaussianBeamParam >;
"""
