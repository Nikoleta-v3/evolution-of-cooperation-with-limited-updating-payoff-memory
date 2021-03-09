#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J S9 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o S9.out # STDOUT
#SBATCH -e S9.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(1.6);exit;'
