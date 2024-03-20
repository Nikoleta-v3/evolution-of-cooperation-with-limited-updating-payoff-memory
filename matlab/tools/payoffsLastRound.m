function [payoffs]=payoffsLastRound(players_indices, population, u, N, delta);
% The realised payoff 
payoffs = zeros(1, 2);
exclude = zeros(1, 3);

for i=1:2
    exclude(i)  = players_indices(i);
    opponent_id = randsample(setdiff(1:N, exclude), 1);

    player = population(players_indices(i), :);
    opponent = population(opponent_id, :);
    v=stationary(player, opponent, delta);
    
    if opponent_id == players_indices(2)
        payoffs(1) = randsample(u, 1, true, v);
        payoffs(2) = (payoffs(1) == u) * [u(1), u(3), u(2), u(4)]';
        break
    else
        payoffs(i) = randsample(u, 1, true, v);
        exclude(3) = opponent_id;
    end

end
end