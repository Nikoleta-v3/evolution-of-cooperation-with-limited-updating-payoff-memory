function v=stationaryMemoryOne(p1,p2,delta);
% Calculates the invariant distribution v
% for the game between two memory-1 players with strategies p1, p2.
% p1=(pCC, pCD, pDC, pDD, p0);

M = [p1(1)*p2(1), p1(1)*(1-p2(1)), (1-p1(1))*p2(1), (1-p1(1))*(1-p2(1));
     p1(2)*p2(3), p1(2)*(1-p2(3)), (1-p1(2))*p2(3), (1-p1(2))*(1-p2(3));
     p1(3)*p2(2), p1(3)*(1-p2(2)), (1-p1(3))*p2(2), (1-p1(3))*(1-p2(2));
     p1(4)*p2(4), p1(4)*(1-p2(4)), (1-p1(4))*p2(4), (1-p1(4))*(1-p2(4))];

    v0=[p1(5)*p2(5), p1(5)*(1-p2(5)), (1-p1(5))*p2(5), (1-p1(5))*(1-p2(5))];

v=(1-delta)*v0/(eye(4)-delta*M);
end