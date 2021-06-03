function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 5 * 10 ^ 7;
payoff_type = "last_round";

bs = linspace(2, 10, 9);


parfor (i = 1:9)
    b = bs(i);
    u = [b - 1, -1, b, 0];
    filename = "../data/last_round_b_" + b;
    evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end
end