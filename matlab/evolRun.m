function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 3;
% payoff_types = ["two_opponents"]

u = [2, -1, 3, 0];

% parfor (i = 1:2)
payoff_type = "two_rounds_opponents";
filename = "../data/" + payoff_type;
evolSimulationTwoRoundsOpponents(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
% end
end