function [xDat,AvCoop,AvPay,Rho,stochastic,Data]=evolSimulation(starting_resident, u, N, delta, beta, numberIterations, stochastic, filename);

%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)), '; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; nIt=',num2str(numberIterations), '; stochastic=',num2str(stochastic)]; 
AvCoop=0; AvPay=0; Res=starting_resident;

sdim=3; 
xDat=zeros(numberIterations + 1, 6); 
xDat(1,:)=[Res, 0, u(4), 0]; 

%% Calculating all possible pairwise imitation probabilities based on one payoff
Rho=zeros(4,4); 
for i1=1:4
    for i2=1:4
        Rho(i1,i2) = 1 / (1 + exp(-beta * (u(i2) - u(i1)))); 
    end
end


%% Running the evolutionary process
for t = progress(1:numberIterations)
    Mut=rand(1,sdim); 
    [rho,coopM,piM]=CalcRho(Mut, Res, Rho, N, u, delta, beta, stochastic); 
    if rand(1)<rho
        Res=Mut; 
    end
    xDat(t + 1,:)=[Res,coopM,piM,t];
end

csvwrite(filename + ".csv", xDat);
writematrix(Data, filename + ".txt");

AvCoop = mean(xDat(:,end-2));
AvPay = mean(xDat(:,end-1));
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
laplus=zeros(1,N-1); laminus=laplus; 
if stochastic==1
    for k=1:N-1
        x=zeros(4,4); 
        for i1=1:4
            for i2=1:4
                x(i1,i2)=1/(N-1)*vRM(i1)*((i1==1 & i2==1) | (i1==2 & i2==3) | (i1==3 &i2==2) | (i1==4 & i2==4))...
                    + (1-1/(N-1))/(N-2)/(N-3) * ((k-1)*(k-2)*vRM(i1)*vMM(i2) + (k-1)*(N-k-1)*vRM(i1)*vMR(i2) + (N-k-1)*(k-1)*vRR(i1)*vMM(i2) + (N-k-1)*(N-k-2)*vRR(i1)*vMR(i2)); 
            end
        end
        laplus(k)=sum(sum(x.*Rho)); 
        laminus(k)=sum(sum(x.*Rho')); 
    end
else
    for k=1:N-1
        piM=(k-1)/(N-1)*piMM+(N-k)/(N-1)*piMR;
        piR=k/(N-1)*piRM+(N-k-1)/(N-1)*piRR;
        laplus(k)=1/(1+exp(-beta*(piM-piR))); 
        laminus(k)=1/(1+exp(-beta*(piR-piM)));
    end
end
    
rho=1/(1+sum(cumprod(laminus./laplus))); 
end