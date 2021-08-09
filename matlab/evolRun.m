function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 6;
payoff_type = "two_rounds_opponents";
u = [9, -1, 10, 0];

seeds = [2, 3, 4, 5, 6, 7, 8, 9, 10];

parfor (i = 1:9)
    rng(seeds(i));
    filename = "../data/" + payoff_type + "_seed_" + seed;
    evolSimulationTwoRoundsOpponents(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end
end