# Laser profiles library.
# Each profile has a name, e.g. "Gaussian", and is presented
# by a dictionary with keys '2d' and '3d' for simulation dimensions
# and values containing the codelets

LaserAntenna = {}

# Gaussian linearly polarised pulse
LaserAntenna["Gaussian"] = \
"""
            if (cellIdx.y() == ${iy_antenna}  ){

                constexpr uint_32 dim(${dim});
                constexpr uint_32 pol(${pol});

                static constexpr float_64 A0_to_J = -4*PI*SI::ELECTRON_MASS_SI/${wavelength} * SI::SPEED_OF_LIGHT_SI / SI::ELECTRON_CHARGE_SI / SI::MUE0_SI / SI::CELL_HEIGHT_SI;

                float_64 distance2_SI = float_64(cellIdx.x()-${ix_cntr}) * SI::CELL_WIDTH_SI * float_64(cellIdx.x()-${ix_cntr}) * SI::CELL_WIDTH_SI ;
                if (dim==3) {
                    distance2_SI +=  float_64(cellIdx.z()-${iz_cntr} ) * SI::CELL_DEPTH_SI * float_64(cellIdx.z()-${iz_cntr} ) * SI::CELL_DEPTH_SI;
                }

                const float_64 time_SI = float_64(currentStep) * SI::DELTA_T_SI;

                const float_64 r2_norm = distance2_SI/(${w0} * ${w0});
                const float_64 time_norm = (time_SI - ${delay}) / ${tau};

                const float_64 laser_phase = 2.0 * PI * time_SI * SI::SPEED_OF_LIGHT_SI / ${wavelength};
                const float_64 laser_profile = math::exp( -r2_norm - time_norm*time_norm );

                if (pol<3) {
                    current_comp_${pol} += laser_profile*A0*A0_to_J*math::cos(laser_phase + ${CEP});
                }

                if (pol==3) {
                    current_comp_1 += laser_profile * ${a0} * A0_to_J * math::cos(laser_phase + ${CEP});
                    current_comp_2 += laser_profile * ${a0} * A0_to_J * math::sin(laser_phase + ${CEP});
                }
            }"""
