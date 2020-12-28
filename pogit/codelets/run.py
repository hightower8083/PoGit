# Plugins are desctibed here

plugins = {}


"""
OpenPMD data output to hdf5 files
Parameters:
-----------
    name : string
      File names of the written
      Default is 'raw'

    period : integer or string
      Period of data writing. Can be either integer or in
      the format of `<start>:<end>[:<period>]`
      Default is 1

    source : string
      Select data sources to dump
      Default is `species_all, fields_all`
"""
plugins["hdf5"] = \
"""
TBG_${name}_${period}="--hdf5.period ${period} --hdf5.file ${name} --hdf5.source '${source}'" """


plugins["openPMD"] = \
"""
TBG_${name}_${period}="--openPMD.period ${period} --openPMD.file ${name} --openPMD.source '${source}' --openPMD.ext h5" """

