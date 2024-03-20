# Evolution of cooperation among individuals with limited updating payoff memory

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A repository for the project "Evolution of cooperation among individuals with
limited payoff memory," a collaboration with [@chilbe3](https://twitter.com/chilbe3)
and Alex McAvoy, at the [Max Planck Research Group Dynamics of Social Behavior](https://www.evolbio.mpg.de/socialdynamics).

Preprint: https://arxiv.org/abs/2311.02365.

## Software

The code for simulating the evolutionary process described in the paper has been
implemented in Matlab. The code used for the results can be found in the folder
`matlab`.

As Matlab is not an open-source language, we have also implemented the process
in Python. Note that the Python code is slower.

### Installation

To use the source code (Python or Matlab), you will first need to clone the
repository locally to your computer. You just need to run the following command
in the terminal:

```shell
$ git clone git@github.com:Nikoleta-v3/evolution-of-cooperation-with-limited-updating-payoff-memory.git
```

## Analysis

The simulations have been run on the supercomputer. We acknowledge and are
thankful to the Scientific Compute Cluster at GWDG, the joint data center of the
Max Planck Society for the Advancement of Science (MPG), and the University of
Göttingen.

For the results, the evolutionary process when the updating considers the two
last rounds with two interactions and the results for higher mutation have the
longest running times. We recommend running them on a remote computer.

The data generated from running the processes have been archived. However, if
you want to reproduce the work, you can use the Matlab scripts (see [README.md](matlab/README.md)).

The scripts output a `.csv` files with the residents at different time steps of
the evolutionary process. You need to run the script `clean_data.py`, which can
be found in the folder `scripts`, before running the analysis.

## Figures

The analysis and figures have been created using Jupyter Notebooks. Before
running the analysis, you have to download the simulation data. They are
archived in Zenodo: [link here](https://zenodo.org/record/7664286#.Y_YDWS0w2hk).

The notebooks for the figures can be found in the folder `nbs`.

The analysis only uses basic Python packages that should be installed with your
Python. However, we have created an environment file. To install it, navigate to
the project using the terminal and run the command:

```shell
$ conda env create -f environment.yml
```

This installs all the dependencies on a `conda` environment. You can activate
the environment by running:

```shell
$ conda activate stochastic-payoffs
```

The environment can also appear in your Jupyter Notebook by running the
following command:

```shell
$ python -m ipykernel install --user --name stochastic-payoffs --display-name stochastic-payoffs
```

## Paper

The paper and supplementary information are written in LaTeX. All the necessary
files to compile the documents can be found in the folder `paper`.

## License

The repository is under an MIT license.

## Contributions

All contributions are welcome, whether they are in the form of code, feedback, or reporting issues.

## Python

As a reminder, the Python code for the evolutionary process is rather slow, so
we recommend using the Matlab code. We are working on creating a more efficient
Python code for such processes.

To install the Python package, navigate to the repository using the terminal.
Once you are there, run the following command:

```shell
$ python setup.py install
```

### Tests

The Python code for the project has been developed using test-driven
development.

To run the test suite and the test suite's coverage, run the following command
(while the environment is activated):

```shell
$ pytest --cov=src tests/
```