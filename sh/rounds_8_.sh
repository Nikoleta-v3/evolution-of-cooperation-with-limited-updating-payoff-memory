#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J S8 # job name
#SBATCH -N 1 # number of nodes
#SBATCH -n 11 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o S8.out # STDOUT
#SBATCH -e S8.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(1.2);exit;'
