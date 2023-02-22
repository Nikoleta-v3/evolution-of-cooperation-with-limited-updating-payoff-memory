function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 7;
payoff_type = "expected";
payoffs = readmatrix("two_by_two_games_values.csv");

parfor (i = 1:11)
    u = payoffs(i, :);
    filename = "../data/two_by_two_games_values_S" + u(2) + "_T_" + u(2);
    evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end
end

