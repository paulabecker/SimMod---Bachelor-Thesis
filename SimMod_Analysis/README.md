# SimMod - Analysis
This directory contains various Jupyter Notebooks used for preprocessing, analyzing, and plotting SimMod data. The primary aim is to provide a reproducible data handling and evaluation pipeline. All data (raw and interim) is stored in the [data](data) folder.

While the sections below give a rough overview of the evaluation scripts, short descriptions can be found at the top of each Notebook.

## Preprocessing
Contains [preprocessing scripts](preprocessing) for easier data handling, e.g., the preparation of the SimMod input data from the raw RCP data, the creation of a combined dataset containing all available temperature observations, etc.

## Visualizing SimMod output
A set of plotting scripts for exploring the SimMod output and comparing ot to literature values is available in the [Exploring](Exploring) and [Direct_Comparison](Direct_Comparison) folders.

## TCR Analysis
The (Implied) TCR Analysis follows the paper of [Hausfather et al., 2020](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2019GL085378). The [original evaluation scripts](https://github.com/hausfath/OldModels/tree/master/notebooks) were adapted and extended.
