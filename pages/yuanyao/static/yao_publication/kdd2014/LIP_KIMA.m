function LIP_KIMA(Q,A,M,k_init,k_inc,k_test,eta,lambda,dim)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Q and A are the feature matrices for questions and answers with normalized scores/labels in the first column
% M is the association matrix
% k_init is the initial size of training set (percentage)
% k_inc is the incremental size of data (percentage)
% k_test is the size of test set (percentage)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

nq = size(Q,1);
na = size(A,1);
Q = [Q ones(nq,1)];
A = [A ones(na,1)];
f = size(Q,2);

fprintf('nq na: %d %d \n', nq, na);

k_init = floor(k_init * nq);
k_inc = floor(k_inc * nq);
k_test = floor(k_test * nq);

% test set
Mtest = M((nq-k_test):nq,:);
[Itest,Jtest] = find(Mtest);
Qtest = Q((nq-k_test):nq,2:f);
Atest = A(Jtest,2:f);
Utest = full(Q((nq-k_test):nq,1));
Vtest = full(A(Jtest,1));


Mt = M(1:k_init,:);
[It,Jt] = find(Mt);
Mt = Mt(:,Jt);
Qt = Q(1:k_init,2:f);
At = A(Jt,2:f);
Ut = full(Q(1:k_init,1));
Vt = full(A(Jt,1));
KAt = full(Kernelize(Qt));
KBt = full(Kernelize(At));

base_q = k_init;
base_a = size(Mt,2);


fprintf('inc-rmse_q inc-rmse_a \n');

[Lq,Dq] = eigs(KAt,dim);
[La,Da] = eigs(KBt,dim);
L = [Lq, zeros(base_q,dim); zeros(base_a,dim), La];
D1=diag(Dq);
D2=diag(Da);
D = spdiags([D1;D2],0,dim*2,dim*2);
ML2 = Mt*La;
GL = [Lq, -ML2; -Mt'*Lq, Mt'*ML2];
X = [L, eta*GL];
DL = D*L';
Y = [DL; DL];
thetat_0 = 1/lambda*([Ut;Vt] - X*(inv(lambda*eye(4*dim)+Y*X)*(Y*[Ut;Vt])));


KAtest = full(KernelizeTest(Qtest,Qt));
KBtest = full(KernelizeTest(Atest,At));
test_q_label_predict = KAtest * thetat_0(1:base_q);
test_a_label_predict = KBtest * thetat_0(base_q+1:base_q+base_a);
rmse_q = sqrt(norm(Utest - test_q_label_predict)^2 / size(test_q_label_predict,1));
rmse_a = sqrt(norm(Vtest - test_a_label_predict)^2 / size(test_a_label_predict,1));
fprintf('%0.4f %0.4f \n', rmse_q, rmse_a);

maxiter = 1000;
inc_q = k_inc;
iter = 0;
while base_q < (nq-k_test) && iter < maxiter
    mt = M((base_q+1):(base_q+inc_q),:);
    [Ii,Ji] = find(mt);
    mt = mt(:,Ji);
    inc_a = size(mt,2);
    
    qt = Q(base_q+1:base_q+inc_q,2:f);
    at = A(Ji,2:f);
    ut = Q(base_q+1:base_q+inc_q,1);
    vt = A(Ji,1);
    
    kat = KernelizeTest(qt,Qt);
    kbt = KernelizeTest(at,At);
    
    Dinvq = inv(Dq);
    Dinva = inv(Da);
    [m,n] = size(Mt);
    [mm,nn] = size(mt);
    [Im,Jm,Vm] = find(Mt);
    [Imm,Jmm,Vmm] = find(mt);
    Imm = Imm + m;
    Jmm = Jmm + n;
    Mt = sparse([Im;Imm],[Jm;Jmm],[Vm;Vmm],m+mm,n+nn);
    
    Xq = [Lq; kat*Lq*Dinvq];
    [Wq,Lqq,Pq] = svds(Xq,dim);
    temp_this = Lqq*Pq'*Dq*Pq*Lqq';
    [Yq,Dqq] = eig(temp_this);
    WYq = Wq*Yq;
    
    Xa = [La; kbt*La*Dinva];
    [Wa,Laa,Pa] = svds(Xa,dim);
    temp_this = Laa*Pa'*Da*Pa*Laa';
    [Ya,Daa] = eig(temp_this);
    WYa = Wa*Ya;

    WY = [WYq, zeros(base_q+inc_q,dim); zeros(base_a+inc_a,dim), WYa];
    D1=diag(Dqq);
    D2=diag(Daa);
    D = spdiags([D1;D2],0,dim*2,dim*2);
    ML2 = Mt*WYa;
    GW = [WYq, -ML2; -Mt'*WYq, Mt'*ML2];
    X = [WY, eta*GW];
    DW = D*WY';
    Y = [DW; DW];
    thetat2 = 1/lambda*([Ut;ut;Vt;vt] - X*(inv(lambda*eye(4*dim)+Y*X)*(Y*[Ut;ut;Vt;vt])));

    Qt = [Qt; qt];
    At = [At; at];
    Ut = [Ut; ut];
    Vt = [Vt; vt];
    
    KAtest = full(KernelizeTest(Qtest,Qt));
    KBtest = full(KernelizeTest(Atest,At));
    test_q_label_predict = KAtest * thetat2(1:base_q+inc_q);
    test_a_label_predict = KBtest * thetat2(base_q+inc_q+1:base_q+inc_q+base_a+inc_a);
    rmse_q = sqrt(norm(Utest - test_q_label_predict)^2 / size(test_q_label_predict,1));
    rmse_a = sqrt(norm(Vtest - test_a_label_predict)^2 / size(test_a_label_predict,1));
    fprintf('%0.4f %0.4f \n', rmse_q, rmse_a);
    
    Lq = WYq;
    Dq = Dqq;
    La = WYa;
    Da = Daa;
    
    iter = iter + 1;
    base_q = base_q+inc_q;
    base_a = base_a+inc_a;

end

end

