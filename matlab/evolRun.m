function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 7;
payoff_types = ["two_rounds", "two_opponents"];


u = [9, -1, 10, 0];

parfor (i = 1:2)
% numberIterations = numbersIterations(i);
payoff_type = payoff_types(i)
% seed = 1;
% rng(seed);
filename = "../data/" + payoff_type + "_b_10";
evolSimulationTwoRounds(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end
end