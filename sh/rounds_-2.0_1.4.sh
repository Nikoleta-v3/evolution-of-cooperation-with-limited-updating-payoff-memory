
#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J -2.0-1.4 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o -2.0-1.4.out # STDOUT
#SBATCH -e -2.0-1.4.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(-2.0,1.4000000000000004);exit;'
