function [xDat, AvCoop, AvPay,payoff_type, Data]=evolSimulation(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);

%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)), '; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; nIt=',num2str(numberIterations), '; payoff=',payoff_type];
AvCoop=0; AvPay=0; Res=starting_resident;

%% Initialization
sdim=3;
xDat=zeros(numberIterations/100,6);
xDat(1,:)=[Res, 0, u(4), 0];
Rho=calcRhoSixteen(u, beta);

%% Running the evolutionary process
j = 2;
for t = progress(1:numberIterations)
    Mut=rand(1, sdim);
    [phi, coopM, piM]=calcPhi(Mut, Res, Rho, N, u, delta, beta, payoff_type);
    if rand(1)<phi
        Res=Mut; xDat(j,:)=[Res, coopM, piM, t]; j=j+1;
    end
end

csvwrite(filename + ".csv", xDat);
writematrix(Data, filename + ".txt");

AvCoop = mean(xDat(:,end-2));
AvPay = mean(xDat(:,end-1));
%time=toc
end

function [Rho]=calcRhoSixteen(u, beta);
%% Calculates all possible pairwise imitation probabilities based on the last two payoffs
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
end

function [phi, coopMM, piMM]=calcPhi(Mut, Res, Rho, N, u, delta, beta, payoff_type);
%% Calculating the fixation probability

vMM = stationaryRoundTwo(Mut, Mut, delta);
vMR = stationaryRoundTwo(Mut, Res, delta);
vRM = stationaryRoundTwo(Res, Mut, delta);
vRR = stationaryRoundTwo(Res, Res, delta);

piMM = vMM*log(kron(exp(u),exp(u)))';
coopMM = (2 * (vMM(1) + vMM(2) + vMM(5) + vMM(6)) + (vMM(3) + vMM(4) + vMM(7) + vMM(8) + vMM(9) + vMM(10) + vMM(13) + vMM(14))) / 2;

if payoff_type=="two_rounds"

    phi = phiTwoRounds(N, vRM, vMM, vMR, vRR, Rho);

elseif  payoff_type=="two_rounds_opponents"

    phi = phiTwoRoundsOpponents(N, vRM, vMM, vMR, vRR, Rho);

else
    disp('Please check payoff type.')
end
end
