function LIP_KIM(Q,A,M,k_init,k_inc,k_test,eta,lambda)
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
St = inv([(eta+1)*KAt+lambda*speye(base_q),  -eta*Mt*KBt; -eta*Mt'*KAt,  KBt+eta*(Mt'*Mt)*KBt+lambda*speye(base_a)]);
thetat_0 = St * ([Ut; Vt]);


KAtest = full(KernelizeTest(Qtest,Qt));
KBtest = full(KernelizeTest(Atest,At));

test_q_label_predict = KAtest * thetat_0(1:base_q);
test_a_label_predict = KBtest * thetat_0(base_q+1:base_q+base_a);
rmse_q = sqrt(norm(Utest - test_q_label_predict)^2 / size(test_q_label_predict,1));
rmse_a = sqrt(norm(Vtest - test_a_label_predict)^2 / size(test_a_label_predict,1));
fprintf('%0.4f %0.4f \n', rmse_q, rmse_a);

inc_q = k_inc;
iter = 0;
maxiter = 1000;
while base_q < (nq-k_test) && iter < maxiter
    mt = M((base_q+1):(base_q+inc_q),:);
    [Ii,Ji] = find(mt);
    mt = mt(:,Ji);
    inc_a = size(mt,2);
    
    qt = Q((base_q+1):(base_q+inc_q),2:f);
    at = A(Ji,2:f);
    ut = full(Q((base_q+1):(base_q+inc_q),1));
    vt = full(A(Ji,1));

    kat = KernelizeTest(qt,Qt);
    kat=kat';
    katt = KernelizeTest(at,At);
    kbt = Kernelize(qt,qt);
    kbt = kbt';
    kbtt = Kernelize(at,at);

    X = [(eta+1)*kat  -eta*(Mt*kbt); -eta*(Mt'*kat)  kbt+eta*(Mt'*(Mt*kbt))];
    Y = [(eta+1)*kat'  -eta*mt*kbt'; -eta*mt'*kat'  kbt'+eta*(mt'*mt)*kbt'];
    Z = [(eta+1)*katt+lambda*speye(inc_q)  -eta*mt*kbtt; -eta*mt'*katt  kbtt+eta*(mt'*mt)*kbtt+lambda*speye(inc_a)];
    QQ = inv(Z-Y*St*X);
    thetat = [thetat_0 + St*(X*(QQ*(Y*thetat_0-[ut;vt]))); -inv(Z)*(Y*(thetat_0+St*(X*(QQ*(Y*thetat_0))))) + QQ*[ut;vt]];    
    thetat = [thetat(1:base_q,:); thetat(base_q+base_a+1:base_q+base_a+inc_q,:); thetat(base_q+1:base_q+base_a,:); thetat(base_q+base_a+inc_q+1:base_q+base_a+inc_q+inc_a,:)];

    [m,n] = size(Mt);
    [mm,nn] = size(mt);
    [Im,Jm,Vm] = find(Mt);
    [Imm,Jmm,Vmm] = find(mt);
    Imm = Imm + m;
    Jmm = Jmm + n;
    Mt = sparse([Im;Imm],[Jm;Jmm],[Vm;Vmm],m+mm,n+nn);
    Qt = [Qt;qt];
    At = [At;at];
   
    % accuacy on test set
    KAtest = full(KernelizeTest(Qtest,Qt));
    KBtest = full(KernelizeTest(Atest,At));
    test_q_label_predict = KAtest * thetat(1:base_q+inc_q);
    test_a_label_predict = KBtest * thetat(base_q+inc_q+1:base_q+inc_q+base_a+inc_a);
    rmse_q = sqrt(norm(Utest_con - test_q_label_predict)^2 / size(test_q_label_predict,1));
    rmse_a = sqrt(norm(Vtest_con - test_a_label_predict)^2 / size(test_a_label_predict,1));
    fprintf('%0.4f %0.4f ', rmse_q, rmse_a);

    % update St = [St + temp_inv*Y*St  -temp_inv; -inv(Z)*Y*(St+temp_inv*Y*St) QQ];
    temp_this = St*X*QQ;
    St = [St + temp_this*(Y*St)  -temp_this; -inv(Z)*Y*St-inv(Z)*Y*temp_this*Y*St QQ];
    St = [St(1:base_q,:); St(base_q+base_a+1:base_q+base_a+inc_q,:); St(base_q+1:base_q+base_a,:); St(base_q+base_a+inc_q+1:base_q+base_a+inc_q+inc_a,:)];
    St = [St(:,1:base_q) St(:,base_q+base_a+1:base_q+base_a+inc_q) St(:,base_q+1:base_q+base_a) St(:,base_q+base_a+inc_q+1:base_q+base_a+inc_q+inc_a)];

    thetat_0 = thetat;
    iter = iter + 1;
    base_q = base_q+inc_q;
    base_a = base_a+inc_a;
end

end

function Y = Kernelize(X)

    normX = sqrt(sum(X .^ 2, 2));
    C = bsxfun(@rdivide, X * X', normX);
    Y = bsxfun(@rdivide, C', normX);
    Y = Y';

end

function Z = KernelizeTest(X,Y)

    normX = sqrt(sum(X .^ 2, 2));
    normY = sqrt(sum(Y .^ 2, 2));
    C = bsxfun(@rdivide, X * Y', normX);
    Z = bsxfun(@rdivide, C', normY);
    Z = Z';

end



