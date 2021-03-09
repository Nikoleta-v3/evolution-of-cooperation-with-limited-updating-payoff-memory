#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J S4 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o S4.out # STDOUT
#SBATCH -e S4.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(-0.4);exit;'
