function [xDat,AvCoop,Rho,Data]=evolSimulationRoundTwo(starting_resident, u, N, delta, beta, numberIterations, filename);

%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)), '; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; nIt=',num2str(numberIterations)];
AvCoop=0; Res=starting_resident;

sdim = 3;
xDat = zeros(numberIterations/100, 5);
xDat(1, :)=[Res, 0, 0];

Us = zeros(16, 16);

for i=1:16
    for j=1:16
        Us(i, j) = (u(1 + fix((j - 1) / 4)) + u(1 + mod(j - 1, 4))) - (u(1 + fix((i - 1) / 4)) + u(1 + mod(i - 1, 4)));
    end
end

Us = Us / 2;

Rho = zeros(16, 16);

for i=1:16
    for j=1:16
        Rho(i, j) = 1 / (1 + exp(-beta * Us(i, j)));
    end
end

%% Running the evolutionary process
j = 2;
for t = progress(1:numberIterations)
    Mut = rand(1, sdim);
    [rho,coopM] = CalcRhoRoundTwo(Mut, Res, N, u, delta, beta, Rho);
    if rand(1)<rho
        Res=Mut; xDat(j,:)=[Res,coopM,t]; j=j+1;
    end
end

csvwrite(filename + ".csv", xDat);
csvwrite(filename + ".txt", Data);
end

function [rho,coopMM]=CalcRhoRoundTwo(Mut, Res, N, u, delta, beta, Rho);

%% Preparations: Calculating outcome probabilities and expected payoffs

vMM = stationaryRoundTwo(Mut, Mut, delta);
vMR = stationaryRoundTwo(Mut, Res, delta);
vRM = stationaryRoundTwo(Res, Mut, delta);
vRR = stationaryRoundTwo(Res, Res, delta);

coopMM = 2 * (vMM(1) + vMM(2) + vMM(5) + vMM(6)) + (vMM(3) + vMM(4) + vMM(7) + vMM(8) + vMM(9) + vMM(10) + vMM(13) + vMM(14));

laplus = zeros(1, N-1); laminus=laplus;
for k=1:N-1
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

rho = 1 / (1 + sum(cumprod(laminus./laplus)));
end
