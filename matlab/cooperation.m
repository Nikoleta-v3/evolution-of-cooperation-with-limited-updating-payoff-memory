function [coop]=cooperation(Mu, h, sz, delta);

coop = zeros(sz, 1);

for i=1:sz
    player_coop = zeros(sz, 1);
    for j=1:sz
        v=stationary(Mu(i, :), Mu(j, :), delta);
        player_coop(i) = v(1) + v(2);
    end
    coop(i) = sum(player_coop .* h / sum(h)); 
end
coop = sum(coop .* h / sum(h)); 
end