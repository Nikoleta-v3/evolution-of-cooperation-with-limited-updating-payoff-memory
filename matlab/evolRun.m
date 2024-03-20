function evolRun(payoff_type);
% `payoff_type` is an input to the evolutionary simulation function. The payoff
% type can take six different values:
%
% 1. "expected" - Updating occurs based on expected payoffs (perfect memory).
% 2. "last_round" - Updating occurs based on the last round of one interaction
%    (limited memory).
% 3. "one_opponent" - Updating occurs based on the average payoff of one
%    interaction.
% 4. "two_rounds" - Updating occurs based on the last two rounds of one
%    interaction.
% 5. "two_opponents" - Updating occurs based on the last round of two
%    interactions.
% 6. "two_rounds_opponents" - Updating occurs based on the last two rounds of two
%    interactions.

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations = 10^7;

% `b` is the benefit of cooperation. For the results, we consider different values of `b`.
b = 10;

% `u` captures the payoff matrix of the game.
% We can change this to capture the snowdrift game.
u = [b - 1, -1, b, 0];

if payoff_type == "expected"
    filename = 'expected_payoff_benefit_' + string(b);
    evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);

elseif payoff_type == "last_round"
    filename = 'limited_payoff_benefit_' + string(b);
    evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);

elseif payoff_type == "one_opponent"
    filename = 'one_opponent_payoff_benefit_' + string(b);
    evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);

elseif payoff_type == "two_rounds"
    filename = 'two_rounds_payoff_benefit_' + string(b);
    evolSimulationUpdatingMemoryTwo(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);

elseif payoff_type == "two_opponents"
    filename = 'two_opponent_payoff_benefit_' + string(b);
    evolSimulationUpdatingMemoryTwo(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);

elseif payoff_type == "two_rounds_opponents"
    filename = 'two_rounds_two_opponents_payoff_benefit_' + string(b);
    evolSimulationUpdatingMemoryFour(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
end

% We can also use the MATLAB function `parfor` to run jobs in parallel. For example, consider:

% benefits = [3; 10];
% filenames = ["expected_low_benefit", "expected_high_benefit"];

% parfor i = 1:2
%     b = benefits(i);
%     filename = filenames(i);
%     evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
% end

end