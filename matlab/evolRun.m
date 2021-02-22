function evolRun();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations= 10 ^ 7;
stochastic = 1;

n = 11;
Ss = linspace(-2, 2, n);
Ts = linspace(-1, 3, n);

payoffs = [[0.0, -1, 1.0, 0],
           [1.0, -1, 2.0, 0],
           [2.0, -1, 3.0, 0],
           [3.0, -1, 4.0, 0],
           [4.0, -1, 5.0, 0],
           [5.0, -1, 6.0, 0],
           [6.0, -1, 7.0, 0],
           [7.0, -1, 8.0, 0],
           [8.0, -1, 9.0, 0],
           [9.0, -1, 10.0, 0]];


parfor i = 1:10
    u = payoffs(i, :);
    c = 1;
    b = u(3);
    filename = "data/stochastic/c_" + c + "_b_" + b + "_stochastic_" + stochastic;
    evolSimulation(starting_resident, u, N, delta, beta, numberIterations, stochastic, filename);
end
end