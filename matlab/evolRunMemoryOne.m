function evolRunMemoryOne();

starting_resident = [0, 0, 0, 0, 0];
N = 100;
delta = 0.999;
betas = [10 ^ - 2, 10 ^ -1, 10 ^ 0, 10 ^ 1, 10 ^ 2];
numberIterations = 10 ^ 7;
payoff_type = "expected" % "last_round"

u = [2, -1, 3, 0];

parfor (i = 1:5)
    beta = betas(i);
    filename = "../data/memory_one_" + payoff_type + "_beta_" + beta;
    evolSimulationMemoryOne(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end
end