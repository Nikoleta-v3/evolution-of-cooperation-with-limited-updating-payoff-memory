function [payoffs]=payoffsLastRound(players_indices, population, u, N, delta);

payoffs = zeros(1, 2);

for i=1:2
    opponent_id = randi(N - i);
    sub_population = population(setdiff(1:N, players_indices(1:i)), :);

    player = population(players_indices(i), :);
    opponent = sub_population(opponent_id, :);

    v=stationary(player, opponent, delta);
    payoffs(i)  = v * u';
end
end