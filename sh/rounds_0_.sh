#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J S0 # job name
#SBATCH -N 1 # number of nodes
#SBATCH -n 11 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o S0.out # STDOUT
#SBATCH -e S0.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(-2.0);exit;'
