import yaml
import sys
import os

def main(dl4miceverywhere_path=None, dl4miceverywhere_album_path=None):

    # Check if paths to the repositories have been provided and if not, it will be assumed that they are located in the same folder.
    if dl4miceverywhere_path is None:
        dl4miceverywhere_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..', 'DL4MicEverywhere'))
    if dl4miceverywhere_album_path is None:
        dl4miceverywhere_album_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))

    # List that will store the notebooks with the new version.
    updated_notebooks = []

    # Go through all the notebooks and check if the version is the same
    dl4miceverywhere_notebooks_path = os.path.join(dl4miceverywhere_path, 'notebooks', 'ZeroCostDL4Mic_notebooks') # TODO: add all the types of notebooks
    dl4miceverywhere_album_solution_path = os.path.join(dl4miceverywhere_album_path, 'solutions', 'DL4MicEverywhere') # TODO: add all the types of notebooks

    dl4miceverywhere_notebooks_list = [e for e in sorted(os.listdir(dl4miceverywhere_notebooks_path)) if os.path.isdir(os.path.join(dl4miceverywhere_notebooks_path, e))]

    for notebook in dl4miceverywhere_notebooks_list:
        # First, get the version from DL4MicEverywhere's configuration
        configuration_path = os.path.join(dl4miceverywhere_notebooks_path, notebook, 'configuration.yaml')

        # Read the information from the configuration
        with open(configuration_path, 'r', encoding='utf8') as f:
            config_data = yaml.safe_load(f)
        
        config_version = config_data['config']['dl4miceverywhere']['notebook_version']

        # Then, get the version from the DL4MicEverywhere-album's solution
        notebook_name = os.path.basename(config_data['config']['dl4miceverywhere']['notebook_url'])
        notebook_name = notebook_name.lower().replace(".ipynb", "").replace("_", "-")
        solution_path = os.path.join(dl4miceverywhere_album_solution_path, notebook_name, 'solution.yml')

        # Read the information from the solution
        with open(solution_path, 'r', encoding='utf8') as f:
            solution_data = yaml.safe_load(f)
        
        solution_version = solution_data['version']

        # Check if they have the same version
        if config_version != solution_version:
            # Check if this solutions has already been tested and if so, don't put it
            # This will avoid the cases that cannot be built to be in loop

            solution_log_path = os.path.join(dl4miceverywhere_path, '.tools', 'solution_log.yml')

            if os.path.exists(solution_log_path):
                # Read the log file
                with open(solution_log_path, 'r', encoding='utf8') as f:
                    solution_log = yaml.safe_load(f)

                if notebook not in solution_log.keys():
                    updated_notebooks.append(notebook)
                else:
                    # We are looking the version on DL4MicEverywhere's config because its 
                    # the one with the latest version and that needs to be tested
                    if config_version not in solution_log[notebook].keys():
                        updated_notebooks.append(notebook)
            else:
                updated_notebooks.append(notebook)

    if len(updated_notebooks) == 0:
        print('')
    else:
        print(' '.join(updated_notebooks))

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # Precondition: Both DL4MicEverywhere and DL4Miceverywhere-album need to be located in the same folder.
        # This can be done on GitHub CI with a double checkout.
        sys.exit(main())
    elif len(sys.argv) == 3:
        # Both paths are provided
        print(f'Path to DL4MicEverywhere folder: {sys.argv[1]}')
        print(f'Path to DL4MicEverywhere-album folder: {sys.argv[2]}')
        sys.exit(main(dl4miceverywhere_path=sys.argv[1], dl4miceverywhere_album_path=sys.argv[2]))
    else:
        sys.exit(1)