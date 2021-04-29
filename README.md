# AlphaMap
> A python-based library that enables the exploration of proteomic datasets on the peptide level.


## Description

AlphaMap is a tool for peptide level MS data exploration. You can load and inspect MS data analyzed by either MaxQuant or Spectronaut. Uploaded data is processed and formatted for visual inspection of the sequence coverage of any selected protein and its identified post-translational modifications (PTMs). UniProt information is available to directly annotate sequence regions of interest such as protein domains, secondary structures, sequence variants, known PTMs, etc.

## Installation instructions

We recommend the Anaconda or Miniconda Python distribution, which comes with a powerful package manager.

It is recommended to install AlphaMap in its own environment.

1. Open the console and create a new conda environment: conda create --name alphamap python=3
2. Activate the environment: conda activate alphamap
3. Redirect to the folder of choice and clone the repository: git clone git@github.com:MannLabs/alphamap.git
4. Navigate to the alphamap folder and install the package with pip install . (default users) or with pip install -e . to enable developers mode.
5. If AlphaMap is installed correctly, you should be able to import alphamap as a package within the environment; see below.

If you would like to use AlphaMap in a jupyter notebook environment, additionally install nb_conda: conda install nb_conda.

## How to use

### Import MS data

```python
from alphamap.importing import import_data
```

Import the entire dataset

```python
data_all = import_data('../testdata/test_maxquant_input.txt',
                       verbose = False)
```

Import a single or multiple selected raw files

```python
# single selected raw file
data_raw_01 = import_data('../testdata/test_maxquant_input.txt',
                          sample="raw_1",
                          verbose = False)

# multiple selected raw files
data_raw_01_raw_02 = import_data('../testdata/test_spectronaut_input.csv',
                                 sample=["raw_01", "raw_02"],
                                 verbose = False)
```

### Data preprocessing

```python
from alphamap.preprocessing import format_input_data
from pyteomics import fasta
full_human_fasta = fasta.IndexedUniProt('../data/human.fasta')
```

```python
formatted_proteome_data = format_input_data(df = data_all,
                                            fasta = full_human_fasta,
                                            modification_exp = r'\[.*?\]')
```

### Data visualization

```python
from alphamap.sequenceplot import plot_peptide_traces, uniprot_color_dict
from alphamap.uniprot_integration import uniprot_feature_dict
import pandas as pd
uniprot_annotation = pd.read_csv('../data/preprocessed_uniprot_human.csv',low_memory=False)
```

```python
#hide_output
plot_peptide_traces(formatted_proteome_data,
                    name = 'proteome',
                    protein = "Q9Y2V2",
                    fasta = full_human_fasta,
                    uniprot=uniprot_annotation,
                    selected_features=["STRUCTURE","MOD_RES", "DOMAIN"],
                    uniprot_feature_dict=uniprot_feature_dict,
                    uniprot_color_dict=uniprot_color_dict)
```




![png](docs/images/output_17_0.png)
