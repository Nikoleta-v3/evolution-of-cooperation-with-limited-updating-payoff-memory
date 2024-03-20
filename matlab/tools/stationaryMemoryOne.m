function v=stationaryMemoryOne(p1,p2,delta);
% Calculates the probabilities of being at CC, CD, DC, DD at the last round
% given that player 1 and 2 use memory-1 strategies

M = [p1(1)*p2(1), p1(1)*(1-p2(1)), (1-p1(1))*p2(1), (1-p1(1))*(1-p2(1));
     p1(2)*p2(3), p1(2)*(1-p2(3)), (1-p1(2))*p2(3), (1-p1(2))*(1-p2(3));
     p1(3)*p2(2), p1(3)*(1-p2(2)), (1-p1(3))*p2(2), (1-p1(3))*(1-p2(2));
     p1(4)*p2(4), p1(4)*(1-p2(4)), (1-p1(4))*p2(4), (1-p1(4))*(1-p2(4))];

    v0=[p1(5)*p2(5), p1(5)*(1-p2(5)), (1-p1(5))*p2(5), (1-p1(5))*(1-p2(5))];

v=(1-delta)*v0/(eye(4)-delta*M);
end