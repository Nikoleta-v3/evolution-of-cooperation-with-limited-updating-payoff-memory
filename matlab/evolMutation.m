function [xDat, payoff_type, Data]=evolMutation(starting_resident, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);

%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)),'; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; mu=',num2str(mutation), '; nIt=',num2str(numberIterations),'; payoff=',payoff_type];
 
%% Initialization
Res=starting_resident; sdim=3;

population=zeros(N, sdim);
for i=1:N
population(i, :)=Res;
end

xDat=zeros(numberIterations/100, 5);
xDat(1,:)=[i, Res, N];
j=2;
%% Running the evolutionary process
for t = progress(1:numberIterations)
    if rand(1)<mutation
        index = randi(N);
        population(index, :) = rand(1, sdim);
        
    else
        indices = randi(N, [1, 2]);
  
        if payoff_type == "expected"
            resident_payoff = payoffsExpected(indices(1), population, u, N, delta);
            mutant_payoff = payoffsExpected(indices(2), population, u, N, delta);
           
        end
        if payoff_type == "last_round"
            payoffs = payoffsLastRound(indices, population, u, N, delta);
            resident_payoff = payoffs(1);
            mutant_payoff = payoffs(2);
           
        end
        
        fermi = 1 / (1 + exp(-beta * (mutant_payoff - resident_payoff)));
        if rand(1)<fermi
            population(indices(1), :) = population(indices(2), :);
        end
    end
   [Mu,~,ic] = unique(population, 'rows', 'stable');
   h = accumarray(ic, 1);
   dimensions=size(h);
   
   xDat(j:j+dimensions-1, :) = [t.* ones(dimensions), Mu, h];
   
   j = j + dimensions;
   
dlmwrite(filename + ".csv", xDat, 'precision', 9);
writematrix(Data, filename + ".txt");
end
