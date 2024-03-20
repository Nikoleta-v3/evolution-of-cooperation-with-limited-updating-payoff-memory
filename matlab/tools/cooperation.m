function [coop]=cooperation(Mu, h, sz, delta);
%% Calculates average cooperation rate withing a population
coop = zeros(sz, 1);

for i=1:sz
    player_coop = zeros(sz, 1);
    for j=1:sz
        v=stationary(Mu(i, :), Mu(j, :), delta);
        player_coop(j) = v(1) + v(2);
    end
    coop(i) = mean(player_coop); 
end
coop = sum(coop .* h / sum(h));
end