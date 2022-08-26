function evolRunRoundsTwo();

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 6;
payoff_type = "two_rounds";
u = [2, -1, 3, 0];

filename = "../data/two_rounds_new.csv";

evolSimulationTwoRounds(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);

end