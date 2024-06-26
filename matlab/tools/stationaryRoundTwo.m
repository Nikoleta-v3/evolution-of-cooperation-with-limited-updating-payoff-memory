function v=stationaryRoundTwo(s1,s2,delta);
% Calculates the probabilities of being at CC|CC, CC|CD, CC|DC, .. etc at the last
% two rounds.

M=[s1(2) * s2(2), s1(2) * (1-s2(2)), (1-s1(2)) * s2(2), (1-s1(2)) * (1-s2(2));
    s1(3) * s2(2), s1(3) * (1-s2(2)), (1-s1(3)) * s2(2), (1-s1(3)) * (1-s2(2));
    s1(2) * s2(3), s1(2) * (1-s2(3)), (1-s1(2)) * s2(3), (1-s1(2)) * (1-s2(3));
    s1(3) * s2(3), s1(3) * (1-s2(3)), (1-s1(3)) * s2(3), (1-s1(3)) * (1-s2(3))];

v0 = [s1(1) * s2(1), s1(1) * (1-s2(1)), (1-s1(1)) * s2(1), (1-s1(1)) * (1-s2(1))];
v = zeros(4, 4);
rhs = v0 / (eye(4) - delta * M);

for i=1:4
    for j=1:4
        v(i, j) = (1 - delta) * M(i, j) * (delta ^ 2) * rhs(i);
    end
end

v = reshape(v.',[1, 16]);
end