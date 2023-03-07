function [phi]=phiTwoRoundsOpponents(N, vRM, vMM, vMR, vRR, Rho, condition_round_one, condition_round_two, ps);
%% Calculates the fixation probability based on the last two rounds payoff with two opponents
laplus = zeros(1, N-1); laminus=laplus;
for k=1:N-1
    x=zeros(256, 256);
    for i1=1:256
        for i2=1:256

learner_role_model = 1 / (N - 1) * vRM(ps(i1, 1)) * condition_round_one(i1, i2) * ( ...
1 / (N - 2) / (N - 3) * ((k - 1) * (k - 2) * vRM(ps(i1, 2)) * vMM(ps(i2, 2)) + (k - 1) * (N - k - 1) * vRM(ps(i1, 2)) * vMR(ps(i2, 2)) + (N - k - 1) * (k - 1) * vRR(ps(i1, 2)) * vMM(ps(i2, 2)) + (N - k - 1) * (N - k - 2) * vRR(ps(i1, 2)) * vMR(ps(i2, 2))));

mutant_mutant = (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * ((k-1) * (k-2) * vRM(ps(i1, 1)) * vMM(ps(i2, 1))) * ((1 - 1 / (N - 2)) / (N - 3) / (N - 4) * ((k-2)*(k-3)*vRM(ps(i1, 2))*vMM(ps(i2, 2)) + (k-2)*(N-k-1)*vRR(ps(i1, 2))*vMM(ps(i2, 2)) + (N-k-1)*(k-2)*vRM(ps(i1, 2))*vMR(ps(i2, 2)) + (N-k-1)*(N-k-2)*vRR(ps(i1, 2))*vMR(ps(i2, 2))) + ...
1 / (N - 2) * vRM(ps(i1, 2)) * condition_round_two(i1, i2));

mutant_resident = (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * ((k-1) * (N-k-1) * vRM(ps(i1, 1)) * vMR(ps(i2, 1))) * ((1 - 1 / ( N - 2)) / (N - 3) / (N - 4) * ((k-1)*(k-3)*vRM(ps(i1, 2))*vMM(ps(i2, 2)) + (k-1)*(N-k-1)*vRR(ps(i1, 2))*vMM(ps(i2, 2)) + (N-k-2)*(k-2)*vRM(ps(i1, 2))*vMR(ps(i2, 2)) + (N-k-2)*(N-k-2)*vRR(ps(i1, 2))*vMR(ps(i2, 2))) + ...
1 / (N - 2) * vRM(ps(i1, 2)) * condition_round_two(i1, i2));

resident_mutant = (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * ((N-k-1) * (k-1) * vRR(ps(i1, 1)) * vMM(ps(i2, 1)))  *  ((1 - 1 / ( N - 2)) / (N - 3) / (N - 4) * ((k-2)*(k-2)*vRM(ps(i1, 2))*vMM(ps(i2, 2)) + (k-2)*(N-k-2)*vRR(ps(i1, 2))*vMM(ps(i2, 2)) + (N-k-1)*(k-1)*vRM(ps(i1, 2))*vMR(ps(i2, 2)) + (N-k-1)*(N-k-3)*vRR(ps(i1, 2))*vMR(ps(i2, 2))) + ...
1 / (N - 2) * vRM(ps(i1, 2)) * condition_round_two(i1, i2));

resident_resident = (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * (N-k-1) * (N-k-2) * vRR(ps(i1, 1)) * vMR(ps(i2, 1)) * ((1 - 1 / ( N - 2)) / (N - 3) / (N - 4) * ((k-1)*(k-2)*vRM(ps(i1, 2))*vMM(ps(i2, 2)) + (k-1)*(N-k-2)*vRR(ps(i1, 2))*vMM(ps(i2, 2)) + (N-k-2)*(k-1)*vRM(ps(i1, 2))*vMR(ps(i2, 2)) + (N-k-2)*(N-k-3)*vRR(ps(i1, 2))*vMR(ps(i2, 2))) + ...
1 / (N - 2) * vRM(ps(i1, 2)) * condition_round_two(i1, i2));

x(i1,i2) = learner_role_model + (mutant_mutant + mutant_resident + resident_mutant + resident_resident);

        end
    end
laplus(k) = sum(sum(x.*Rho));
laminus(k) = sum(sum(x.*Rho'));
end

phi = 1 / (1 + sum(cumprod(laminus./laplus)));
end