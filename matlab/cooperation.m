function [coop]=cooperation(player, Mu, h, sz, delta);


coop = zeros(sz, 1);

for i=1:sz
    v=stationary(player, Mu(i, :), delta);
    coop(i) = v(1) + v(2);
end

coop = sum(coop .* h / sum(h));
end