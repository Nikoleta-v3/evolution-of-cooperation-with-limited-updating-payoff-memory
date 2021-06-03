function [phi]=phiTwoOpponents(N, vRM, vMM, vMR, vRR, Rho);
%% Calculates the fixation probability based on the last round payoff with two opponents
laplus=zeros(1,N-1); laminus=laplus;

for k=1:N-1
    x=zeros(4,4);
    for i1=1:4
        for i2=1:4
            x(i1,i2) = 1 / (N-1) * vRM(i1) * ((i1==1 & i2==1) | (i1==2 & i2==3) | (i1==3 &i2==2) | (i1==4 & i2==4))...
                + (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * ( ...
  ((k-1) * (k-2) * vRM(i1) * vMM(i2)) / (N - 3) / (N - 4) * ((k-2)*(k-3)*vRM(i1)*vMM(i2) + (k-2)*(N-k-1)*vRR(i1)*vMM(i2) + (N-k-1)*(k-2)*vRM(i1)*vMR(i2) + (N-k-1)*(N-k-2)*vRR(i1)*vMR(i2)) ...
+ ((k-1) * (N-k-1) * vRM(i1) * vMR(i2)) / (N - 3) / (N - 4) * ((k-1)*(k-3)*vRM(i1)*vMM(i2) + (k-1)*(N-k-1)*vRR(i1)*vMM(i2) + (N-k-2)*(k-2)*vRM(i1)*vMR(i2) + (N-k-2)*(N-k-2)*vRR(i1)*vMR(i2)) ...
+ ((N-k-1) * (k-1) * vRR(i1) * vMM(i2)) / (N - 3) / (N - 4) *  ((k-2)*(k-2)*vRM(i1)*vMM(i2) + (k-2)*(N-k-2)*vRR(i1)*vMM(i2) + (N-k-1)*(k-1)*vRM(i1)*vMR(i2) + (N-k-1)*(N-k-3)*vRR(i1)*vMR(i2)) ...
+ (N-k-1) * (N-k-2) * vRR(i1) * vMR(i2) / (N - 3) / (N - 4) * ((k-1)*(k-2)*vRM(i1)*vMM(i2) + (k-1)*(N-k-2)*vRR(i1)*vMM(i2) + (N-k-2)*(k-1)*vRM(i1)*vMR(i2) + (N-k-2)*(N-k-3)*vRR(i1)*vMR(i2)));
        end
    end
    laplus(k)=sum(sum(x.*Rho));
    laminus(k)=sum(sum(x.*Rho'));
end

phi = 1 / (1 + sum(cumprod(laminus./laplus)));
end
