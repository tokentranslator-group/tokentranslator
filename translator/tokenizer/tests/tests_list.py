'''
``tests_list_*`` for tests,
``*_asserted`` for tests result.
Don't forget add one's before
run tests'''


tests_list_cs = [
    ["group(A) \\and abelian(A) => Eq(A = A_1 + ... + A_n)Eq"],
    ["group(A_i) \\where(A_i:(order(A_i, p) \\and prime(p)))"],
    ['group(A) \\and abelian(A) \\and finite(A) => sum_of_prime(A)'],
    ['(group(A), abelian(A), finite(A)) => sum_of_prime(A)'],
    ['(\\for_all x) \\in X: Eq(x(t-1.0) == y)Eq'],
    ['((\\for_all x) \\in X: Eq(x(t-1.0) == y)Eq,',
     '(\\for_all y) \\in Y: Eq(y == z)Eq',
     ')\\into group(x) \\and group(Y)'],
    ['(\\for_all x) \\in X'],
    ["Let(x: x \\in X, g: abelian(g) in:"
     "group(x) \\and subgroup(x, g) => abelian(x)" + ")"],
    ["bilinear(f)=>Eq(f(x,y)=g(x,y)+h(x,y))Eq"
     + "\\where(g: simmetric(g), h: simplectic(g))"],
    ["bilinear_form(f) => (\\exist e1, e2, e3):"
     + " Eq(g(x)=a0*x0^2+a1*x1^2+a2*x2^2)Eq"],
    ["Let(F: finite_field(F), E: finite_field(E),"
     + " G: galois_group(G, E, F) in:"
     + " Eq([E:F]==k)Eq => is_cyclic(G) \\and order(G, k))"]]

cs_asserted = [
    ['f(', 'a', ')', 'm', 'f(', 'a', ')', 'm', 'a'],
    ['f(', 'a', ')', 'm', '(', 'a', 'm',
     '(', 'f(', 'a', ',', 'a', ')', 'm', 'f(', 'a', ')))'],
    ['f(', 'a', ')', 'm', 'f(', 'a', ')',
     'm', 'f(', 'a', ')', 'm', 'f(', 'a', ')'],
    ['(', 'f(', 'a', '),', 'f(', 'a', '),', 'f(', 'a', '))',
     'm', 'f(', 'a', ')'],
    ['f(', 'a', ')', 'm', 'a', 'm', 'a'],

    ['(', 'f(', 'a', ')', 'm', 'a', 'm', 'a', ',',
     'f(', 'a', ')', 'm', 'a', 'm', 'a', ')', 'm',
     'f(', 'a', ')', 'm', 'f(', 'a', ')'],

    ['f(', 'a', ')', 'm', 'a'],
    ['f(', 'a', 'm', 'a', 'm', 'a', ',',
     'a', 'm', 'f(', 'a', ')', ',', 'f(', 'a', ')',
     'm', 'f(', 'a', ',', 'a', ')', 'm', 'f(', 'a', '))'],

    ['f(', 'a', ')', 'm', 'a', 'm', '(', 'a', 'm',
     'f(', 'a', '),', 'a', 'm', 'f(', 'a', '))'],

    ['f(', 'a', ')', 'm', 'f(', 'a', ',',
     'a', ',', 'a', ')', 'm', 'a'],

    ['f(', 'a', 'm', 'f(', 'a', '),', 'a', 'm',
     'f(', 'a', '),', 'a', 'm', 'f(', 'a', ',',
     'a', ',', 'a', ')', ',', 'a', 'm', 'f(', 'a', ')',
     'm', 'f(', 'a', ',', 'a', '))'],
]

tests_list_eqs = [
    ["a[i,j,] = a[j,i,]"],
    ["a.transpose().conjugate()"],
    ["a.t(f).s()"],
    ["a.t.r()"],
    ["a.t().s()"],
    ["a.t(f)"],
    ["a.t() = a"],
    ['x(t-1.0) == y'],
    ['y == z'],
    ["U'=a*(D[U,{x,2}]+ D[U,{y,2}])"],
    ["(V(t-1.1, {x, 0.7}{y, 0.7}))^3"],
    ["-(V+U)"],
    ["f(x, y)*t"],
    ["U'=a+U+U*U*V-(b+1)*U+c*D[U,{x,2}]"],
    ["U"],
    ["U'=2.0 - V"],
    ["U'=a*(sin(a+b)+(U)^3)"],
    ["+cos(U-c*D[U,{x,2}])"],
    ["U'=-(U(t-1.1)+V)"],
    ["f(x, y,)+g(y,z,)+h(x,z,)"],
    ["exp(t)"]
]
    
eqs_asserted = [
    ['f(', 'a', ',', 'a', ',', ')',
     '=', 'f(', 'a', ',', 'a', ',', ')'],
    ['a'],
    ['a'],
    ['a'],
    ['a'],
    ['a'],
    ['a', '=', 'a'],
    ['f(', 'a', '-', 'a', ')==', 'a'],
    ['a', '==', 'a'],
    ['a', '=', 'a', '*(', 'a', '+', 'a', ')'],
    ['(', 'a', ')w'],
    ['-(', 'a', '+', 'a', ')'],
    ['f(', 'a', ',', 'a', ')*', 'a'],
    ['a', '=', 'a', '+', 'a', '+', 'a', '*', 'a', '*', 'a',
     '-(', 'a', '+', 'a', ')*', 'a', '+', 'a', '*', 'a'],
    ['a'],
    ['a', '=', 'a', '-', 'a'],
    ['a', '=', 'a', '*(', 'f(', 'a', '+',
     'a', ')+(', 'a', ')w', ')'],
    ['+', 'f(', 'a', '-', 'a', '*', 'a', ')'],
    ['a', '=-(', 'a', '+', 'a', ')'],
    
    ['f(', 'a', ',', 'a', ',)+', 'f(', 'a', ',', 'a', ',)+', 'f(', 'a', ',', 'a', ',)'],
    
    ['f(', 'a', ')']]
