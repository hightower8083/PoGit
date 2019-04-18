from mako.template import Template
import numpy as np
from scipy.constants import c

from .codelets.laser import LaserProfile
from .codelets.fieldBackground import LaserAntenna
from .codelets.fieldBackground import r2_2d, r2_3d
from .codelets.fieldBackground import laser_profile_2d, laser_profile_3d

class Laser:
    """
    Class that defines laser using either native PIConGPU
    method or current-driven antenna (multiple sources).
    Note that methods need some featured arguments to be set.

    Main attributes
    ---------------
        List of `templates`, which are to be rendered in the
        following files:
            include/picongpu/param/laser.param
            include/picongpu/param/fieldBackground.param
    """
    def __init__( self, a0, ctau, waist, cdelay, iy_antenna=0,
                  y_foc=0.0, profile='Gaussian', pol='x', CEP = 0.0,
                  wavelength=0.8e-6, method='native', LMNum=0, LM=[1.,],
                  dim='3d', center_ij=(0,0) ):

        """
        Initialize the Laser object
        Parameters
        ----------
        a0 : float
            Laser normalized amplitude

        ctau : float (in meters)
            Laser duration as two RMS of the intensity profile
            ctau * 1.17741 = FWHM of the intensity profile

        waist : float (in meters)
            Laser waist (two RMS of the intensity profile)

        cdelay : float (in meters)
            Delay between simulation start and time of laser centre,
            as a longitudinal size ( c * delay )

        iy_antenna : integer (in cells)
            Position of the emitting antenna in the box (y coordinate).

        y_foc : float (in meters)
            Laser focal y-position

        profile: string
            Name of the profile defined in `codelets/laser.py`

        pol: char
            Laser polarization `x`, `z` or `circ`

        CEP : float (in radians)
            Laser phase

        wavelength : float (in meters)
            Laser wavelength

        method : string
            Method of field egeneration to be used. Can be:
              'native': Native method of PIConGPU. Allows multiple Laguerre
                modes, and can disable absorber at (Y=0). Presently, only
                single laser definition is allowed.
              'antenna': Generate laser by electric current in the Y-plane.
                Allows multiple definitons. Extendable in codelets

        LMNum : integer
            Number of Laguerre modes for tranverse profile (used by 'native')

        LM : list
            List of coefficients of Laguerre modes (used by 'native')

        dim: string
            Dimensionality, '3d' or '2d' (used by 'antenna')

        center_ij : tuple (2 integers)
            X and Z indicies of the laser axis on the simulation grid.
            Should be set, for example to `(Nx//2,Nz//2)` (used by 'antenna')
        """
        params = {}

        params['a0'] = a0
        params['w0'] = waist
        params['y_foc'] = y_foc
        params['iy_antenna'] = iy_antenna
        params['wavelength'] = wavelength
        params['CEP'] = CEP

        if method=='native':
            params['tau'] = ctau / c / 2
            params['injection_duration'] = 2 * cdelay / c / params['tau']
            params['pol'] = { 'x':'LINEAR_X', 'z':'LINEAR_Z',
                              'circ':'CIRCULAR' }[pol]
            params['MODENUMBER'] = LMNum
            params['LAGUERREMODES'] = ", ".join([str(m) for m in LM])
        elif method=='antenna':
            params['tau'] = ctau / c
            params['delay'] = cdelay / c
            params['dim'] = { '2d':'2', '3d':'3' }[dim]
            params['pol'] = { 'x':'1', 'z':'2', 'circ':'3' }[pol]
            params['ix_cntr'] = center_ij[0]
            params['iz_cntr'] = center_ij[1]
            if dim=='3d':
               params['r2'] = Template(r2_3d).render(**params)
               params['laser_profile'] = Template(laser_profile_3d).render(**params)
            elif dim=='2d':
               params['r2'] = Template(r2_2d).render(**params)
               params['laser_profile'] = Template(laser_profile_2d).render(**params)
            
        # Converting float and integer arguments to strings
        for arg in params.keys():
            if type(params[arg]) == float:
                # Imposing a fixed float format
                params[arg] = f"{params[arg]:.15e}"
            if type(params[arg]) == int:
                params[arg] = f"{params[arg]:d}"

        template = {}
        if method=='native':
            template['filename'] = 'laser.template'
            template['Main'] = {}
            template['Main']["laserProfile"] = Template( \
                LaserProfile[profile] ).render(**params)

        elif method=='antenna':
            template['filename'] = 'fieldBackground.template'

            template['Appendable'] = {}
            template['Appendable']['\n'] = {}
            template['Appendable']['\n']['Antenna'] = Template( \
               LaserAntenna[profile] ).render(**params)

        self.templates = [template,]
