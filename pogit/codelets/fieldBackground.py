# Laser profiles library.
# Each profile has a name, e.g. "Gaussian", and is presented
# by a dictionary with keys '2d' and '3d' for simulation dimensions
# and values containing the codelets

Antenna = {}

# Gaussian linearly polarised pulse
Antenna["Gaussian"] = {}
Antenna["Gaussian"]['2d'] = \
"""
            if (cellIdx.y() == int(${y_antenna}/dy)  ){

                constexpr int32_t ix_center( ${center_x} );

                constexpr float_64 laser_frequency_SI(SI::SPEED_OF_LIGHT_SI/${wavelength});
                constexpr float_64 laser_tau_SI( ${tau} );
                constexpr float_64 laser_delay_SI( ${delay} );
                constexpr float_64 laser_waist_SI( ${waist} );
                constexpr float_64 A0( ${a0} );

                static constexpr float_64 A0_to_J = -4*PI*SI::ELECTRON_MASS_SI/${wavelength} * SI::SPEED_OF_LIGHT_SI / SI::ELECTRON_CHARGE_SI / SI::MUE0_SI / SI::CELL_HEIGHT_SI;

                const float_64 distance_x_SI = float_64(cellIdx.x()-ix_center) * SI::CELL_WIDTH_SI ;
                const float_64 time_SI = float_64(currentStep) * SI::DELTA_T_SI;

                const float_64 r2_norm = distance_x_SI*distance_x_SI/(laser_waist_SI*laser_waist_SI);
                const float_64 time_centered_norm = (time_SI-laser_delay_SI)/laser_tau_SI;
                const float_64 laser_phase = 2.0 * PI * time_SI * laser_frequency_SI;

                const float_64 laser_rt_profile = math::exp( -r2_norm - time_centered_norm*time_centered_norm );

                current_comp_${pol} += laser_rt_profile*A0*A0_to_J*math::cos(laser_phase + ${CEP});
            }"""

Antenna["Gaussian"]['3d'] = \
"""
            if (cellIdx.y()==int(${y_antenna}/dy)){

                constexpr int32_t ix_center( ${center_x} );
                constexpr int32_t iz_center( ${center_z}  );

                constexpr float_64 laser_frequency_SI(SI::SPEED_OF_LIGHT_SI/${wavelength});
                constexpr float_64 laser_tau_SI( ${tau} );
                constexpr float_64 laser_delay_SI( ${delay} );
                constexpr float_64 laser_waist_SI( ${waist} );
                constexpr float_64 A0( ${a0} );

                static constexpr float_64 A0_to_J = -4*PI*SI::ELECTRON_MASS_SI/${wavelength} * SI::SPEED_OF_LIGHT_SI / SI::ELECTRON_CHARGE_SI / SI::MUE0_SI / SI::CELL_HEIGHT_SI;

                const float_64 distance_x_SI = float_64(cellIdx.x()-ix_center) * SI::CELL_WIDTH_SI ;
                const float_64 distance_z_SI = float_64(cellIdx.z()-iz_center) * SI::CELL_DEPTH_SI ;
                const float_64 time_SI = float_64(currentStep) * SI::DELTA_T_SI;

                const float_64 r2_norm = (distance_x_SI*distance_x_SI + distance_z_SI*distance_z_SI)/(laser_waist_SI*laser_waist_SI);
                const float_64 time_centered_norm = (time_SI-laser_delay_SI)/laser_tau_SI;
                const float_64 laser_phase = 2.0 * PI * time_SI * laser_frequency_SI;

                const float_64 laser_rt_profile = math::exp( -r2_norm - time_centered_norm*time_centered_norm );

                current_comp_${pol} += laser_rt_profile*A0*A0_to_J*math::cos(laser_phase + ${CEP});
            }"""


# Gaussian circularly polarised pulse
Antenna["GaussianCIRCULAR"] = {}
Antenna["GaussianCIRCULAR"]['2d'] = \
"""
            if (cellIdx.y()==int(${y_antenna}/dy)){

                constexpr int32_t ix_center( ${center_x} );

                constexpr float_64 laser_frequency_SI(SI::SPEED_OF_LIGHT_SI/${wavelength});
                constexpr float_64 laser_tau_SI( ${tau} );
                constexpr float_64 laser_delay_SI( ${delay} );
                constexpr float_64 laser_waist_SI( ${waist} );
                constexpr float_64 A0( ${a0} );

                static constexpr float_64 A0_to_J = -4*PI*SI::ELECTRON_MASS_SI/${wavelength} * SI::SPEED_OF_LIGHT_SI / SI::ELECTRON_CHARGE_SI / SI::MUE0_SI / SI::CELL_HEIGHT_SI;

                const float_64 distance_x_SI = float_64(cellIdx.x()-ix_center) * SI::CELL_WIDTH_SI ;
                const float_64 time_SI = float_64(currentStep) * SI::DELTA_T_SI;

                const float_64 r2_norm = distance_x_SI*distance_x_SI/(laser_waist_SI*laser_waist_SI);
                const float_64 time_centered_norm = (time_SI-laser_delay_SI)/laser_tau_SI;
                const float_64 laser_phase = 2.0 * PI * time_SI * laser_frequency_SI;

                const float_64 laser_rt_profile = math::exp( -r2_norm - time_centered_norm*time_centered_norm );

                current_comp_x += laser_rt_profile*A0*A0_to_J*math::cos(laser_phase + ${CEP});
                current_comp_z += laser_rt_profile*A0*A0_to_J*math::sin(laser_phase + ${CEP});
            }"""

Antenna["GaussianCIRCULAR"]['3d'] = \
"""
            if (cellIdx.y()==int(${y_antenna}/dy)){

                constexpr int32_t ix_center( ${center_x} );
                constexpr int32_t iz_center( ${center_z}  );

                constexpr float_64 laser_frequency_SI(SI::SPEED_OF_LIGHT_SI/${wavelength});
                constexpr float_64 laser_tau_SI( ${tau} );
                constexpr float_64 laser_delay_SI( ${delay} );
                constexpr float_64 laser_waist_SI( ${waist} );
                constexpr float_64 A0( ${a0} );

                static constexpr float_64 A0_to_J = -4*PI*SI::ELECTRON_MASS_SI/${wavelength} * SI::SPEED_OF_LIGHT_SI / SI::ELECTRON_CHARGE_SI / SI::MUE0_SI / SI::CELL_HEIGHT_SI;

                const float_64 distance_x_SI = float_64(cellIdx.x()-ix_center) * SI::CELL_WIDTH_SI ;
                const float_64 distance_z_SI = float_64(cellIdx.z()-iz_center) * SI::CELL_DEPTH_SI ;
                const float_64 time_SI = float_64(currentStep) * SI::DELTA_T_SI;

                const float_64 r2_norm = (distance_x_SI*distance_x_SI + distance_z_SI*distance_z_SI)/(laser_waist_SI*laser_waist_SI);
                const float_64 time_centered_norm = (time_SI-laser_delay_SI)/laser_tau_SI;
                const float_64 laser_phase = 2.0 * PI * time_SI * laser_frequency_SI;

                const float_64 laser_rt_profile = math::exp( -r2_norm - time_centered_norm*time_centered_norm );

                current_comp_x += laser_rt_profile*A0*A0_to_J*math::cos(laser_phase + ${CEP});
                current_comp_z += laser_rt_profile*A0*A0_to_J*math::sin(laser_phase + ${CEP});
            }"""
