
#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J -0.8--1.0 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o -0.8--1.0.out # STDOUT
#SBATCH -e -0.8--1.0.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(-0.7999999999999998,-1.0);exit;'
