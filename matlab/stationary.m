function v=stationary(s1,s2,delta); 

y1=s1(1); p1=s1(2); q1=s1(3); r1=p1-q1;
y2=s2(1); p2=s2(2); q2=s2(3); r2=p2-q2;
y1b=1-y1; q1b=1-q1; r1b=-r1; 
y2b=1-y2; q2b=1-q2; r2b=-r2; 

D1 =1 - delta ^ 2 * r1 * r2; D2 = (1 - delta * r1 * r2) * D1; 

v1=(1-delta)*y1*y2/D1+delta*(q1+r1*((1-delta)*y2+delta*q2))*(q2+r2*((1-delta)*y1+delta*q1))/D2; 
v2=(1-delta)*y1*y2b/D1+delta*(q1+r1*((1-delta)*y2+delta*q2))*(q2b+r2b*((1-delta)*y1+delta*p1))/D2;
v3=(1-delta)*y1b*y2/D1+delta*(q1b+r1b*((1-delta)*y2+delta*p2))*(q2+r2*((1-delta)*y1+delta*q1))/D2; 
v4=(1-delta)*y1b*y2b/D1+delta*(q1b+r1b*((1-delta)*y2+delta*p2))*(q2b+r2b*((1-delta)*y1+delta*p1))/D2; 

v=[v1,v2,v3,v4];
end