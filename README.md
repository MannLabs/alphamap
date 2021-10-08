# AlphaMap
> A python-based library that enables the exploration of proteomic datasets on the peptide level.


## About

AlphaMap is a tool for peptide level MS data exploration. You can load and inspect MS data analyzed by [AlphaPept](https://github.com/MannLabs/alphapept), DIA-NN, MaxQuant, Spectronaut or FragPipe. Uploaded data is processed and formatted for visual inspection of the sequence coverage of any selected protein and its identified post-translational modifications (PTMs). UniProt information is available to directly annotate sequence regions of interest such as protein domains, secondary structures, sequence variants, known PTMs, etc. Additionally, users can select proteases to further evaluate the distribution of proteolytic cleavage sites across a protein sequence. The functionality of AlphaMap can be accessed via an intuitive graphical user interface or - more flexibly - as a Python package that allows its integration into common analysis workflows for data visualization. 


## License

AlphaMap was developed by the [Mann Labs at the Max Planck Institute of Biochemistry](https://www.biochem.mpg.de/mann) and is freely available with an [Apache License](LICENSE).


## Installation

AlphaMap can be installed and used on Windows and MacOS.
There are three different types of installation possible:

* [**One-click GUI installer:**](#one-click-gui) Choose this installation if you only want the GUI and/or keep things as simple as possible.
* [**Pip installer:**](#pip) Choose this installation if you want to use AlphaMap as a Python package in an existing Python 3.8 environment (e.g. a Jupyter notebook). If needed, the GUI can be installed with pip as well.
* [**Developer installer:**](#developer) Choose this installation if you are familiar with CLI tools, [conda](https://docs.conda.io/en/latest/) and Python. This installation allows access to all available features of AlphaMap and even allows to modify its source code directly.


### One-click GUI

The GUI of AlphaMap is a completely stand-alone tool that requires no knowledge of Python. Click on one of the links below to download the latest release for:

* [**Windows**](https://github.com/MannLabs/alphamap/releases/latest/download/alphamap_installer_windows.exe)
* [**MacOS**](https://github.com/MannLabs/alphamap/releases/latest/download/alphamap_gui_installer_macos.pkg)

***IMPORTANT: Please refer to the [GUI manual](alphamap/data/alphamap_tutorial.pdf) for detailed instructions on the installation, troubleshooting and usage of the stand-alone AlphaMap GUI.*** 

***IMPORTANT***: The one-click-installers on macOS and Windows require **at least macOS Catalina (10.15) or higher** and **Windows 10** respectively. For Windows, a system update might be necessary in case older versions do not work. To prevent installation errors on **Windows**, we recommend **uninstalling the previous AlphaMap version before installing a new one**.

### Pip

AlphaMap can be installed in an existing Python 3.8 environment with a single `bash` command. *This `bash` command can also be run directly from within a Jupyter notebook by prepending it with a `!`*.

```bash
pip install alphamap
```

When a new version of AlphaMap becomes available, the old version can easily be upgraded by running e.g. the command again with an additional `--upgrade` flag:

```bash
pip install alphamap --upgrade
```

NOTE: When installing with `pip`, UniProt information is not included. Upon first usage of a specific Organism, its information will be automatically downloaded from UniProt.


### Developer

AlphaMap can also be installed in editable (i.e. developer) mode with a few `bash` commands. This allows to fully customize the software and even modify the source code to your specific needs. When an editable Python package is installed, its source code is stored in a transparent location of your choice. While optional, it is advised to first (create and) navigate to e.g. a general software folder:

```bash
mkdir ~/folder/where/to/install/software
cd ~/folder/where/to/install/software
```

Next, download the AlphaMap repository from GitHub either directly or with a `git` command. This creates a new AlphaMap subfolder in your current directory.

```bash
git clone https://github.com/MannLabs/alphamap.git
cd alphamap
```

For any Python package, it is highly recommended to use a [conda virtual environment](https://docs.conda.io/en/latest/). AlphaMap can either be installed in a new conda environment or in an already existing environment. *Note that dependency conflicts can occur with already existing packages in the latter case*! Once a conda environment is activated, AlphaMap and all its [dependencies](requirements) need to be installed.

```bash
conda create -n alphamap python=3.8 -y
conda activate alphamap
pip install -e .
```

* By using the editable flag `-e`, all modifications to the AlphaMap [source code folder](alphamap) are directly reflected when running AlphaMap. Note that the AlphaMap folder cannot be moved and/or renamed if an editable version is installed.

* When using Jupyter notebooks and multiple conda environments direcly from the terminal, it is recommended to `conda install nb_conda_kernels` in the conda base environment. Hereafter, running a `jupyter notebook` from the conda base environment should have a `python [conda env: alphamap]` kernel available, in addition to all other conda kernels in which the command `conda install ipykernel` was run.


## Test data

AlphaMap has direct data import options for AlphaPept, DIA-NN, MaxQuant, Spectronaut and FragPipe.

### AlphaPept
AlphaMap takes the *results.csv* file from AlphaPept as input format. An example is available for [download here](https://github.com/MannLabs/alphamap/releases/download/v0.0.210730-alpha/test_alphapept_input.csv).

### DIA-NN
AlphaMap takes the peptide-level output .tsv file from DIA-NN as input format. An example is available for [download here](https://github.com/MannLabs/alphamap/releases/download/v0.0.210730-alpha/test_diann_input.tsv).

### MaxQuant
AlphaMap takes the *evidence.txt* file from MaxQuant as input format. A reduced example file is available for [download here](https://github.com/MannLabs/alphamap/releases/download/v0.0.210622-alpha/test_maxquant_input.txt).

### Spectronaut
AlphaMap takes Spectronaut results exported in normal long format (.csv or .tsv) as input. Necessary columns include:
* PEP.AllOccuringProteinAccessions
* EG.ModifiedSequence
* R.FileName

To ensure proper formatting of the Spectronaut output, an export scheme is available for [download here](https://github.com/MannLabs/alphamap/blob/master/alphamap/data/spectronaut_export_scheme.rs).

A reduced example file is also available for [download here](https://github.com/MannLabs/alphamap/releases/download/v0.0.210622-alpha/test_spectronaut_input.tsv).
<!-- It is not directly clear how to download this individual file from here. Luckily, the two larger ones have a "download" button on the top right -->

### FragPipe
There are two options to visualize data analyzed by FragPipe:
1) Upload individual **"peptide.tsv"** files for single MS runs. A reduced example file is available for [download here](https://github.com/MannLabs/alphamap/releases/download/0.1.3/test_fragpipe_input.tsv).

2) Upload the **"combined_peptide.tsv"** file with the joint information about peptides identified in all runs (there is an option to select the experiment(s)). Be aware that the combined_peptide.tsv does not provide information about PTM localization. PTMs are therefore not shown for this option. A reduced example file is available for [download here](https://github.com/MannLabs/alphamap/releases/download/0.1.3/combined_peptide.txt).

## Usage

There are two ways to use AlphaMap:

* [**GUI:**](#gui) This allows to interactively import and visualize the data.
* [**Python:**](#python-and-jupyter-notebooks) This allows to access data and explore it interactively with custom code.

NOTE: The first time you use a fresh installation of AlphaMap, it is often quite slow because some functions might still need compilation on your local operating system and architecture. Subsequent use should be a lot faster.

### GUI

Please refer to the [GUI manual](https://github.com/MannLabs/alphamap/blob/master/alphamap/data/alphamap_tutorial.pdf) for detailed instructions on the installation and usage of the stand-alone AlphaMap GUI.

If the GUI was not installed through a one-click GUI installer, it can be activated with the following `bash` command:

```bash
alphamap
```

Note that this needs to be prepended with a `!` when you want to run this from within a Jupyter notebook. When the command is run directly from the command-line, make sure you use the right environment (activate it with e.g. `conda activate alphamap` or set an alias to the binary executable).

### Python and Jupyter notebooks

AlphaMap can be imported as a Python package into any Python script or notebook with the command `import alphamap`.

A Jupyter notebook tutorial ['Workflow.ipynb'](Workflow.ipynb) is available to demonstrate how to load AlphaMap as python module and hot to visualize data interactively. When running locally it provides interactive plots, which are not rendered on GitHub.

AlphaMap includes fasta files and UniProt annotations for: 'Human', 'Mouse', 'Rat', 'Cow', 'Zebrafish', 'Drosophila', 'Caenorhabditis elegans', 'Slime mold', 'Arabidopsis thaliana', 'Rice', 'Escherichia coli', 'Bacillus subtilis', 'Saccharomyces cerevisiae', 'SARS-COV' and 'SARS-COV-2'. If additional organisms are of interest, corresponding .fasta files and sequence annotations can be downloaded directly from UniProt. A Jupyter notebook tutorial ['Uniprot_preprocessing.ipynb'](Uniprot_preprocessing.ipynb) shows how to load and format a UniProt annotation file.

