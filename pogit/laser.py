from mako.template import Template
import numpy as np
from scipy.constants import c

from .codelets.fieldBackground import Antenna


class Laser:
    """
    Class that contains parameters of the laser defined
    via a current-driven antenna.
    Main attributes
    ---------------
        List of `templates`, which are to be rendered in the
        following files:
            include/picongpu/param/fieldBackground.param
    """
    def __init__( self, a0, ctau, waist, y_antenna, y0, i_center,
                  profile='Gaussian', pol='x', CEP = 0.0, dim='3d',
                  wavelength=0.8e-6 ):

        """
        Initialize the Antenna object
        Parameters
        ----------
        a0 : float
            Laser normalized amplitude

        ctau : float (in meters)
            Laser duration as a longitudinal size (two RMS of the
            power envelope)

        waist : float (in meters)
            Laser waist (two RMS of the intensity profile)

        y_antenna : float (in meters)
            Position of the emitting antenna in the box (y coordinate)

        y0 : float (in meters)
            Initial position of laser centroid.
            Note: Aboslute distance from antenna is counted

        i_center : tuple (two integers)
            Position of the antenna center on the grid in cells (ix, iz)

        profile: string
            Name of the profile defined in `fieldBackground.template`

        pol: char
            Laser polarization `x` or `z`

        CEP : float (in radians)
            Laser phase

        dim : string
            Simulation dimensionality '2d' or '3d'

        wavelength : float (in meters)
            Laser wavelength
        """

        params = {}
        params['a0'] = a0
        params['tau'] = ctau / c
        params['waist'] = waist
        params['delay'] = (y_antenna-y0) / c
        params['y_antenna'] = y_antenna

        params['wavelength'] = wavelength
        params['pol'] = pol
        params['CEP'] = CEP
        params['dim'] = dim

        if dim == '3d':
            params['center_x'] = i_center[0]
            params['center_z'] = i_center[1]
        elif dim == '2d':
            params['center_x'] = i_center

        params['code'] = Template(Antenna[profile][dim])\
            .render(**params)

        template = {}
        template['filename'] = 'fieldBackground.template'

        template['AppendableArgs'] = {}
        template['AppendableArgs']['Antenna'] = Template( \
            Antenna[profile][dim] ).render(**params)

        self.templates = [template,]
