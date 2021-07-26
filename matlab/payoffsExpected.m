function [payoff]=payoffsExpected(player_id, population, u, N, delta);

player = population(player_id, :);
payoff = 0;
sub_population = population(setdiff(1:N, player_id), :);

for i=1:(N-1) 
    v=stationary(player, sub_population(i, :), delta);
    payoff = payoff + v *u';
end

payoff = payoff / (N - 1);
end