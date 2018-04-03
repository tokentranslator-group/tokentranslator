'''
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

'''
from grammars import gm_to_cnf
from grammars import grammar_pow_f
from grammars import gm_pow_f_args
from lex import lex
from cyk import cyk
from trees import convert
from op_to_out import flatten
from op_to_out import map_tree, map_tree_postproc
# from replacer import lex_replacer
from replacer_cpp import CppGen


class Equation():

    def __init__(self, sent):
        self.sent = sent
        self.cpp_replacer = CppGen()

    def _sym_step(self, goal_sent):

        '''Transform list of Word's into operation's tree'''

        # transform grammar to cnf:
        grammar_cnf = gm_to_cnf(gm_pow_f_args)  # grammar_pow_f

        # parse
        p, t = cyk(goal=goal_sent, grammar=grammar_cnf)
        # return(t)
        # convert parse tree to operator's tree:
        ot = convert(t)

        print('\nresult:')
        return(ot)

    def _transform_sent_to_tree(self, sent):

        '''Transform string s into parser tree, then
        operation tree, then convert result by replacing
        all lexem with it's values'''

        # lexical step:
        goal_sent = lex(sent=sent)

        lex_replacer = self.cpp_replacer

        # for case goal_sent = a (like s='U'):
        if len(goal_sent) == 1:
            res = flatten(goal_sent, lex_replacer)
            return(res)

        # for case like goal_sent = -(a+ ...) or -a
        if goal_sent[0] == '-':
            if len(goal_sent) == 2:
                # like -a:
                res = flatten(goal_sent, lex_replacer)
                return(res)
            else:
                # like -(a+a)
                prefix, goal_sent = goal_sent[0], goal_sent[1:]
                ot = self._sym_step(goal_sent)
                res = flatten(ot, lex_replacer)
                return(prefix+res)

        # for all other cases:
        ot = self._sym_step(goal_sent)
        self.operator_tree = ot
        res = flatten(ot, lex_replacer)
        return(res)

    def parse(self):

        '''Parse sent with cyk parser and lexems from lex.

        Input:
        snet - string either like "U'= F" or "F" where
               F must satisfy grammar's rules and lexem's patterns.
        Return:
        converted sent.
        '''
        sent = self.sent
        # remove spaces:
        sent = sent.replace(' ', "")

        # work with equations
        if '=' in sent:
            # like eq: U'= sin(x)
            prefix, sent = sent.split('=')
            prefix = prefix + '='
        else:
            # like eq: sin(x)
            prefix = ""

        # main work:
        sent_out_list = self._transform_sent_to_tree(sent)

        # put prefix back:
        res = [prefix]+sent_out_list
        self.result = res

    def show(self):
        # print("self.result")
        # print(self.result)
            
        # try:
        '''
        s = []
        d = []
        for term in self.result:
            try:
                d.append(term.global_data)
            except:
                pass
            try:
                try:
                    index = term.global_data['delay']
                    s.append([term.out, index])
                except:
                    if type(term) == str:
                        s.append(term)
                    else:
                        s.append(term.out)
            except:
                
                s.append(term.name)
        print("global_data")
        print(d)
        print("\neq result:")
        print(s)
        '''
        '''
        except:
            raise(BaseException('result not redy: use parse first'))
        '''
    # FOR set out cpp parameters:
    def set_dim(self, **kwargs):

        '''dim=2'''

        self.cpp_replacer.set_dim(**kwargs)
    
    def set_blockNumber(self, **kwargs):
        '''blockNumber=0'''
        self.cpp_replacer.set_blockNumber(**kwargs)

    def set_vars_indexes(self, **kwargs):

        ''' Shift index for variable:
        like (U,V)-> (source[+0], source[+1])

        Input:
        vars_to_indexes=[('U', 0), ('V', 1)]
        '''

        self.cpp_replacer.set_vars_indexes(**kwargs)
        
    def set_diff_type(self, **kwargs):

        '''
        Inputs:
           diffType="pure", diffMethod="common"

           diffType="pure", diffMethod="special",
           side=0, func="sin(x)"

           diffType="pure", diffMethod="interconnect",
           side=0, firstIndex=0, secondIndexSTR=1
        '''

        self.cpp_replacer.set_diff_type(**kwargs)

    def set_point(self, **kwargs):

        '''For bound like "V(t-1.1,{x,1.3}{y, 5.3})".

        Input:
        point=[3, 3]'''

        self.cpp_replacer.set_point(**kwargs)
        
    def set_coeffs_indexes(self, **kwargs):

        '''map coeffs ot it's index
        like (a,b)-> (params[+0], params[+1])

        Input:
        coeffs_to_indexes=[('a', 0), ('b', 1)]
        '''
        self.cpp_replacer.set_coeffs_indexes(**kwargs)

    # END FOR


def test():
    sa = 'a*(a+fa,a,a,))'
    eq = Equation(sa)

    tests = ['(a)', '(a+a)', 'a*(a+a)', 'a+(a+a)*a',
             sa, 'fa)', 'fa,)']

    # sym tests:
    outs = []

    for test in tests:
        op_tree = eq._sym_step(test)
        flat = flatten(op_tree, eq.cpp_replacer)
        '''
        try:
            outs.append(eq._sym_step(test))
        except:
            outs.append("fail for %s " % (test))
        '''
    print("\nouts:")
    for out in outs:
        print(out)


def test_1():
    '''Test tree chengings.
    '''
    input_word_lex_func = "(V(t-3.1)*U(t-3.1)+V(t-1.1)*U(t-3.1)+U(t-1.1))^3+cos(U-c*D[U,{x,2}])"
    eq = Equation(input_word_lex_func)

    eq.set_dim(dim=2)
    eq.set_blockNumber(blockNumber=0)

    eq.set_vars_indexes(vars_to_indexes=[('U', 0), ('V', 1)])

    coeffs_to_indexes = [('a', 0), ('b', 1), ('c', 2)]
    eq.set_coeffs_indexes(coeffs_to_indexes=coeffs_to_indexes)

    eq.set_diff_type(diffType='pure',
                     diffMethod='common')
    eq.set_point(point=[3, 3])

    eq.parse()
    # return(eq)
    cpp_fl = flatten(eq.operator_tree, eq.cpp_replacer)
    cpp_map = map_tree(eq.operator_tree, eq.cpp_replacer)
    cpp_map_postproc = map_tree_postproc(cpp_map, eq.cpp_replacer)
    return(cpp_map_postproc)
    return(cpp_map)
    return(cpp_fl)


if __name__ == '__main__':
    test_1()
