# MATLAB Source Code

In this folder, you can find all the necessary files to reproduce the results
presented in the manuscript.

There are some function files that act as helper functions. These can be found
in the `tools` folder. You will need to add the MATLAB files under `tools` to
your path.

The following files are for simulating the evolutionary process and for
obtaining most of the results. Because we are considering different rules based
on how updating occurs, the processes slightly differ, and thus we consider
three files:

- `evolSimulation.m` is the code for the evolutionary process when updating is
  done based on the expected, last round, and one opponent average payoff.
- `evolSimulationUpdatingMemoryTwo.m` is the code for the evolutionary process
  when updating is done based on the last two rounds or last two interactions.
- `evolSimulationUpdatingMemoryTwo.m` is the code for the evolutionary process
  when updating is done based on the last two rounds of the last two
  interactions.

The file `evolRun.m` is the script for running these processes and obtaining the
results. The file includes documentation on how to use and run each of these
processes, such as documentation about the input arguments.

For the two further cases considered in the Electronic Supplementary
Information, namely the case of memory-1 strategies and of higher mutation, the
code is in the folder `beyond_reactive_and_low_mutation`.

In the root of this directory, the rest of the files are for calculating the
fixation probability of a mutant strategy based on the different updating rules.

The simulations have been run on the supercomputer. We acknowledge the
facilities used for producing the results. This work utilized the Scientific
Compute Cluster at GWDG, the joint data center of Max Planck Society for the
Advancement of Science (MPG), and University of Göttingen.