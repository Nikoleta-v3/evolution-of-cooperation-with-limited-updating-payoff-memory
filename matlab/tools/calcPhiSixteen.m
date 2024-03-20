function [Phi]=calcPhiSixteen(u, beta);
%% Calculates all possible pairwise imitation probabilities based on the last two payoffs
    Us = zeros(16, 16);

    for i=1:16
        for j=1:16
            Us(i, j) = (u(1 + fix((j - 1) / 4)) + u(1 + mod(j - 1, 4))) - (u(1 + fix((i - 1) / 4)) + u(1 + mod(i - 1, 4)));
        end
    end

    Us = Us / 2;
    Phi = zeros(16, 16);

    for i=1:16
        for j=1:16
            Phi(i, j) = 1 / (1 + exp(-beta * Us(i, j)));
        end
    end
end