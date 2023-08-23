# Concensus Pharmacophore

[**Description**](#description) | [**Requirements**](#requirements) | [**Installation**](#installation) | [**Tutorials**](#tutorials) | [**Citation**](#citation) | [**License**](#license) | [**Information**](#information) | [**Disclaimer**](#disclaimer)


[![DOI](https://zenodo.org/badge/680058699.svg)](https://zenodo.org/badge/latestdoi/680058699)


## Description

A consensus pharmacophore is a set of properties shared by several active molecules that bind to the same target. It is composed of geometric elements such as points, spheres, vectors, or planes that represent different types of features such as hydrophobic regions, hydrogen bond donors or acceptors, aromatic rings, or positive or negative charges. It can be used to represent the fundamental properties of a molecular interaction and to direct the development of new compounds with comparable or improved activity.

The consensus pharmacophore as Ligand-based method for examining the chemical structures of known active compounds in order to determine the common features that account for their activity. Using the three-dimensional structure of the target protein and its bound ligands, it can provide information about the interaction site and extract the key features required for binding.

A consensus pharmacophore can also be used to identify new potential ligands that match the features of the target and are likely to bind to it. This technique is known as pharmacophore matching, and it is useful for identifying drug targets and performing virtual screening.

This library was developed to generate concensus pharmacophores from large datasets of ligands and ligand-protein complexes.  

Question about usage or troubleshooting? Please leave a comment in the discussion section of this repo

## Requirements

ConPhar is reliant on a variety of academic software:

- [Pharmer/Pharmit](https://pharmit.csb.pitt.edu/) 

- pandas
- pymol
- plotly
- seaborn
- scikit-learn

## Installation 

```
pip install conphar
```

## Tutorials
> [Ligand-Receptor pharmacophores](https://github.com/AngelRuizMoreno/ConcensusPharmacophore/blob/main/tutorials/ReceptorLigandPharmacophores.ipynb)

> [Generate Consensus Pharmacophore](https://github.com/AngelRuizMoreno/ConcensusPharmacophore/blob/main/tutorials/ConsensusPharmacophore.ipynb)

## Citation

If you use this software or its results in your research, publication, or project, please cite it as follows:

> ConPhar: Tool for generation and analysis of concensus pharmacophore: [DOI: 10.5281/zenodo.8276506](https://zenodo.org/record/8276506)


If you use pharmer for your work you must cite:

> Koes, D.R., & Camacho, C.J. (2011). Pharmer: Efficient and Exact Pharmacophore Search. Journal of chemical information and modeling, 51 6, 1307-14 .

If you use Pharmit in your work you must cite:

> Sunseri, J., & Koes, D.R. (2016). Pharmit: interactive exploration of chemical space. Nucleic Acids Research, 44, W442 - W448.


## License

This tool is under MIT license, see the LICENSE file for details.

## Information

- This library works with pharmacophores generated with [pharmer](https://sourceforge.net/projects/pharmer/) and/or [pharmit](https://pharmit.csb.pitt.edu/). An executable version of pharmit is included in this library but works only for linux.

Users can generate their pharmacophores and use this library for analysis. Check tutorials for more information.


## Disclaimer 

This software is still under development and may contain bugs or errors. The developers do not guarantee the accuracy, completeness, or reliability of the software or its results. Use it at your own risk and discretion. The software is provided "as is" without any warranty of any kind, either express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. The developers are not liable for any damages, losses, or costs arising from the use of the software or its results.