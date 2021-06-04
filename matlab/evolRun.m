function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 7;
payoff_types = ["two_rounds", "two_rounds_opponents"]

u = [2, -1, 3, 0];

parfor (i = 1:2)
    payoff_type = payoff_types(i);
    filename = "../data/sixteen_states_" + payoff_type;
    evolSimulationTwoRounds(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end
end