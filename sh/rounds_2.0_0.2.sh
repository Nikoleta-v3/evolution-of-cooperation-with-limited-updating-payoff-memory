
#!/bin/sh
#SBATCH -p medium  # partition (queue)
#SBATCH -J 2.0-0.2 # job name
#SBATCH -n 1 # number of cores
#SBATCH -t 2-00:00  # time (D-HH:MM)
#SBATCH -o 2.0-0.2.out # STDOUT
#SBATCH -e 2.0-0.2.err # STDERR

module load matlab
cd matlab

matlab -nodisplay -r 'evolRunRoundTwo(2.0,0.20000000000000018);exit;'
