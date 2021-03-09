
#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J -1.2-3.0 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o -1.2-3.0.out # STDOUT
#SBATCH -e -1.2-3.0.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(-1.2,3.0);exit;'
