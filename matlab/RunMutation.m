function RunMutation();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 5;

data = ["expected", 10 ^ -1;
        "last_round", 10 ^ -1];

u = [2, -1, 3, 0];

mutation = 10 ^ -1;
payoff_type = "last_round";

filename = "../data/mutation_" + payoff_type + "_mutation_" + mutation;
evolMutation(starting_resident, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);
% parpool();
% parfor (i = 1:2)
% mutation = str2num(data(i, 2));
% payoff_type = data(i, 1);
% 
% filename = "../data/mutation_" + payoff_type + "_mutation_" + mutation;
% evolMutation(starting_resident, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);
% end
end