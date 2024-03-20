function [payoffs]=payoffsExpected(player_indices, population, u, N, delta);
% The expected payoff for each member of the population given the population
payoffs = zeros(N - 1, 2);

for i=1:N 
    for j=1:2
        if i ~= player_indices(j)
            v=stationaryReactive(population(player_indices(j), :), population(i, :), delta);
            payoffs(i, j) = v * u';
        end
    end
end

payoffs = sum(payoffs / (N - 1));
end