function [phi]=expected(N, piMM, piMR, piRR, piRM, beta);
%% Calculates the fixation probability based on the expected payoffs

laplus=zeros(1, N-1); laminus=laplus;
for k=1:N-1
    piM = (k-1) / (N-1) * piMM + (N-k) / (N-1) * piMR;
    piR = k / (N-1) * piRM + (N-k-1) / (N-1) * piRR;

    laplus(k) = 1 / (1 + exp(-beta * (piM - piR)));
    laminus(k) = 1 /(1 + exp(-beta * (piR - piM)));
end

phi = 1 / (1 + sum(cumprod(laminus./laplus)));
end
