
#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J 2.0--1.0 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o 2.0--1.0.out # STDOUT
#SBATCH -e 2.0--1.0.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(2.0,-1.0);exit;'
