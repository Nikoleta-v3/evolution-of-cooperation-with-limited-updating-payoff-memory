function RunMutation();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 8;

% payoff_types = ["expected", "last_round"];
% mutations = [10 ^ -4, 10 ^ -3, 10 ^ -2, 10 ^ -1, 10 ^ 0];

data = ["expected", 10 ^ -4;
        "expected", 10 ^ -3;
        "expected", 10 ^ -2;
        "expected", 10 ^ -1;
        "expected", 10 ^ 0;
        "last_round", 10 ^ -4;
        "last_round", 10 ^ -3;
        "last_round", 10 ^ -2;
        "last_round", 10 ^ -1;
        "last_round", 10 ^ 0;]

u = [2, -1, 3, 0];

parfor (i = 1:10)

mutation = mutations(str2num(data(i, 2)));
payoff_type = payoff_types(data(i, 1));

filename = "../data/mutation_" + payoff_type + "_mutation_" + mutation;
evolMutation(starting_resident, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);
end
end