from mako.template import Template
import os

from pogit import __path__ as src_path
templatePath = src_path[0] + '/templates/'

def WriteSimulationFiles( objs ):
    """
    Method which renders all temaplates from the given objects
    and writes the files.
    """

    # Define and if needed create the output folders
    path_include = './include/picongpu/param/'
    path_etc = './etc/picongpu/'

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
        templateMainArgs = {}
        templateAppendableArgs = {}
        templateCommaAppendableArgs = {}
        templateSpaceAppendableArgs = {}

        # loop through the objects
        for obj in objs:
            # loop through the templates of the object
            for objectTemplate in obj.templates:
                # check if objects affects current template file
                if objectTemplate['filename'] != filename:
                    continue

                # Add main template arguments (once per template)
                objectArgs = objectTemplate.keys()
                if 'MainArgs' in objectArgs:
                    templateMainArgs = objectTemplate['MainArgs']

                # Make lists of appendable codelets
                for templateArgsStr, templateArgs in (
                    ('AppendableArgs', templateAppendableArgs),
                    ('CommaAppendableArgs', templateCommaAppendableArgs),
                    ('SpaceAppendableArgs', templateSpaceAppendableArgs) ):
                    if templateArgsStr not in objectArgs:
                        continue

                    for arg in objectTemplate[templateArgsStr].keys():
                        if arg not in templateArgs.keys():
                            templateArgs[arg] = []

                        templateArgs[arg].append(
                            objectTemplate[templateArgsStr][arg] )

        # Stack appendable codelets (reduce lists to strings)
        for templateArgs, join_str in ( (templateAppendableArgs, '\n'),
                                        (templateCommaAppendableArgs, ',\n'),
                                        (templateSpaceAppendableArgs,' ') ):
            for arg in templateArgs.keys():
                if len(templateArgs[arg])>0:
                    templateArgs[arg] = join_str.join( templateArgs[arg] )

        """
        for arg in templateAppendableArgs.keys():
            templateAppendableArgs[arg] = '\n'.join( \
                templateAppendableArgs[arg] )

        for arg in templateCommaAppendableArgs.keys():
            if len(templateCommaAppendableArgs[arg])>0:
                templateCommaAppendableArgs[arg] = ',\n'.join( \
                    templateCommaAppendableArgs[arg] )

        for arg in templateSpaceAppendableArgs.keys():
            templateSpaceAppendableArgs[arg] = ' '.join( \
                templateSpaceAppendableArgs[arg] )
        """

        templateArgs = { **templateMainArgs,
                         **templateAppendableArgs,
                         **templateCommaAppendableArgs,
                         **templateSpaceAppendableArgs }

        if filename.split('.')[0] == 'run':
            filename_dest = filename.replace('template', 'cfg')
            with open(path_etc + filename_dest, mode='w') as file:
                file.writelines(template.render(**templateArgs))
        else:
            filename_dest = filename.replace('template', 'param')
            with open(path_include+filename_dest, mode='w') as file:
                file.writelines(template.render(**templateArgs))

        print(filename_dest)
