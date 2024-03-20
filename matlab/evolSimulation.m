function [xDat, payoff_type, Data]=evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename, seed);
rng(seed)
%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)), '; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; nIt=',num2str(numberIterations), '; payoff=',payoff_type];
AvCoop=0; AvPay=0; Res=starting_resident;

%% Initialization
sdim=3;
xDat=zeros(numberIterations/100,6);
xDat(1,:)=[Res, 0, u(4), 0];
Phi=calcPhi(u, beta);

%% Running the evolutionary process
j = 2;
for t = progress(1:numberIterations)
    Mut=rand(1, sdim);
    [rho, coopM, piM]=calcRho(Mut, Res, Phi, N, u, delta, beta, payoff_type);
    if rand(1)<rho
        Res=Mut; xDat(j,:)=[Res, coopM, piM, t]; j=j+1;
    end
end

dlmwrite(filename + ".csv", xDat, 'precision', 9);
writematrix(Data, filename + ".txt");
end

function [Phi]=calcPhi(u, beta);
%% Calculates all possible pairwise imitation probabilities based on one payoff
    Phi=zeros(4,4);
    for i1=1:4
        for i2=1:4
            Phi(i1,i2) = 1 / (1 + exp(-beta * (u(i2) - u(i1))));
        end
    end
end

function [rho, coopMM, piMM]=calcRho(Mut, Res, Phi, N, u, delta, beta, payoff_type);
%% Calculating the fixation probability

vMM = stationary(Mut, Mut, delta);
vMR = stationary(Mut, Res, delta);
vRM = [vMR(1) vMR(3) vMR(2) vMR(4)];
vRR = stationary(Res, Res, delta);

piMM = vMM*u';
coopMM = vMM(1)+vMM(2);

if payoff_type=="last_round"

    phi = rhoLastRound(N, vRM, vMM, vMR, vRR, Phi);

elseif payoff_type=="expected"

    piMR=vMR*u';
    piRM=vRM*u';
    piRR=vRR*u';
    phi = rhoExpected(N, piMM, piMR, piRR, piRM, beta);
    
elseif payoff_type=="one_opponent"
    piMR=vMR*u';
    piRM=vRM*u';
    piRR=vRR*u';
    phi = rhoOneOpponent(N, piMM, piMR, piRR, piRM, beta);

else
    disp('Please check payoff type.')
end
end
