function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 7;

u = [2, -1, 3, 0];

payoff_types = ["expected", "last_round", "two_opponents"];

parfor (i = 1:3)
    payoff_type = payoff_types(i)
    filename = "../data/" + payoff_type;
    evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end
end