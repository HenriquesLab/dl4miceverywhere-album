###album catalog: cellcanvas

# Based on https://github.com/HenriquesLab/DL4MicEverywhere/blob/main/notebooks/ZeroCostDL4Mic_notebooks/U-Net_3D_DL4Mic/configuration.yaml
# and https://github.com/betaseg/solutions/blob/main/solutions/io.github.betaseg/cellsketch-plot/solution.py

from album.runner.api import setup
import subprocess

try:
    subprocess.check_output('nvidia-smi')
    gpu_access = True
except Exception: 
    gpu_access = False

def install():
    from album.runner.api import get_app_path
    from git import Repo
    import subprocess
    import requests
    import shutil
    import os

    # Clone the DL4MicEverywhere repository
    clone_url = "https://github.com/HenriquesLab/DL4MicEverywhere"
    repository_path = get_app_path().joinpath("DL4MicEverywhere")
    Repo.clone_from(clone_url, repository_path)
    assert (repository_path.exists())

    # URL of the notebook you want to download
    notebook_url = "https://raw.githubusercontent.com/HenriquesLab/ZeroCostDL4Mic/master/Colab_notebooks/U-Net_3D_ZeroCostDL4Mic.ipynb"
    
    notebook_path = get_app_path().joinpath("U-Net_3D_ZeroCostDL4Mic.ipynb")
    notebook_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(notebook_url)
    response.raise_for_status()
    
    with open(notebook_path, 'wb') as notebook_file:
        notebook_file.write(response.content)
    
    assert notebook_path.exists(), "Notebook download failed"

    # Convert the notebook to its colabless form
    section_to_remove = "1.1. 1.2. 2. 6.2."
    section_to_remove = section_to_remove.split(' ')
    
    python_command = ["python", ".tools/notebook_autoconversion/transform.py", "-p", f"{get_app_path()}", "-n", "U-Net_3D_ZeroCostDL4Mic.ipynb", "-s"]
    python_command += section_to_remove

    subprocess.run(python_command, cwd=repository_path)
    subprocess.run(["mv", get_app_path().joinpath("colabless_U-Net_3D_ZeroCostDL4Mic.ipynb"), get_app_path().joinpath("U-Net_3D_ZeroCostDL4Mic.ipynb")])

    # Remove the cloned DL4MicEverywhere repository
    if os.name == 'nt':
        os.system(f'rmdir /s /q "{to}"')
    else:
        # rmtree has no permission to do this on Windows
        shutil.rmtree(repository_path) 

def run():
    from album.runner.api import get_args, get_app_path
    import subprocess
    import os

    # Fetch arguments and paths
    args = get_args()
    app_path = get_app_path()
    
    # Path to the downloaded notebook
    notebook_path = app_path.joinpath("U-Net_3D_ZeroCostDL4Mic.ipynb")

    # Ensure the notebook exists
    assert notebook_path.exists(), "Notebook does not exist"

    # Output path for running the notebook
    output_path = args.path
    os.makedirs(output_path, exist_ok=True)
    print(f"Saving output to {output_path}")

    # Set the LD_LIBRARY_PATH to allow TensorFlow to find the CUDA libraries
    global gpu_access
    if gpu_access:
        os.environ["LD_LIBRARY_PATH"] = f"{os.environ['LD_LIBRARY_PATH']}:{os.environ['CONDA_PREFIX']}/lib"

    # Optionally, launch the Jupyter notebook to show the results
    subprocess.run(["jupyter", "lab", str(notebook_path)], cwd=str(output_path))

if gpu_access:
    channels = """
- conda-forge
- nvidia
- anaconda
- defaults
"""
    dependencies = """
- python=3.10
- cudatoolkit=11.8.0
- cudnn=8.9.2
- pip
- pkg-config
"""
else:
    channels = """
- conda-forge
- defaults
"""
    dependencies = f"""
- python=3.10
- pip
- pkg-config
"""

env_file = f"""
channels:
{channels}
dependencies:
{dependencies}
- pip:
    - GitPython==3.1.43 
    - PTable==0.9.2
    - bioimageio.core==0.5.9
    - data==0.4
    - elasticdeform==0.5.0
    - fpdf2==2.7.4
    - future==0.18.3
    - google==2.0.3
    - h5py==3.8.0
    - imageio==2.25.1
    - imgaug==0.4.0
    - ipywidgets==8.0.7
    - matplotlib==3.7.1
    - numpy==1.22.4
    - pandas==1.5.3
    - pip==23.1.2
    - requests==2.27.1
    - scikit-image==0.19.3
    - scipy==1.10.1
    - tensorflow==2.12.0
    - tifffile==2023.7.10
    - tqdm==4.65.0
    - wget==3.2
    - zarr==2.15.0
    - nbformat==5.9.2
    - jupyterlab==3.4.0
"""

setup(
    group="DL4MicEverywhere",
    name="u-net-3d-zerocostdl4mic",
    version="2.2.1",
    solution_creators=["DL4MicEverywhere team", "album team"],
    title="u-net-3d-zerocostdl4mic implementation.",
    description="3D binary segmentation. The 3D U-Net was first introduced by Çiçek et al for learning dense volumetric segmentations from sparsely annotated ground-truth data building upon the original U-Net architecture by Ronneberger et al. Note - visit the ZeroCostDL4Mic wiki to check the original publications this network is based on and make sure you cite these.",
    documentation="https://raw.githubusercontent.com/HenriquesLab/ZeroCostDL4Mic/master/BioimageModelZoo/README.md",
    tags=['AMD64', 'colab', 'notebook', 'U-Net', 'segmentation', 'ZeroCostDL4Mic', '3D', 'dl4miceverywhere'],
    args=[{
        "name": "path",
        "type": "string",
        "default": ".",
        "description": "What is your working path?"
    }],
    cite=[{'doi': 'https://doi.org/10.1038/s41467-021-22518-0', 'text': 'von Chamier, L., Laine, R.F., Jukkala, J. et al. Democratising deep learning for microscopy with ZeroCostDL4Mic. Nat Commun 12, 2276 (2021). https://doi.org/10.1038/s41467-021-22518-0'}, {'text': 'Özgün Çiçek, Ahmed Abdulkadir, Soeren S. Lienkamp, Thomas Brox, Olaf Ronneberger. 3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation. https://arxiv.org/abs/1606.06650', 'url': 'https://arxiv.org/abs/1606.06650'}],
    album_api_version="0.5.1",
    covers=[],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
