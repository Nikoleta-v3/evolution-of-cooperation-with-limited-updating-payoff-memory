#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J S7 # job name
#SBATCH -N 1 # number of nodes
#SBATCH -n 11 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o S7.out # STDOUT
#SBATCH -e S7.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunOpponentsRoundsTwo(0.8);exit;'
