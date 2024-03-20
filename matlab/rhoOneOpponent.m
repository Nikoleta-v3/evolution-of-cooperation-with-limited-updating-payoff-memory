function [rho]=rhoOneOpponent(N, piMM, piMR, piRR, piRM, beta);
%% Calculates the fixation probability based on the last round payoffs

rhos = [1 / (1 + exp(-beta * (piRM - piMR)));
        1 / (1 + exp(-beta * (piRM - piMM))); 
        1 / (1 + exp(-beta * (piRR - piMM))); 
        1 / (1 + exp(-beta * (piRR - piMR)));
        1 / (1 + exp(-beta * (piMR - piRM)));
        1 / (1 + exp(-beta * (piMM - piRM)));
        1 / (1 + exp(-beta * (piMM - piRR)));
        1 / (1 + exp(-beta * (piMR - piRR)));];

laplus=zeros(1, N-1); laminus=laplus;
for k=1:N-1
    laminus(k) = 1/(N-1)*rhos(1)...
                + (1-1/(N-1))/(N-2)/(N-3) * ((k-1)*(k-2)*rhos(2) + (k-1)*(N-k-1)*rhos(1) + (N-k-1)*(k-1)*rhos(3) + (N-k-1)*(N-k-2)*rhos(4));
   
    laplus(k) = 1/(N-1)*rhos(5)...
                + (1-1/(N-1))/(N-2)/(N-3) * ((k-1)*(k-2)*rhos(6) + (k-1)*(N-k-1)*rhos(5) + (N-k-1)*(k-1)*rhos(7) + (N-k-1)*(N-k-2)*rhos(8));
end

rho = 1 / (1 + sum(cumprod(laminus./laplus)));
end