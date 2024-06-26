function v=stationaryReactive(p1,p2,delta);
% Calculates the probabilities of being at CC, CD, DC, DD at the last round.
% This is done using the invariant distrubtion of the transition matrix.

M=[p1(2)*p2(2), p1(2)*(1-p2(2)), (1-p1(2))*p2(2), (1-p1(2))*(1-p2(2));
    p1(3)*p2(2), p1(3)*(1-p2(2)), (1-p1(3))*p2(2), (1-p1(3))*(1-p2(2));
    p1(2)*p2(3), p1(2)*(1-p2(3)), (1-p1(2))*p2(3), (1-p1(2))*(1-p2(3));
    p1(3)*p2(3), p1(3)*(1-p2(3)), (1-p1(3))*p2(3), (1-p1(3))*(1-p2(3))];

v0=[p1(1)*p2(1), p1(1)*(1-p2(1)), (1-p1(1))*p2(1), (1-p1(1))*(1-p2(1))];

v = (1 - delta) * v0 / (eye(4) - delta * M);
end