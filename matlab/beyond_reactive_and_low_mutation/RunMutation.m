function RunMutation();

starting_resident = [0, 0, 0];
N = 100;
sdim = 3;
delta = 0.999;
beta = 1;
numberIterations = 10 ^ 5;

data = ["expected", 10 ^ -4;
        "expected", 10 ^ -3;
        "expected", 10 ^ -2;
        "expected", 10 ^ -1;
        "expected", 10 ^ 0;
        "last_round", 10 ^ -4;
        "last_round", 10 ^ -3;
        "last_round", 10 ^ -2;
        "last_round", 10 ^ -1;
        "last_round", 10 ^ -0];

u = [2, -1, 3, 0];
n_run = 2;
previous = n_run - 1;

parfor (i = 1:1)
        mutation = str2num(data(i, 2));
        payoff_type = data(i, 1);

        filename = "../data/test/mutation_" + payoff_type + "_mutation_" + mutation + "_run_" + n_run;
        population_fln = "../data/test/mutation_" + payoff_type + "_mutation_" + mutation + "_run_" + previous;
        if n_run == 1;
            %% Initialization
            Res=starting_resident; 
            population = Res .* ones(N, sdim, 'single');

        else
            population = readmatrix(population_fln + "_population.csv");

        end
        disp(population)
%         evolMutation(population, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);
end
end