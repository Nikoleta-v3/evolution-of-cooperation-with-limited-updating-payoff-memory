#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J S2 # job name
#SBATCH -N 1 # number of nodes
#SBATCH -n 11 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o S2.out # STDOUT
#SBATCH -e S2.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunOpponentsRoundsTwo(-1.2);exit;'
