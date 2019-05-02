densityProfile = {}

densityProfile['Gaussian'] = \
"""
    PMACC_STRUCT(DensityParameter${name}${profile_index},
        (PMACC_C_VALUE(float_X, gasFactor, ${gasFactor}))
        (PMACC_C_VALUE(float_X, gasPower, ${gasPower}))
        (PMACC_C_VALUE(uint32_t, vacuumCellsY, ${vacuumCellsY}))
        (PMACC_C_VALUE(float_64, gasCenterLeft_SI,  ${gasCenterLeft}))
        (PMACC_C_VALUE(float_64, gasCenterRight_SI, ${gasCenterRight}))
        (PMACC_C_VALUE(float_64, gasSigmaLeft_SI, ${gasSigmaLeft}))
        (PMACC_C_VALUE(float_64, gasSigmaRight_SI, ${gasSigmaRight}))
    );

    using densityProfile${name}${profile_index} = GaussianImpl< DensityParameter${name}${profile_index} >;"""

densityProfile['FormulaXY'] = \
"""
    struct DensityParameter${name}${profile_index}
    {
        HDINLINE float_X
        operator()(
            const floatD_64& position_SI,
            const float3_64& cellSize_SI
        )
        {
            const float_64 x( position_SI.x() );
            const float_64 y( position_SI.y() );
            float_64 dens = 0.0;
${Formula}
            dens *= float_64( dens >= 0.0 );
            return dens;
        }
    };

    using densityProfile${name}${profile_index} = FreeFormulaImpl< DensityParameter${name}${profile_index} >;"""
    
densityProfile['FormulaXYZ'] = \
"""
    struct DensityParameter${name}${profile_index}
    {
        HDINLINE float_X
        operator()(
            const floatD_64& position_SI,
            const float3_64& cellSize_SI
        )
        {
            const float_64 x( position_SI.x() );
            const float_64 y( position_SI.y() );
            const float_64 z( position_SI.z() );
            float_64 dens = 0.0;
${Formula}
            dens *= float_64( dens >= 0.0 );
            return dens;
        }
    };

    using densityProfile${name}${profile_index} = FreeFormulaImpl< DensityParameter${name}${profile_index} >;"""
