function evolRun();

num_workers = 1;
my_pool = parpool(num_workers);

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations= 10 ^ 8;
stochastic = 0;

u = [0, -1, 1, 0];

filename = "data/expected/donation_b_1";
evolSimulation(starting_resident, u, N, delta, beta, numberIterations, stochastic, filename);

% n = 11;
% Ss = linspace(-2, 2, n);
% Ts = linspace(-1, 3, n);

% payoffs = zeros(n * n, 2);

% for i=1:n
%     for j=1:n
%         payoffs(j + (i - 1) + (i -1) * 10, 1) = Ss(i);
%         payoffs(j + (i - 1) + (i -1) * 10, 2) = Ts(j);
%     end
% end

% lenght = n * n;
% parfor i = 1:lenght
%     S = payoffs(i, 1);
%     T = payoffs(i, 2);
%     u = [1, S, T, 0];
%     filename = "data/expected/S_" + S + "_T_" + T + "_beta_" + beta;
%     evolSimulation(starting_resident, u, N, delta, beta, numberIterations, stochastic, filename);
% end
% end