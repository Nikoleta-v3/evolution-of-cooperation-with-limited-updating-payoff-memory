function [xDat, AvCoop, AvPay,payoff_type, Data]=evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);

rng('default')
%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)), '; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; nIt=',num2str(numberIterations), '; payoff=',payoff_type];
AvCoop=0; AvPay=0; Res=starting_resident;

%% Initialization
sdim=3;
xDat=zeros(numberIterations/100,6);
xDat(1,:)=[Res, 0, u(4), 0];
Rho=calcRho(u, beta);

%% Running the evolutionary process
j = 2;
for t = progress(1:numberIterations)
    Mut=rand(1, sdim);
    [phi, coopM, piM]=calcPhi(Mut, Res, Rho, N, u, delta, beta, payoff_type);
    if rand(1)<phi
        Res=Mut; xDat(j,:)=[Res, coopM, piM, t]; j=j+1;
    end
end

dlmwrite(filename + ".csv", xDat, 'precision', 9);
writematrix(Data, filename + ".txt");

AvCoop = mean(xDat(:,end-2));
AvPay = mean(xDat(:,end-1));
%time=toc
end

function [Rho]=calcRho(u, beta);
%% Calculates all possible pairwise imitation probabilities based on one payoff
    Rho=zeros(4,4);
    for i1=1:4
        for i2=1:4
            Rho(i1,i2) = 1 / (1 + exp(-beta * (u(i2) - u(i1))));
        end
    end
end

function [phi, coopMM, piMM]=calcPhi(Mut, Res, Rho, N, u, delta, beta, payoff_type);
%% Calculating the fixation probability

vMM=stationary(Mut, Mut, delta);
vMR=stationary(Mut, Res, delta);
vRM=[vMR(1) vMR(3) vMR(2) vMR(4)];
vRR=stationary(Res, Res, delta);

piMM=vMM*u';
coopMM=vMM(1)+vMM(2);

if payoff_type=="last_round"

    phi = phiLastRound(N, vRM, vMM, vMR, vRR, Rho);

elseif payoff_type=="expected"

    piMR=vMR*u';
    piRM=vRM*u';
    piRR=vRR*u';
    phi = phiExpected(N, piMM, piMR, piRR, piRM, beta);

else
    disp('Please check payoff type.')
end
end
