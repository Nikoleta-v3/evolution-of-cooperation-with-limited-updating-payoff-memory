
#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J -0.4-1.4 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o -0.4-1.4.out # STDOUT
#SBATCH -e -0.4-1.4.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(-0.3999999999999999,1.4000000000000004);exit;'
