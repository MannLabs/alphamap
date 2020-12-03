# AlphaMap
> A python-based library that enables the exploration of proteomic datasets on the peptide level. 


## Installation instructions

We recommend the Anaconda or Miniconda Python distribution, which comes with a powerful package manager. 

It is recommended to install AlphaMap in its own environment.

1. Open the console and create a new conda environment: conda create --name alphamap python=3
2. Activate the environment: conda activate alphamap
3. Redirect to the folder of choice and clone the repository: git clone git@github.com:MannLabs/pepmap.git
4. Navigate to the alphamap folder and install the package with pip install . (default users) or with pip install -e . to enable developers mode.
5. If AlphaMap is installed correctly, you should be able to import alphamap as a package within the environment; see below.

If you would like to use AlphaMap in a jupyter notebook environment, additionally install nb_conda: conda install nb_conda.

## How to use

### Load fasta 

```python
#from pyteomics import fasta
#full_human_fasta = fasta.IndexedUniProt('../data/human.fasta')
```

### Import data MS data

```python
# from pepmap.importing import import_data
```

Import the entire dataset

```python
# data_all = import_data('testdata/test_spectronaut_input.csv')
```

Import a single raw file

```python
# data_raw_01 = import_data('testdata/test_spectronaut_input.csv', sample="raw_01")
```

Import a selection of multiple raw files

```python
# data_raw_01_raw_02 = import_data('testdata/test_spectronaut_input.csv', sample=["raw_01", "raw_02"])
```

### Data preprocessing

```python
# from pepmap.preprocessing import format_input_data
```

```python
# formatted_proteome_data = format_input_data(df = data_all, fasta = full_human_fasta)
```

### Data visualization

```python
#plot_peptide_traces(formatted_proteome_data,
#                    name = 'proteome',
#                    protein = "P37802",
#                    fasta = full_human_fasta,
#                    uniprot=uniprot_annotation,
#                    selected_features=all_annotatins,
#                    uniprot_feature_dict=uniprot_feature_dict, 
#                    uniprot_color_dict=uniprot_color_dict)
```
