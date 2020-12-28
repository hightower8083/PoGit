from mako.template import Template
from scipy.constants import c
import numpy as np

from .codelets.run import plugins

class Plugin:
    """
    Class that adds the pluging
    Main attributes
    ---------------
        List of `templates`, which are to be rendered in the
        following files:
            etc/picongpu/run.cfg
    """

    def __init__( self, type="openPMD", period=0,
                  source="fields_all, species_all",
                  name='raw', **kw_args ):

        params = {}
        params["name"] = name
        params["period"] = str(int(period))
        params["source"] = source

        params = { **params, **kw_args}

        template_run = {}
        template_run['filename'] = 'run.template'

        template_run['Appendable'] = {}
        template_run['Appendable']['\n'] = {}
        template_run['Appendable'][' '] = {}

        template_run['Appendable']['\n']['Plugin']=\
            Template(plugins[type]).render(**params)

        template_run['Appendable'][' ']['PluginName'] = \
            f"!TBG_{name}_{period:d}"

        self.templates = [template_run, ]
