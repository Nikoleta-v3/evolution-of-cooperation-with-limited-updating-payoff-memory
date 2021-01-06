function [xDat,AvCoop,AvPay,Rho,stochastic,Data]=run(stochastic, u, filename);

starting_resident = [0, 0, 0];
N = 100;
delta = 0.999;
beta = 1;
numberIterations= 10 ^ 7;

[xDat,AvCoop,AvPay,Rho,stochastic,Data]=evolSimulation(starting_resident, u, N, delta, beta, numberIterations, stochastic, filename);
end