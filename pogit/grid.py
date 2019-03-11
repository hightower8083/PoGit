from mako.template import Template
from scipy.constants import c
import numpy as np

class GridSolver:
    """
    Class that contains parameters of the numerical grid and the solver.
    Main attributes
    ---------------
        List of `templates`, which are to be rendered in the
        following files:
            include/picongpu/param/grid.param
            include/picongpu/param/dimension.param
            include/picongpu/param/fieldSolver.param
            etc/picongpu/run.cfg
    """
    def __init__( self, xmax, ymax, zmax, Nx, Ny, Nz,
                  Nsteps, decomposition = (1,2,1),
                  dim='3d', dt_fromCFL=0.995, dt=None, absorber=None,
                  type='Yee', J_smoothing=None,
                  movingWindow=False, movePoint=1.0
                ):
        """
        Initialize the GridSolver object
        Parameters
        ----------
        xmax, ymax, zmax : float (in meters)
            Lengths of the simulation box in x, y and z directions

        Nx, Ny, Nz : int
            Numbers of gridpoints in x, y and z directions

        Nsteps : int
            Number of simu;ation steps to perform

        decomposition: tuple (three int)
            Number of devices used in x, y and z directions

        dim : string
            Dimensionality of the simulation. Can be '3d' or '2d'

        dt_fromCFL : float
            If not `None`, then time-step will be calculated from CFL
            condition using this value as a factor

        dt : float (in seconds)
            If not `None`, used as a time-step.
            Sould not be used if `dt_fromCFL` is not `None`

        absorber : dict
            Dictionary defining the absorber (see below for details)

        type : string
            Solver to be used. Can be:
                "Yee": (default)
                "Lehe": (anti-NCI scheme)
                "DirSplitting": Sentoku's Directional Splitting Method
                "None": disable the vacuum update of E and B

        J_smoothing : string
            Smoothing of the currents. Can be:
                None: no smoothing is performed (default)
                "Binomial": 2nd order Binomial filter
                "NoneDS": experimental, for directional splitting

        movingWindow : bool
            If True the moving window along y-axis will be activated

        movePoint : float
             Slide point model to start moving the co-moving window.
              A virtual photon starts at t=0 and y=0. When it reaches
              movePoint % of the global simulation box the co-moving
              window starts to move with the speed of light.
        """
        params = {}

        params['simDim'] = dim[0]

        params['nGPUx'] = decomposition[0]
        params['nGPUy'] = decomposition[1]
        params['nGPUz'] = decomposition[2]

        if dim=='3d':
            SuperCell = (8, 8, 4)
        else:
            SuperCell = (16, 16, 1)

        Nx = np.ceil( 1.*Nx / decomposition[0] / SuperCell[0] ) * \
                              decomposition[0] * SuperCell[0]
        Ny = np.ceil( 1.*Ny / decomposition[1] / SuperCell[1] ) * \
                              decomposition[1] * SuperCell[1]
        Nz = np.ceil( 1.*Nz / decomposition[2] / SuperCell[2] ) * \
                              decomposition[2] * SuperCell[2]

        dx = xmax/Nx
        dy = ymax/Ny
        dz = zmax/Nz

        params['Nx'] = np.int(Nx)
        params['Ny'] = np.int(Ny)
        params['Nz'] = np.int(Nz)
        params['Nsteps'] = Nsteps
        params['CELL_WIDTH_SI'] = dx
        params['CELL_HEIGHT_SI'] = dy
        params['CELL_DEPTH_SI'] = dz

        if dt is not None:
            if dt_fromCFL is not None:
                print("Either `dt_fromCFL` or `dt` should be given, not both")
            params['DELTA_T_SI'] = dt
        else:
            if dt_fromCFL is None:
                print("Give either `dt_fromCFL` or `dt`")
            params['DELTA_T_SI'] = dt_fromCFL/c * (dx**-2+dy**-2+dz**-2)**-.5

        if absorber is None:
            params['absorber'] = {}
            params['absorber']["Cells"] = ( (32, 32),
                                            (64, 64),
                                            (32, 32) )
            params['absorber']["Strength"] = ( (1e-3, 1e-3),
                                               (1e-3, 1e-3),
                                               (1e-3, 1e-3) )
        else:
            params['absorber'] = absorber

        if movingWindow:
            params['movingWindow'] =  "-m"
        else:
            params['movingWindow'] =  ""

        params['movePoint'] = movePoint

        for i_comp, comp in enumerate(('x', 'y', 'z')):
            for i_lim, lim in enumerate(('min', 'max')):

                params[ f'ABSORBER_CELLS_{comp}{lim}' ] = \
                    params['absorber']["Cells"][i_comp][i_lim]

                params[ f'ABSORBER_STRENGTH_{comp}{lim}' ] = \
                    params['absorber']["Strength"][i_comp][i_lim]

        params['Solver'] = type
        if J_smoothing is None:
            params['CurrentInterpolation'] = 'None'
        else:
            params['CurrentInterpolation'] = J_smoothing

        # Grid template
        template_grid = {}
        template_grid['filename'] = 'grid.template'
        template_grid['MainArgs'] = params

        # Dimension template
        template_dim = {}
        template_dim['filename'] = 'dimension.template'
        template_dim['MainArgs'] = params

        # Solver template
        template_solver = {}
        template_solver['filename'] = 'fieldSolver.template'
        template_solver['MainArgs'] = params

        # Run script template
        template_run = {}
        template_run['filename'] = 'run.template'
        template_run['MainArgs'] = params

        self.templates = [template_grid, template_dim, template_solver, template_run]
