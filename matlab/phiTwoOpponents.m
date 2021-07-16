function [phi]=phiTwoOpponents(N, vRM, vMM, vMR, vRR, Rho);
%% Calculates the fixation probability based on the last round payoff with two opponents
laplus=zeros(1,N-1); laminus=laplus;
for k=1:N-1
    x=zeros(16, 16);
    for i1=1:16
        for i2=1:16

            p_11 = 1 + fix((i1 - 1) / 4);
            p_12 = 1 + mod(i1 - 1, 4);
            q_21 = 1 + fix((i2 - 1) / 4);
            q_22 = 1 + mod(i2 - 1, 4);

            x(i1, i2) = q_22;

learner_role_model = 1 / (N - 1) * vRM(p_11) * ((p_11==1 & q_21==1) | (p_11==2 & q_21==3) | (p_11==3 &q_21==2) | (p_11==4 & q_21==4)) * ( ...
1 / (N - 2) / (N - 3) * ((k - 1) * (k - 2) * vRM(p_12) * vMM(q_22) + (k - 1) * (N - k - 1) * vRM(p_12) * vMR(q_22) + (N - k - 1) * (k - 1) * vRR(p_12) * vMM(q_22) + (N - k - 1) * (N - k - 2) * vRR(p_12) * vMR(q_22)));

mutant_mutant = (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * ((k-1) * (k-2) * vRM(p_11) * vMM(q_21)) * ((1 - 1 / (N - 2)) / (N - 3) / (N - 4) * ((k-2)*(k-3)*vRM(p_12)*vMM(q_22) + (k-2)*(N-k-1)*vRR(p_12)*vMM(q_22) + (N-k-1)*(k-2)*vRM(p_12)*vMR(q_22) + (N-k-1)*(N-k-2)*vRR(p_12)*vMR(q_22)) + ...
1 / (N - 2) * vRM(p_12) * ((p_12==1 & q_22==1) | (p_12==2 & q_22==3) | (p_12==3 &q_22==2) | (p_12==4 & q_22==4)));

mutant_resident = (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * ((k-1) * (N-k-1) * vRM(p_11) * vMR(q_21)) * ((1 - 1 / ( N - 2)) / (N - 3) / (N - 4) * ((k-1)*(k-3)*vRM(p_12)*vMM(q_22) + (k-1)*(N-k-1)*vRR(p_12)*vMM(q_22) + (N-k-2)*(k-2)*vRM(p_12)*vMR(q_22) + (N-k-2)*(N-k-2)*vRR(p_12)*vMR(q_22)) + ...
1 / (N - 2) * vRM(p_12) * ((p_12==1 & q_22==1) | (p_12==2 & q_22==3) | (p_12==3 &q_22==2) | (p_12==4 & q_22==4)));

resident_mutant = (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * ((N-k-1) * (k-1) * vRR(p_11) * vMM(q_21))  *  ((1 - 1 / ( N - 2)) / (N - 3) / (N - 4) * ((k-2)*(k-2)*vRM(p_12)*vMM(q_22) + (k-2)*(N-k-2)*vRR(p_12)*vMM(q_22) + (N-k-1)*(k-1)*vRM(p_12)*vMR(q_22) + (N-k-1)*(N-k-3)*vRR(p_12)*vMR(q_22)) + ...
1 / (N - 2) * vRM(p_12) * ((p_12==1 & q_22==1) | (p_12==2 & q_22==3) | (p_12==3 &q_22==2) | (p_12==4 & q_22==4)));

resident_resident = (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * (N-k-1) * (N-k-2) * vRR(p_11) * vMR(q_21) * ((1 - 1 / ( N - 2)) / (N - 3) / (N - 4) * ((k-1)*(k-2)*vRM(p_12)*vMM(q_22) + (k-1)*(N-k-2)*vRR(p_12)*vMM(q_22) + (N-k-2)*(k-1)*vRM(p_12)*vMR(q_22) + (N-k-2)*(N-k-3)*vRR(p_12)*vMR(q_22)) + ...
1 / (N - 2) * vRM(p_12) * ((p_12==1 & q_22==1) | (p_12==2 & q_22==3) | (p_12==3 &q_22==2) | (p_12==4 & q_22==4)));

x(i1,i2) = learner_role_model + (mutant_mutant + mutant_resident + resident_mutant + resident_resident);
        end
    end
    laplus(k)=sum(sum(x.*Rho));
    laminus(k)=sum(sum(x.*Rho'));
end

phi = 1 / (1 + sum(cumprod(laminus./laplus)));
end
