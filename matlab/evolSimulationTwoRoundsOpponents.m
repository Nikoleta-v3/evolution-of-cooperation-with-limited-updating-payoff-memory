function [xDat, AvCoop, AvPay,payoff_type, Data]=evolSimulationTwoRoundsOpponents(starting_resident, u, N, delta, beta, numberIterations, payoff_type, filename);
%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)), '; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; nIt=',num2str(numberIterations), '; payoff=',payoff_type];
AvCoop=0; AvPay=0; Res=starting_resident;

%% Initialization
sdim=3;
xDat=zeros(round(numberIterations/(100 * 0.6)), 6);
xDat(1,:)=[Res, 0, u(4), 0];
Rho=calcRhoTwoFiftySix(u, beta);

ps = zeros(256, 2);
for i1=1:256
    ps(i1, 1) = 1 + fix((i1 - 1) / 16);
    ps(i1, 2) = 1 + mod(i1 - 1, 16);
end

condition_round_one = zeros(256, 256);
condition_round_two = zeros(256, 256);

for i1=1:256
    for i2=1:256
        condition_round_one(i1, i2) = ((ps(i1, 1)==1 & ps(i2, 1)==1) |(ps(i1, 1)==2 & ps(i2, 1)==3) |(ps(i1, 1)==3 &ps(i2, 1)==2) |(ps(i1, 1)==4 & ps(i2, 1)==4) |(ps(i1, 1)==5 & ps(i2, 1)==9) | (ps(i1, 1)==6 & ps(i2, 1)==11)|...
        (ps(i1, 1)==7 & ps(i2, 1)==10) |(ps(i1, 1)==8 & ps(i2, 1)==12) |(ps(i1, 1)==9 & ps(i2, 1)==5)  |(ps(i1, 1)==10 & ps(i2, 1)==7)|(ps(i1, 1)==11 & ps(i2, 1)==6)|(ps(i1, 1)==12 & ps(i2, 1)==8)|...
        (ps(i1, 1)==13 & ps(i2, 1)==13)|(ps(i1, 1)==14 & ps(i2, 1)==15)|(ps(i1, 1)==15 & ps(i2, 1)==14)|(ps(i1, 1)==16 & ps(i2, 1)==16));

        condition_round_two(i1, i2) = ((ps(i1, 2)==1 & ps(i2, 2)==1) |(ps(i1, 2)==2 & ps(i2, 2)==3) |(ps(i1, 2)==3 &ps(i2, 2)==2) |(ps(i1, 2)==4 & ps(i2, 2)==4) |(ps(i1, 2)==5 & ps(i2, 2)==9) |(ps(i1, 2)==6 & ps(i2, 2)==11)|...
        (ps(i1, 2)==7 & ps(i2, 2)==10) |(ps(i1, 2)==8 & ps(i2, 2)==12) |(ps(i1, 2)==9 & ps(i2, 2)==5)  |(ps(i1, 2)==10 & ps(i2, 2)==7)|(ps(i1, 2)==11 & ps(i2, 2)==6)|(ps(i1, 2)==12 & ps(i2, 2)==8)|...
        (ps(i1, 2)==13 & ps(i2, 2)==13)|(ps(i1, 2)==14 & ps(i2, 2)==15)|(ps(i1, 2)==15 & ps(i2, 2)==14)|(ps(i1, 2)==16 & ps(i2, 2)==16));
    end
end

%% Running the evolutionary process
j = 2;
for t = progress(1:numberIterations)
    Mut=rand(1, sdim);
    [phi, coopM, piM]=calcPhi(Mut, Res, Rho, N, u, delta,  payoff_type, condition_round_one, condition_round_two, ps);
    if rand(1)<phi
        Res=Mut; xDat(j,:)=[Res, coopM, piM, t]; j=j+1;
    end
end

csvwrite(filename + ".csv", xDat);
writematrix(Data, filename + ".txt");

AvCoop = mean(xDat(:,end-2));
AvPay = mean(xDat(:,end-1));
end

function [Rho]=calcRhoTwoFiftySix(u, beta);
    %% Calculates all possible pairwise imitation probabilities based on the last two payoffs
        new_u = log(kron(exp(u),exp(u)));
        Rho = zeros(256, 256);
    
        for i=1:256
            for j=1:256
                player = new_u(1 + fix((i - 1) / 16)) + new_u(1 + mod(i - 1, 16));
                opponent = new_u(1 + fix((j - 1) / 16)) + new_u(1 + mod(j - 1, 16));
                Rho(i, j) =  1 / (1 + exp(-beta *(opponent - player) / 2));
            end
        end
end

function [phi, coopMM, piMM]=calcPhi(Mut, Res, Rho, N, u, delta, payoff_type, condition_round_one, condition_round_two, ps);
%% Calculating the fixation probability

vMM = stationaryRoundTwo(Mut, Mut, delta);
vMR = stationaryRoundTwo(Mut, Res, delta);
vRM = stationaryRoundTwo(Res, Mut, delta);
vRR = stationaryRoundTwo(Res, Res, delta);

piMM = vMM*log(kron(exp(u),exp(u)))';
coopMM = (2 * (vMM(1) + vMM(2) + vMM(5) + vMM(6)) + (vMM(3) + vMM(4) + vMM(7) + vMM(8) + vMM(9) + vMM(10) + vMM(13) + vMM(14))) / 2;

if payoff_type=="two_rounds_opponents"

    phi = phiTwoRoundsOpponents(N, vRM, vMM, vMR, vRR, Rho, condition_round_one, condition_round_two, ps);

else
    disp('Please check payoff type.')
end
end
