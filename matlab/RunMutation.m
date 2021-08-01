function RunMutation();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
mutation = 10 ^ -4 % [10 ^ -4, 10 ^ -3, 10 ^ -2, 10 ^ -1, 10 ^ 0];
numberIterations = 10 ^ 8;
payoff_types = ["expected", "last_round"];

u = [2, -1, 3, 0];

parfor (i = 1:2)
payoff_type = payoff_types(i);
filename = "../data/mutation_" + payoff_type + "_mutation_" + mutation;
evolMutation(starting_resident, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);
end
end