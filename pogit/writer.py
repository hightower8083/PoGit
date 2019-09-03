from mako.template import Template
import os

from pogit import __path__ as src_path
templatePath = src_path[0] + '/templates/'

def WriteSimulationFiles( objs ):
    """
    Method which renders all temaplates from the given objects
    and writes the files. Must be called in the directory, where
    `./include/picongpu/param/` and `./etc/picongpu/` exist
    """

    # Define the output folders
    path_include = './include/picongpu/param/'
    path_etc = './etc/picongpu/'

    # Create folders if needed (for tests)
    for p in (path_include, path_etc):
        if os.path.exists(p) == False :
            try:
                os.makedirs(p)
            except OSError :
                pass

    # List all template files affected by the objects
    FilesList = []
    for obj in objs:
        for objectTemplate in obj.templates:
            if objectTemplate['filename'] not in FilesList:
                FilesList.append(objectTemplate['filename'])

    # Render all listed template files from all objects
    for filename in FilesList:
        # create Mako template
        template = Template( filename=templatePath+filename )

        # define dictionaries for main and appendable arguments
        templateMain = {}
        templateAppendable = {}
        MainDone = False

        # loop through the objects
        for obj in objs:
            # loop through the templates of the object
            for objectTemplate in obj.templates:
                # check if object affects current template file
                if objectTemplate['filename'] != filename:
                    continue

                args = objectTemplate.keys()  # object arguments list

                # Add main template arguments (once per template)
                if 'Main' in args and not MainDone:
                    templateMain = objectTemplate['Main']
                    MainDone = True

                # check if object has any appendable codelets are defined
                if 'Appendable' not in args:
                    continue

                # separator is something like '\n', ',\n', ' '
                for separator in objectTemplate['Appendable'].keys():
                    # initialize separator dictionary if needed
                    if separator not in templateAppendable.keys():
                        templateAppendable[separator] = {}

                    # append object codelets to corresponding template lists
                    args = objectTemplate['Appendable'][separator].keys()
                    for arg in args:
                        # initialize a list for the codelet if needed
                        if arg not in templateAppendable[separator].keys():
                            templateAppendable[separator][arg] = []

                        # append codelet to the template list
                        templateAppendable[separator][arg].append( \
                            objectTemplate['Appendable'][separator][arg])

        # join appendable codelets with proper separators
        for separator in templateAppendable.keys():
            for arg in templateAppendable[separator].keys():
                # Do only for non-empty lists
                if len(templateAppendable[separator][arg])>0:
                    templateAppendable[separator][arg] = \
                        separator.join(templateAppendable[separator][arg])

        # Merge all arguments into a master dictionary
        templateArgs = { **templateMain}
        for separator in templateAppendable.keys():
            templateArgs = {**templateArgs, **templateAppendable[separator]}

        # render the template and write the files
        if filename.split('.')[0] == 'run':
            filename_dest = filename.replace('template', 'cfg')
            with open(path_etc + filename_dest, mode='w') as file:
                file.writelines(template.render(**templateArgs))
        else:
            filename_dest = filename.replace('template', 'param')
            with open(path_include+filename_dest, mode='w') as file:
                file.writelines(template.render(**templateArgs))

        # print the name of the file
        print('\t', filename_dest)

def WriteAndSubmit( objs, sim_name='run', output_path="$PIC_SCRATCH",
                    write_input=True, build=True, run=True, s='bash',
                    t='etc/picongpu/bash/mpiexec.tpl' ):
    """
    Convenience method to generate the simulation files, build the code and
    runs the simulation locally
    NB: this method does some forced folders removal, should be used
    with care!
    """

    # Generate the param files
    if write_input:
        print('*** GENERATE THE SIMULATION INPUT')
        WriteSimulationFiles( objs )

    # Build PIConGPU
    if build:
        print('*** BUILD PIConGPU')
        # Clean the previous build
        os.system(f'rm -rf .build')
        os.system('pic-build >/dev/null 2>&1')

    # Run the simulation using local bash submission
    if run:
        # Clean the previous output folders
        print('*** REMOVE THE USED FOLDERS')
        os.system(f'rm -rf {output_path}/{sim_name}')

        print('*** RUN THE SIMULATION')
        os.system( f'tbg -s {s} -c etc/picongpu/run.cfg -t {t} '+\
                   f'{output_path}/{sim_name} > log &' )
