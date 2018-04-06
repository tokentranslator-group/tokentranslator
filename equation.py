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
from op_to_out import map_tree, map_tree_postproc
from replacer_cpp import CppGen
from nodes import NodeCommon

import logging

# create logger
log_level = logging.INFO  # logging.DEBUG
logging.basicConfig(level=log_level)
logger = logging.getLogger('equation.py')
logger.setLevel(level=log_level)


class Equation():

    def __init__(self, sent, trace=0):
        self.sent = sent
        self.tree_cpp_replacer = CppGen()
        self.prefix = []
        self.operator_tree = None

        # for debugging:
        self.trace = trace

    def convert_to_node(self):

        '''Convert Word to node like object.
        For cpp replacing.
        For prefix and trivial kernel'''

        # convert prefix:
        self.prefix = [NodeCommon(char) for char in self.prefix]
        
        # convert trivial kernel:
        if not self.have_tree:  # type(self.kernel) == list:
            self.kernel = [NodeCommon(char) for char in self.kernel]
            
    def _sym_step(self, goal_sent):

        '''Transform list of Word's into operation's tree'''

        # transform grammar to cnf:
        grammar_cnf = gm_to_cnf(gm_pow_f_args)  # grammar_pow_f

        # parse
        logger.debug("for cyk:")
        logger.debug(goal_sent)
        p, t = cyk(goal=goal_sent, grammar=grammar_cnf)
        self.from_cyk = (p, t)

        # return(t)
        # convert parse tree to operator's tree:
        ot = convert(t)
        self.operator_tree = ot

        return(ot)

    def parse(self):

        '''Parse sent with cyk parser and lexems from lex.

        Input:
        snet - string either like "U'= F" or "F" where
               F must satisfy grammar's rules and lexem's patterns.
        Return:
        converted sent.
        '''
        self.prefix = []
        self.kernel = []

        sent = self.sent
        # remove spaces:
        sent = sent.replace(' ', "")
        
        # tokenisation:
        sent = lex(sent=sent)
        self.from_lex = sent
        # return(goal_sent)

        # work with prefix:
        self._prefix_step(sent)

        # convert prefix and trivial cases
        # to term like objects (for replacer):
        self.convert_to_node()
        
        if self.have_tree:
            # make operator tree:
            self._sym_step(self.kernel)
            logger.debug("operator tree:")
            logger.debug(self.operator_tree)
        else:
            logger.debug("trivial case without tree")

    def _prefix_step(self, sent):
        
        self.have_tree = True

        if '=' in sent:
            # like eq: U'= sin(x)
            prefix = sent[:sent.index('=')-1]
            kernel = sent[sent.index('=')+1:]
            self.prefix.extend(prefix)
            self.prefix.append('=')
            self.kernel = kernel
        else:
            # like eq: sin(x)
            self.prefix = []
            kernel = sent
            self.kernel = kernel

        # for case sent = a (like s='U'):
        if len(kernel) == 1:
            self.kernel = kernel
            self.have_tree = False
            
        # for case like goal_sent = -(a+ ...) or -a
        if kernel[0] == '-':
            if len(kernel) == 2:
                # like -a:
                self.prefix.append('-')
                self.kernel = kernel[1:]
                self.have_tree = False
            else:
                # like -(a+a)
                self.prefix.append(kernel[0])
                self.kernel = kernel[1:]

    def map_cpp(self):

        '''Add cpp out to self.prefix and self.operator_tree
        or self.kernel (if tree is trivial)'''

        cpp_map_prefix = [map_tree(term, self.tree_cpp_replacer)
                          for term in self.prefix]
        cpp_map_prefix_post = [map_tree_postproc(term, self.tree_cpp_replacer)
                               for term in cpp_map_prefix]
        if self.have_tree:
            
            cpp_map = map_tree(self.operator_tree, self.tree_cpp_replacer)
            cpp_map_postproc = map_tree_postproc(cpp_map,
                                                 self.tree_cpp_replacer)
            return(cpp_map_prefix_post, [cpp_map_postproc])
        else:
            cpp_map_kernel = [map_tree(term, self.tree_cpp_replacer)
                              for term in self.kernel]
            cpp_map_ker_p = [map_tree_postproc(term, self.tree_cpp_replacer)
                             for term in cpp_map_kernel]
            return(cpp_map_prefix_post, cpp_map_ker_p)

    def flatten(self, key):

        '''Return list of term as key.
        Key either original or cpp.'''
        
        if key == 'cpp':
            prefix, kernel = self.map_cpp()
        elif key == 'original':
            prefix = self.prefix
            if self.have_tree:
                kernel = [self.operator_tree]
            else:
                kernel = self.kernel

        logger.debug("prefix")
        logger.debug(prefix)
        logger.debug("kernel")
        logger.debug(kernel)

        # ['(', 'a']
        out_prefix = [term.flatten(key)[0] for term in prefix]
        if self.have_tree:
            # [['(', 'a']]
            out_kernel = [term.flatten(key) for term in kernel][0]
        else:
            # [['a'], [')']]
            out_kernel = [term.flatten(key)[0] for term in kernel]

        logger.debug("out_prefix")
        logger.debug(out_prefix)
        logger.debug("out_kernel")
        logger.debug(out_kernel)

        out = out_prefix + out_kernel
        return("".join(out))

    def show_original(self):
        print(self.flatten("original"))

    def show_cpp(self):
        print(self.flatten('cpp'))

    def show_tree_original(self):
        if self.have_tree:
            self.operator_tree.show_original()
    
    def show_tree_cpp_out(self):
        if self.have_tree:
            self.operator_tree.show_cpp_out()
        
    def show_tree_cpp_data(self):
        if self.have_tree:
            self.operator_tree.show_cpp_data()

    # FOR set out cpp parameters:

    def set_default(self):
        self.set_dim(dim=2)
        self.set_blockNumber(blockNumber=0)

        self.set_vars_indexes(vars_to_indexes=[('U', 0), ('V', 1)])

        coeffs_to_indexes = [('a', 0), ('b', 1), ('c', 2)]
        self.set_coeffs_indexes(coeffs_to_indexes=coeffs_to_indexes)

        self.set_diff_type(diffType='pure',
                           diffMethod='common')
        self.set_point(point=[3, 3])

    def set_dim(self, **kwargs):

        '''dim=2'''

        self.tree_cpp_replacer.set_dim(**kwargs)
    
    def set_blockNumber(self, **kwargs):
        '''blockNumber=0'''
        self.tree_cpp_replacer.set_blockNumber(**kwargs)

    def set_vars_indexes(self, **kwargs):

        ''' Shift index for variable:
        like (U,V)-> (source[+0], source[+1])

        Input:
        vars_to_indexes=[('U', 0), ('V', 1)]
        '''

        self.tree_cpp_replacer.set_vars_indexes(**kwargs)
        
    def set_diff_type(self, **kwargs):

        '''
        Inputs:
           diffType="pure", diffMethod="common"

           diffType="pure", diffMethod="special",
           side=0, func="sin(x)"

           diffType="pure", diffMethod="interconnect",
           side=0, firstIndex=0, secondIndexSTR=1
        '''

        self.tree_cpp_replacer.set_diff_type(**kwargs)

    def set_point(self, **kwargs):

        '''For bound like "V(t-1.1,{x,1.3}{y, 5.3})".

        Input:
        point=[3, 3]'''

        self.tree_cpp_replacer.set_point(**kwargs)
        
    def set_coeffs_indexes(self, **kwargs):

        '''map coeffs ot it's index
        like (a,b)-> (params[+0], params[+1])

        Input:
        coeffs_to_indexes=[('a', 0), ('b', 1)]
        '''
        self.tree_cpp_replacer.set_coeffs_indexes(**kwargs)

    # END FOR


tests = [("(V(t-3.1)*U(t-3.1)+V(t-1.1)*U(t-3.1)+U(t-1.1))^3"
          + "+cos(U-c*D[U,{x,2}])"),
         ("U'=(V(t-3.1)*U(t-3.1)+V(t-1.1)*U(t-3.1)+U(t-1.1))^3"
          + "+cos(U-c*D[U,{x,2}])"),
         "U'=U",
         "U'=-U",
         "U'=-(U+V)",
         "U",
         "-(U(t-1.1)+V)",
         "U'=-(U(t-1.1)+V)",
         "f(x, y,)+g(y,z,)+h(x,z,)"]


def test():
    
    eqs = [Equation(test) for test in tests]

    for _id, eq in enumerate(eqs):
        print("\n=== test %s: %s ===" % (_id, tests[_id]))
        try:
            eq.parse()
        except:
            print(eq.from_lex)
            print(eq.from_cyk)

        eq.set_default()

        print('\noriginal:')
        eq.show_original()

        print('\ncpp:')
        eq.show_cpp()

        '''
        try:

        except:
            outs.append("fail for %s " % (test))
        '''


def test_1():
    '''
    outs.append(eq.flatten('original')
    outs.append(eq._sym_step(test))

    cpp_fl = flatten(eq.operator_tree, eq.tree_cpp_replacer)
    cpp_fl = eq.operator_tree.flatten('cpp')
    cpp_map = map_tree(eq.operator_tree, eq.tree_cpp_replacer)
    cpp_map_postproc = map_tree_postproc(cpp_map, eq.tree_cpp_replacer)

    print("original:")
    print(cpp_map_postproc.flatten('original'))
    print("cpp:")
    print(cpp_map_postproc.flatten('cpp'))

    return(cpp_map_postproc)
    return(cpp_map)
    return(cpp_fl)
    '''
    pass


if __name__ == '__main__':
    test()
