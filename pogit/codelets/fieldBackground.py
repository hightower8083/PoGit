# Laser profiles library.
# Each profile has a name, e.g. "Gaussian", and is presented
# by a dictionary with keys '2d' and '3d' for simulation dimensions
# and values containing the codelets

LaserAntenna = {}

# Gaussian linearly polarised pulse
LaserAntenna["Gaussian"] = \
"""
            if (cellIdx.y() == ${iy_antenna}  ){

                static constexpr int32_t pol(${pol});
                static constexpr float_64 A0_to_J (-4*PI*SI::ELECTRON_MASS_SI/${wavelength} * SI::SPEED_OF_LIGHT_SI / SI::ELECTRON_CHARGE_SI / SI::MUE0_SI / SI::CELL_HEIGHT_SI);                
                ${r2}
                const float_64 time_SI = float_64(currentStep) * SI::DELTA_T_SI;
                const float_64 y_relpos = ${y_foc} - ${iy_antenna} * SI::CELL_HEIGHT_SI;
                const float_64 Rayleigh_SI = PI * ${w0} * ${w0} / ${wavelength};
                const float_64 w2_SI = ${w0} * ${w0} * (1+y_relpos * y_relpos / Rayleigh_SI / Rayleigh_SI); 
                const float_64 r2_norm = distance2_SI / w2_SI;
                const float_64 Ry_inverse_SI = -y_relpos / (y_relpos * y_relpos + Rayleigh_SI * Rayleigh_SI);
                const float_64 Gouy_phase = algorithms::math::atan(-y_relpos/Rayleigh_SI);
                const float_64 temporal_norm = (time_SI - ${delay} - distance2_SI * Ry_inverse_SI /2/SI::SPEED_OF_LIGHT_SI + Gouy_phase /2.0 / PI /SI::SPEED_OF_LIGHT_SI* ${wavelength}) / ${tau};
                const float_64 laser_phase = 2.0 * PI / ${wavelength} * (time_SI * SI::SPEED_OF_LIGHT_SI -${delay} * SI::SPEED_OF_LIGHT_SI- distance2_SI * Ry_inverse_SI /2) + Gouy_phase ;                
                ${laser_profile}
                
                if (pol<3) {
                    current_comp_${pol} += laser_profile * ${a0} * A0_to_J * math::sin(laser_phase + ${CEP});
                }

                if (pol==3) {
                    current_comp_1 += laser_profile * ${a0} * A0_to_J * math::sin(laser_phase + ${CEP});
                    current_comp_2 += laser_profile * ${a0} * A0_to_J * math::cos(laser_phase + ${CEP});
                }
            }"""

r2_2d = "const float_64 distance2_SI = float_64(cellIdx.x()-${ix_cntr}) * SI::CELL_WIDTH_SI * float_64(cellIdx.x()-${ix_cntr}) * SI::CELL_WIDTH_SI ;"
r2_3d = "const float_64 distance2_SI = float_64(cellIdx.x()-${ix_cntr}) * SI::CELL_WIDTH_SI * float_64(cellIdx.x()-${ix_cntr}) * SI::CELL_WIDTH_SI +  float_64(cellIdx.z()-${iz_cntr} ) * SI::CELL_DEPTH_SI * float_64(cellIdx.z()-${iz_cntr} ) * SI::CELL_DEPTH_SI;"
laser_profile_2d = "const float_64 laser_profile = math::exp( -r2_norm - temporal_norm*temporal_norm ) * algorithms::math::sqrt(${w0}) / algorithms::math::sqrt(algorithms::math::sqrt(w2_SI));"
laser_profile_3d = "const float_64 laser_profile = math::exp( -r2_norm - temporal_norm*temporal_norm ) * ${w0} / algorithms::math::sqrt(w2_SI);"
