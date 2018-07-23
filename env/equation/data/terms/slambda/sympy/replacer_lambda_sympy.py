from translator.replacer.replacer import Gen

from env.equation.data.terms.slambda.sympy.patterns._list_values import terms_gens_value
from env.equation.data.terms.slambda.sympy.patterns.ids._list_ids import terms_gens_id
from env.equation.data.terms.slambda.sympy.patterns._list_br import terms_br_gens

import sympy
import random


import logging

# create logger
log_level = logging.INFO  # logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger('replacer_lambda_sympy.py')
logger.setLevel(level=log_level)


class Out():
    pass


class Params():
    pass


class LambdaSympyGen(Gen):

    '''Fill term.sympy with print_sympy,
    term.arg_rand (or term.arg_fix) with get_args_rand,
    term.arg_sympy with get_args
    and term.lambda_sympy with lambdify
    '''
    def __init__(self):

        pass

    def postproc(self, node):
        pass

    def translate_brackets(self, node):
        
        # ''Add to brackets like term''

        self.init_output((node))
        self.lambdify_br(node)

    def translate(self, node):

        # ''Add pattern out to term and return it''

        self.init_output((node))
        self.lambdify(node)

    def init_output(self, nodes):

        '''For add out to nodes'''

        for node in nodes:
            try:
                node.slambda
            except AttributeError:
                node.slambda = Out()
            # node.slambda.sympy = Out()
            # node.slambda.sympy.global_data = {}

    def set_slambda(self, node, value):

        node.slambda.sympy = value

    def get_params_field_name(self):
        return('term_lambda_sympy_params')
    
    def lambdify_br(self, node_br):
        
        '''Lambdefy func term'''

        left_node = node_br[0]
        # right_node = node_br[-1]
        args_node = node_br[1]

        term_id = self.get_term_id(left_node)

        if term_id == 'func':

            # FOR left_node (sin():
            if 'variable' in left_node.args:
                # for func like f, g, h value must exist
                # substituted with subs:
                func = left_node.args['variable']['value']
            else:
                # for func like sin, cos, exp:
                # func = left_node.name.lex[0][:-1]
                func = self.get_term_value(left_node)[:-1]
            # END FOR

            args_count = len(args_node)
            if args_count > 1:
                raise(BaseException("term func for lambda_sympy not"
                                    + " supported more then one argument"))

            self.set_slambda(left_node, terms_br_gens['func'](func, sympy))
            # self.set_slambda(left_node, lambda A: sympy.simplify(func)(A))
            # left_node.lambda_sympy = lambda A: sympy.simplify(func)(A)
        
    def lambdify(self, node):

        '''Add lambda expresion to some terms
        first try simple terms (with value) (include +,-,*,/)
        then with term_id (diff)
        finally use node.args['variable']['value'] (that must
        be substituted before)
        '''
        
        term_value = self.get_term_value(node)
        if term_value in terms_gens_value:
            self.set_slambda(node, terms_gens_value[term_value])
        
        else:
            term_id = self.get_term_id(node)

            if term_id in terms_gens_id:
                # TODO: replace to bracket:
                self.set_slambda(node, terms_gens_id[term_id](self, node,
                                                              sympy))
            
            elif term_id in ['var', 'free_var', 'coeffs']:
                var = node.args['variable']['value']
                # var = node.name.lex[0]

                # transform to sympy:
                self.set_slambda(node, lambda: var)
                # node.arg_sympy = sympy.symbols(names=var)
                # node.lambda_sympy = lambda: sympy.symbols(names=var)
        
        '''
        if term_value == '+':
            self.set_slambda(node, lambda L, R: L.__add__(R))
            # node.lambda_sympy = lambda L, R: L.__add__(R)
        elif term_value == '*':
            self.set_slambda(node, lambda L, R: L.__mul__(R))
            # node.lambda_sympy = lambda L, R: L.__mul__(R)
        elif term_value == '-':
            self.set_slambda(node, lambda L, R: R.__add__(-L))
            # node.lambda_sympy = lambda L, R: R.__add__(-L)
        elif term_value == '/':
            self.set_slambda(node, lambda L, R: R.__div__(L))
            # node.lambda_sympy = lambda L, R: R.__div__(L)
        
        elif term_value == '=':
            self.set_slambda(node, lambda L, R: L.__eq__(R))
            # node.lambda_sympy = lambda L, R: L.__eq__(R)
        elif term_value == '=-':
            self.set_slambda(node, lambda L, R: L.__eq__(-R))
            # node.lambda_sympy = lambda L, R: L.__eq__(-R)
        '''
