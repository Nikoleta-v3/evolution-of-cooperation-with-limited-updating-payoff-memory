function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
numberIterations= 10 ^ 7;
stochastic = 1;

n = 7;
betas = [10 ^ -4, 10 ^ -3, 10 ^ -2, 10 ^ -1, 10 ^ 0, 10 ^ 1, 10 ^ 2];

parfor i = 1:n
    u = [2.0, -1, 3.0, 0];
    beta= betas(i);
    filename = "data/stochastic/beta_" + beta + "_stochastic_" + stochastic;
    evolSimulation(starting_resident, u, N, delta, beta, numberIterations, stochastic, filename);
end
end