import itertools

games = ["donation", "snowdrift", "stag", "harmony"]
modes = ["expected", "stochastic"]


def write_invasion_sh(games=games, modes=modes):
    number_of_cores = 4
    experiment = "invasion"

    combinations = itertools.product(games, modes)
    for game, mode in combinations:
        name = experiment + "_" + game + "_" + mode[:5] + ".sh"

        skeleton = f"""#!/bin/bash
#SBATCH -p amd  # partition (queue)
#SBATCH -J {experiment[:3] + "-" + game[:3]} # job name
#SBATCH -N 1 # number of nodes, use 1-1 if you need exactly one node
#SBATCH -n {number_of_cores} # number of cores
#SBATCH -t 1-00:00  # time (D-HH:MM)
#SBATCH -o slurm.%j.out # STDOUT
#SBATCH -e slurm.%j.err # STDERR

module load python/3.6.6
source ../venvs/payoffs/bin/activate

python src/{experiment}.py {mode} {game} None"""

        with open("sh/%s" % name, "w") as textfile:
            textfile.write(skeleton)


def write_simulation_sh(games=games, modes=modes):
    number_of_cores = 1
    experiment = "simulation"

    combinations = itertools.product(games, modes)
    for game, mode in combinations:
        name = experiment + "_" + game + "_" + mode[:5] + ".sh"

        skeleton = f"""#!/bin/bash
#SBATCH -p amd  # partition (queue)
#SBATCH -J {experiment[:3] + "-" + game[:3]} # job name
#SBATCH -N 1 # number of nodes, use 1-1 if you need exactly one node
#SBATCH -n {number_of_cores} # number of cores
#SBATCH -t 1-00:00  # time (D-HH:MM)
#SBATCH -o slurm.%j.out # STDOUT
#SBATCH -e slurm.%j.err # STDERR

module load python/3.6.6
source ../venvs/payoffs/bin/activate

python src/{experiment}.py {mode} {game}"""

        with open("sh/%s" % name, "w") as textfile:
            textfile.write(skeleton)


def write_multi_simulations_sh(games=games):
    number_of_cores = 10
    experiment = "multi_interactions"

    for game in games:
        for resident, resident_name in zip(["0, 0, 0", "1/3, 1/3, 1/3"], ["ALLD", "GTFT"]):
            name = experiment + "_" + game + resident_name + ".sh"

            skeleton = f"""#!/bin/bash
#SBATCH -p amd  # partition (queue)
#SBATCH -J {experiment[:3] + "-" + game[:3]} # job name
#SBATCH -N 1 # number of nodes, use 1-1 if you need exactly one node
#SBATCH -n {number_of_cores} # number of cores
#SBATCH -t 1-00:00  # time (D-HH:MM)
#SBATCH -o slurm.%j.out # STDOUT
#SBATCH -e slurm.%j.err # STDERR

module load python/3.6.6
source ../venvs/payoffs/bin/activate

python src/{experiment}.py {resident} {resident_name}"""

            with open("sh/%s" % name, "w") as textfile:
                textfile.write(skeleton)


# write_invasion_sh()
# write_simulation_sh()
write_multi_simulations_sh()
