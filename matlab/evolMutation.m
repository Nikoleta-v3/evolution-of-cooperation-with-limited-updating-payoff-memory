function [xDat, population, Data]=evolMutation(starting_resident, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);
tic
%% Preparations for the output
Data=['R=',num2str(u(1)),'; S=',num2str(u(2)),'; T=',num2str(u(3)),'; P=',num2str(u(4)),'; N=',num2str(N),'; beta=',num2str(beta), '; mu=',num2str(mutation), '; nIt=',num2str(numberIterations),'; payoff=',payoff_type];
writematrix(Data, filename + ".txt");

%% Initialization
Res=starting_resident; sdim=3;

population = Res .* ones(N, sdim);
xDat=zeros(numberIterations, 5);
xDat(1,:)=[0, Res, 0];

j = 2;
%% Running the evolutionary process
for t = progress(1:numberIterations)
    if rand(1)<mutation
        index = randi(N);
        population(index, :) = rand(1, sdim);
        
    else
        indices = randi(N, [1, 2]);
        
        if population(indices(1),:) ~= population(indices(2),:)
            if payoff_type == "expected"
                payoffs = payoffsExpected(indices, population, u, N, delta);
                resident_payoff = payoffs(1);
                mutant_payoff = payoffs(2);          
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
    end

   [Mu,~,ic] = unique(population, 'rows', 'stable'); 
   h = accumarray(ic,1);
   sz = size(h, 1);
   avg_player = sum(Mu .* h / sum(h), 1);
   coop=cooperation(Mu, h, sz, delta);
   
   xDat(j, :) = [t, avg_player, coop];
   
%    if coop > 0
%        disp(coop)
%    end

   j = j + 1;
end
dlmwrite(filename + ".csv", xDat, 'precision', 9);
toc
end

