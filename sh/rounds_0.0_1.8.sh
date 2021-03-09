
#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J 0.0-1.8 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o 0.0-1.8.out # STDOUT
#SBATCH -e 0.0-1.8.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(0.0,1.8000000000000003);exit;'
