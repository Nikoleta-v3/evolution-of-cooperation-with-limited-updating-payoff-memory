function [xDat,AvCoop,AvPay,Rho,stochastic,Data]=evolSimulationOpponentsTwo(starting_resident, u, N, delta, beta, numberIterations, filename);

%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)), '; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; nIt=',num2str(numberIterations)];
AvCoop=0; AvPay=0; Res=starting_resident;

sdim=3;
xDat=zeros(numberIterations/100, 6);
xDat(1, :)=[Res, 0, u(4), 0];

%% Calculating all possible pairwise imitation probabilities based on one payoff
Rho=zeros(4,4);
for i1=1:4
    for i2=1:4
        Rho(i1,i2)=1 / (1 + exp(-beta * (u(i2) - u(i1))));
    end
end


%% Running the evolutionary process
j = 2;
for t = progress(1:numberIterations)
    Mut=rand(1,sdim);
    [rho,coopM,piM]=CalcRho(Mut, Res, Rho, N, u, delta, beta, stochastic); 
    if rand(1)<rho
        Res=Mut; xDat(j,:)=[Res,coopM,piM,t]; j=j+1;
    end
end

csvwrite(filename + ".csv", xDat);
csvwrite(filename + ".txt", Data);

AvCoop = mean(xDat(:, end-2));
AvPay = mean(xDat(:, end-1));
%time=toc
end

function [rho,coopMM,piMM]=CalcRho(Mut, Res, Rho, N, u, delta, beta, stochastic); 

%% Preparations: Calculating outcome probabilities and expected payoffs

vMM=stationary(Mut,Mut,delta);
vMR=stationary(Mut,Res,delta);
vRM=[vMR(1) vMR(3) vMR(2) vMR(4)];
vRR=stationary(Res,Res,delta);

coopMM=vMM(1)+vMM(2);
piMM=vMM*u';
piMR=vMR*u';
piRM=vRM*u';
piRR=vRR*u';

%% Calculating the fixation probability
laplus = zeros(1,N-1); laminus=laplus;

for k=1:N-1
    x=zeros(4,4);
    for i1=1:4
        for i2=1:4
            x(i1,i2)= 1/(N-1) * vRM(i1) * ((i1==1 & i2==1) | (i1==2 & i2==3) | (i1==3 &i2==2) | (i1==4 & i2==4))...
                + (1- 1 / (N - 1)) / (N - 2) / (N - 3) * ( ...
  ((k-1) * (k-2) * vRM(i1) * vMM(i2)) / (N - 3) / (N - 4) * ((k-2)*(k-3)*vRM(i1)*vMM(i2) + (k-2)*(N-k-1)*VRR(i1)*vMM(i2) + (N-k-1)*(k-2)*vRM(i1)*vMR(i2) + (N-k-1)*(N-k-2)*vRR(i1)*vMR(i2)) ...
+ ((k-1) * (N-k-1) * vRM(i1) * vMR(i2)) / (N - 3) / (N - 4) * ((k-1)*(k-3)*vRM(i1)*vMM(i2) + (k-1)*(N-k-1)*vRR(i1)*vMM(i2) + (N-k-2)*(k-2)*vRM(i1)*vMR(i2) + (N-k-2)*(N-k-2)*vRR(i1)*vMR(i2)) ...
+ ((N-k-1) * (k-1) * vRR(i1) * vMM(i2)) / (N - 3) / (N - 4) *  ((k-2)*(k-2)*vRM(i1)*vMM(i2) + (k-2)*(N-k-2)*vRR(i1)*vMM(i2) + (N-k-1)*(k-1)*vRM(i1)*vMR(i2) + (N-k-1)*(N-k-3)*vRR(i1)*vMR(i2)) ...
=+ (N-k-1) * (N-k-2) * vRR(i1) * vMR(i2) / (N - 3) / (N - 4) * ((k-1)*(k-2)*vRM(i1)*vMM(i2) + (k-1)*(N-k-2)*vRR(i1)*vMM(i2) + (N-k-2)*(k-1)*vRM(i1)*vMR(i2) + (N-k-2)*(N-k-3)*vRR(i1)*vMR(i2)));
        end
    end
    laplus(k)=sum(sum(x.*Rho));
    laminus(k)=sum(sum(x.*Rho'));
end

rho=1/(1+sum(cumprod(laminus./laplus))); 
end