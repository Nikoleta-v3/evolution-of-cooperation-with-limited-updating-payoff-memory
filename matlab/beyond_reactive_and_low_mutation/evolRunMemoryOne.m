function evolRunMemoryOne();

starting_resident = [0, 0, 0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 7;
payoff_type = "expected" % "last_round"

us = [1, -1, 2, 0;
      2, -1, 3, 0;
      3, -1, 4, 0;
      4, -1, 5, 0;
      5, -1, 6, 0;
      6, -1, 7, 0;
      7, -1, 8, 0;
      8, -1, 9, 0;
      9, -1, 10, 0];

parfor (i = 1:9)
    u = us(i, :);
    filename = "../data/memory_one_run_two" + payoff_type + "_b_" + u(3);
    evolSimulationMemoryOne(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end
end
