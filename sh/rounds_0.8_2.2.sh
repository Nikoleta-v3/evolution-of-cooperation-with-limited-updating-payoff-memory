
#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J 0.8-2.2 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o 0.8-2.2.out # STDOUT
#SBATCH -e 0.8-2.2.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(0.8000000000000003,2.2);exit;'
