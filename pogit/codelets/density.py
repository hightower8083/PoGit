densityProfile = {}

densityProfile['Gaussian'] = \
"""
    PMACC_STRUCT(DensityParameter${name},
        (PMACC_C_VALUE(float_X, gasFactor, ${gasFactor}))
        (PMACC_C_VALUE(float_X, gasPower, ${gasPower}))
        (PMACC_C_VALUE(uint32_t, vacuumCellsY, ${vacuumCellsY}))
        (PMACC_C_VALUE(float_64, gasCenterLeft_SI,  ${gasCenterLeft}))
        (PMACC_C_VALUE(float_64, gasCenterRight_SI, ${gasCenterRight}))
        (PMACC_C_VALUE(float_64, gasSigmaLeft_SI, ${gasSigmaLeft}))
        (PMACC_C_VALUE(float_64, gasSigmaRight_SI, ${gasSigmaRight}))
    );

    using densityProfile${name} = GaussianImpl< DensityParameter${name} >;"""
