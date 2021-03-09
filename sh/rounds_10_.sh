#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J S10 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o S10.out # STDOUT
#SBATCH -e S10.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(2.0);exit;'
