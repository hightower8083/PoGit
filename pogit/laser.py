from mako.template import Template
import numpy as np
from scipy.constants import c

from .codelets.laser import LaserProfile


class Laser:
    """
    Class that contains parameters of the laser defined in PIConGPU
    Main attributes
    ---------------
        List of `templates`, which are to be rendered in the
        following files:
            include/picongpu/param/laser.param
    """
    def __init__( self, a0, ctau, waist, cdelay, iy_antenna=0,
                  y_foc=1e-6, profile='Gaussian', pol='x', CEP = 0.0,
                  wavelength=0.8e-6, LaguerreModeNumber=0,
                  LaguerreModes=[1.,] ):

        """
        Initialize the Laser object
        Parameters
        ----------
        a0 : float
            Laser normalized amplitude

        ctau : float (in meters)
            Laser duration as a longitudinal size (two RMS of the
            power envelope)

        waist : float (in meters)
            Laser waist (two RMS of the intensity profile)

        cdelay : float (in meters)
            Delay between simulation start and time of laser centre,
            as a longitudinal size ( c * delay )

        iy_antenna : integer (in cells)
            Position of the emitting antenna in the box (y coordinate).

        y_foc : float (in meters)
            Laser focal position along y-axis. Currently focal position
            cannot be equal to the antenna position.

        profile: string
            Name of the profile defined in `codelets/laser.py`

        pol: char
            Laser polarization `x`, `z` or `circ`

        CEP : float (in radians)
            Laser phase

        wavelength : float (in meters)
            Laser wavelength
        """
        params = {}

        params['A0'] = a0
        params['PULSE_LENGTH'] = ctau / c / 1.17741
        params['W0'] = waist
        params['FOCUS_POS'] = y_foc
        params['PULSE_INIT'] = 2 * cdelay / c / params['PULSE_LENGTH']
        params['initPlaneY'] = iy_antenna
        params['WAVE_LENGTH'] = wavelength
        params['Polarisation'] = {'x':'LINEAR_X', 'z':'LINEAR_Z',
                                  'circ':'CIRCULAR'}[pol]
        params['LASER_PHASE'] = CEP
        params['MODENUMBER'] = LaguerreModeNumber
        params['LAGUERREMODES'] = ", ".join([str(m) for m in LaguerreModes])

        # Converting float and integer arguments to strings
        for arg in params.keys():
            if type(params[arg]) == float:
                # Imposing a fixed float format
                params[arg] = f"{params[arg]:.15e}"
            if type(params[arg]) == int:
                params[arg] = f"{params[arg]:d}"

        template = {}
        template['filename'] = 'laser.template'

        template['MainArgs'] = {}
        template['MainArgs']["laserProfile"] = Template( \
            LaserProfile[profile] ).render(**params)

        self.templates = [template,]
