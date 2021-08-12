function [population, avg_player, coop]=evolMutation(starting_resident, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);
tic

%% Initialization
Res=starting_resident; sdim=3; avg_player=0; coop=0;

population = Res .* ones(N, sdim, 'single');
% xDat=zeros(numberIterations, 5);
% xDat(1,:)=[0, Res, 0];
% j = 1;

%% Running the evolutionary process
for t = progress(1:numberIterations)
    if rand(1)<mutation
        idx = randi(N);
%         population = population(idx, :);
        population(idx, :) = rand;
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
  avg_player = avg_player + sum(Mu .* h / sum(h), 1);
  coop = coop + cooperation(Mu, h, sz, delta);
  
%   if mod(t, 100000) == 0 
%    xDat(j, :) = [t, avg_player, coop];
%    j = j + 1;
%   end    
end
% dlmwrite(filename + ".csv", xDat, 'precision', 9);

Data=["R", "S", "T", "P", "N", "beta", "mutation", "numberIterations", "coop", "y", "p", "q";
      u(1),...
      u(2),...
      u(3),...
      u(4),...
      N,...
      beta,...
      mutation,...
      numberIterations,...
      coop / numberIterations,...
      avg_player / numberIterations];

writematrix(Data, filename + ".csv");
toc
end



