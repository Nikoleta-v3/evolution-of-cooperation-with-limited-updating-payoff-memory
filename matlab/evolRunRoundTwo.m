function evolRunRoundTwo(S, T);

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations= 10 ^ 8;

u = [1, S, T, 0];
filename = "data/round_two/S_" + S + "_T_" + T;
evolSimulationRoundTwo(starting_resident, u, N, delta, beta, numberIterations, filename);