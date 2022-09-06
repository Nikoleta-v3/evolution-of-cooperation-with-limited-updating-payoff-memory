function [population, avg_player, coop]=evolMutation(population, u, N, delta, beta, mutation, numberIterations, payoff_type, filename);

sdim=3; avg_player=0; coop=0;
%% Running the evolutionary process
for t = progress(1:numberIterations)
    if rand(1) < mutation
        idx = randi(N);
        population(idx, :) = rand(1, sdim);
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
            if rand(1) < fermi
                population(indices(1), :) = population(indices(2), :);
            end
        end
    end
    
  [Mu,~,ic] = unique(population, 'rows', 'stable'); 
  h = accumarray(ic,1);
  sz = size(h, 1);
  avg_player = avg_player + sum(Mu .* h / sum(h), 1);
  coop = coop + cooperation(Mu, h, sz, delta);

end

Data=["R", "S", "T", "P", "N", "beta", "mutation", "numberIterations", "coop", "y", "p", "q";
      u(1),...
      u(2),...
      u(3),...
      u(4),...
      N,...
      beta,...
      mutation,...
      numberIterations,...
      coop,...
      avg_player];

writematrix(Data, filename + ".csv");
writematrix(population, filename + "population.csv");
toc
end



