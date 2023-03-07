function [laplus, laminus]=phiTwoRounds(N, vRM, vMM, vMR, vRR, Rho);
%% Calculates the fixation probability based on the last two rounds payoff

laplus = zeros(1, 1); laminus=laplus;
k=1;
x=zeros(16,16);
for i1=1:16
    for i2=1:16
x(i1,i2) = 1 / (N-1) * vRM(i1) * ((i1==1 & i2==1)  |(i1==2 & i2==3)  |(i1==3 &i2==2)   |(i1==4 & i2==4) |(i1==5 & i2==9) |(i1==6 & i2==11)|...
                              (i1==7 & i2==10) |(i1==8 & i2==12) |(i1==9 & i2==5)  |(i1==10 & i2==7)|(i1==11 & i2==6)|(i1==12 & i2==8)|...
                              (i1==13 & i2==13)|(i1==14 & i2==15)|(i1==15 & i2==14)|(i1==16 & i2==16))...
     + (1 - 1 / (N - 1)) / (N - 2) / (N - 3) * ((k - 1) * (k - 2) * vRM(i1) * vMM(i2) ...
     + (k - 1) * (N - k - 1) * vRM(i1) * vMR(i2) + (N - k - 1) * (k - 1) * vRR(i1) * vMM(i2) ...
     + (N - k - 1) * (N - k - 2) * vRR(i1) * vMR(i2));
    end
end
laplus(k) = sum(sum(x.*Rho));
laminus(k) = sum(sum(x.*Rho'));
end