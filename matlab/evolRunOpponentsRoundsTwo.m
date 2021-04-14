function evolRunOpponentsRoundsTwo(S);

distcomp.feature( 'LocalUseMpiexec', false)
num_workers = 11;
my_pool = parpool(num_workers);

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 10;
numberIterations= 10 ^ 7;

n=11;
Ts=linspace(-1, 3, n);

parfor i = 1:n
    T=Ts(i);
    u = [1, S, T, 0];
    filename = "data/rounds_opponents_two/S_" + S + "_T_" + T;
    evolSimulationOpponentsRoundsTwo(starting_resident, u, N, delta, beta, numberIterations, filename);
end
end