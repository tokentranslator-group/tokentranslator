from grammars import gm_to_cnf
from grammars import grammer, grammer_pow, grammer_pow_a, grammer_pow_f
from lex import lex
from cyk import cyk
from trees import convert
from op_to_out import convert as convert_out


def old_test(s):
    # transform grammer to Chomsky normal form:
    grammer_cnf = gm_to_cnf(grammer)

    # parse
    p, t = cyk(goal=s, grammer=grammer_cnf)
    
    # convert parse tree to operator's tree:
    ot = convert(t)

    print('\nresult:')
    return(ot)


def pow_test(s):
    # transform grammer to Chomsky normal form:
    grammer_pow_cnf = gm_to_cnf(grammer_pow_a)

    # parse:
    p, t = cyk(goal=s, grammer=grammer_pow_cnf)

    # convert parse tree to operator's tree:
    ot = convert(t)

    print('\nresult:')
    return(ot)


def sym_step(goal_sent):

    '''Transform list of Word's into operation's tree'''

    # transform grammar to cnf:
    grammer_cnf = gm_to_cnf(grammer_pow_f)

    # parse
    p, t = cyk(goal=goal_sent, grammer=grammer_cnf)
    
    # convert parse tree to operator's tree:
    ot = convert(t)

    print('\nresult:')
    return(ot)


def word_lex_test(s, lex_repacer=lambda x:x[0]):

    '''Transform string s into parser tree, then
    operation tree, then convert result by replacing
    all lexem with it's values'''

    # lexical step:
    goal_sent = lex(sent=s)

    # for case goal_sent = a (like s='U'):
    if len(goal_sent) == 1:
        res = convert_out(goal_sent, lex_repacer)
        return(res)

    # for case like goal_sent = -(a+ ...) or -a
    if goal_sent[0] == '-':
        if len(goal_sent) == 2:
            # like -a:
            res = convert_out(goal_sent, lex_repacer)
            return(res)
        else:
            # like -(a+a)
            prefix, goal_sent = goal_sent[0], goal_sent[1:]
            ot = sym_step(goal_sent)
            res = convert_out(ot, lex_repacer)
            return(prefix+res)
    
    # for all other cases:
    ot = sym_step(goal_sent)
    res = convert_out(ot, lex_repacer)
    return(res)


def parse(sent):
    '''Parse sent with cyk parser and lexems from lex.

    Algorithm:

    1) lexical analysis:
          U'=c*(D[U,{x,2}+sin(x))]
       to
          a*(a+fa))
       where each a, f is type of Word, and contain original
       lexems in lex arg. (f is short for sin(,cos(,...)
    2) 1 to parse tree (by CYK):
    with grammar:
       E -> E{+-}T|T
       T->T{*/}F|T{*/}W|T{*/}V|F
       W -> (E)^
       V -> f(E)
       F->(E)|a
    (grammar_pow_f from grammars.py)
    to parse tree:
    ('E', ('T', 'T1'))
        child 0: ('T', 'a')
        child 1: ('T1', ('M', 'F'))
           child 0: ('M', '*')
           child 1: ('F', ('L', 'F1'))
              child 0: ('L', '(')
              child 1: ('F1', ('E', 'R'))
                 child 0: ('E', ('E', 'E1'))
                    child 0: ('E', 'a')
                    child 1: ('E1', ('P', 'T'))
                       child 0: ('P', '+')
                       child 1: ('T', ('LF', 'V1'))
                          child 0: ('LF', 'f')
                          child 1: ('V1', ('E', 'RF'))
                             child 0: ('E', 'a')
                             child 1: ('RF', ')')
                 child 1: ('R', ')')
    3) Convert parse tree to operator's tree
    (with convert from trees.py):
       ('M', '*')
            child 0: ('P', '+')
               child 0: ('E', 'a')
                  child 0: ('RF', ')')
                  child 1: ('LF', 'f')
               child 1: ('E', 'a')
               child 2: ('R', ')')
               child 3: ('L', '(')
            child 1: ('T', 'a')

    4) Transform operator's tree to out by replacing lexems
    with func lex_repacer (with convert from op_to_out.py):
    for lex_repacer = lambda x:x[0] result should be same as
    original sent (see op_to_out.py for more):
       
       c*(D[U,{x,2}+sin(x))]

    END OF Algorithm.

    Input:
    snet - string either like "U'= F" or "F" where
           F must satisfy grammar's rules and lexem's patterns.
    Return:
    converted sent.
    
'''
    # remove spaces:
    sent = sent.replace(' ', "")

    # work with equations
    if '=' in sent:
        # like eq: U'= sin(x)
        prefix, sent = sent.split('=')
    else:
        # like eq: sin(x)
        prefix = ""
    
    # this function work with lexems in postprocessing:
    # in that case it just return lexem original value
    # because Word.lex = [lexem, re.math object]
    def lex_repacer(lex):
        if type(lex) == str:
            if len(lex) > 0:
                # for prefix case:
                return(lex+'=')
        else:
            return(lex[0])

    prefix = lex_repacer(prefix)

    # main work:
    sent_out_list = word_lex_test(sent, lex_repacer)
    
    # put prefix back:
    res = [prefix]+[sent_out_list]
    return(res)


if __name__ == '__main__':
    # s = sys.argv[sys.argv.index('-s')+1]
    
    result_old = old_test(s='a*(a+a)+(a+a)*a')
    result_new = pow_test(s='a*(a+a)+(a+a)*a')
    result_new_pow = pow_test(s='a*(a+aw+(a+a)*a')
    result_new_pow = pow_test(s='(a+a)*a+a*(a+(a+a)w')
    result_word_lex = word_lex_test(s="a+U*U*V+D[V,{y,1}]-c*D[U,{x,2}]")
    result_word_lex_pow = word_lex_test(s="a+(D[V,{y,1}]-c*D[U,{x,2}])^3")
    result_word_lex_func = word_lex_test(s="sin(a+c)+cos(U-c*D[U,{x,2}])")
 
    print("\nresult old:")
    print("input: %s" % ('a*(a+a)+(a+a)*a'))
    print(result_old)

    print("\nresult new:")
    print("input: %s" % ('a*(a+a)+(a+a)*a'))
    print(result_new)

    print("\nresult new pow:")
    print("input: %s" % ('(a+a)*a+a*(a+(a+a)w'))
    print(result_new_pow)
    
    print("\nresult word_lex_test:")
    print("\ninput: %s\n" % ('a+U*U*V+D[V,{y,1}]-c*D[U,{x,2}]'))
    print(result_word_lex)
    print('\nconverted:')
    print(convert_out(result_word_lex))

    print("\nresult word_lex_pow:")
    print("\ninput: %s\n" % ("a+(D[V,{y,1}]-c*D[U,{x,2}])^3"))
    print(result_word_lex_pow)
    print('\nconverted:')
    print(convert_out(result_word_lex_pow))

    print("\nresult word_lex_func:")
    print("\ninput: %s\n" % ("sin(a+c)+cos(U-c*D[U,{x,2}])"))
    print(result_word_lex_func)
    print('\nconverted:')
    print(convert_out(result_word_lex_func))
