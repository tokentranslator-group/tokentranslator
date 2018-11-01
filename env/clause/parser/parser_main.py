from translator.grammar.grammars import gm_to_cnf
from env.clause.data.grammars.cl_grammar import gm_0
from translator.grammar.cyk import cyk

from translator.tokenizer.tokenizer_main import ClTokenizer


from translator.tree.tree_converter import convert
from translator.tree.nodes import NodeCommon


import logging

# if using from tester.py uncoment that:
# create logger that child of tester loger
logger = logging.getLogger('clause.cl_parser')

# if using directly uncoment that:
'''
# create logger
log_level = logging.DEBUG  # logging.DEBUG
logging.basicConfig(level=log_level)
logger = logging.getLogger('eq_parser')
logger.setLevel(level=log_level)
'''


class ClParser():

    def __init__(self, net):
        self.net = net
        
        # FOR lex_nets:
        self.lex_nets = {}

        # patterns (lexems) for wolfram terms:
        self.lex_nets['wolfram'] = LexNetW()
        # END FOR

        # FOR tokenizers:
        self.tokenizers = {}

        # init wolfram tokenizer:
        self.tokenizers['wolfram'] = LexNetTokenizer(self.lex_nets['wolfram'])
        # END FOR
        
        self.tokenizer_current = self.tokenizers['wolfram']

        # lexical analysis of sent:
        self.lex = self.tokenizer_current.lex

    def parse(self):

        '''Parse sent with cyk parser and lexems from lex.

        Input:
        snet - string either like "U'= F" or "F" where
               F must satisfy grammar's rules and lexem's patterns.
        Return:
        operator tree self.eq_tree.
        '''

        sent = self.net.sent

        # work with prefix:
        sent = self._prefix_step(sent)

        self.eq_from_lex = self.lex(sent=sent)
                
        logger.debug("self.eq_from_lex:")
        logger.debug(self.eq_from_lex)

        self.eq_tree = self._sym_step(self.eq_from_lex)

        # convert left-midle-right part of eq
        # to tree (for replacer):
        # self._convert_to_node()

    def _prefix_step(self, sent):

        # remove spaces:
        sent = sent.replace(' ', "")
        return(sent)

    def _sym_step(self, goal_sent):

        '''Transform list of Word's into operation's tree
        with grammar'''

        # transform grammar to cnf:
        grammar_cnf = gm_to_cnf(gm_0)  # grammar_pow_f

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

    def _convert_to_node(self):

        '''Get eq_left, eq_mid, eq_right = self.eq
        it convert eq_left and eq_right to
        operator_tree, then convert eq_mid to Node like objects,
        then unite all to single Node like object.'''

        eq_left, eq_mid, eq_right = self.eq
        if eq_left is not None:
            eq_left = self._sym_step(eq_left)
        if eq_right is not None:
            eq_right = self._sym_step(eq_right)
        if eq_mid is not None:
            eq_mid = NodeCommon("".join(eq_mid))

            if (eq_left is not None
                and eq_right is not None):
                # case x=y
                eq_mid.children = [eq_right, eq_left]
            elif eq_left is None:
                # case -y -> 0-y
                eq_left = NodeCommon("0")
                eq_mid.children = [eq_right, eq_left]
            '''
            elif eq_right is None:
                # case y- -> y-0
                # y? -> ?+y
                eq_right = NodeCommon("0")
                eq_mid.children = [eq_right, eq_left]
            '''
            
            if eq_left is None and eq_right is None:
                raise(BaseException("eq_left or eq_right must exist"))

            eq_tree = eq_mid
        else:
            # if equation not like U'=sin(U) but
            # like sin(U)
            eq_tree = eq_right
        
        self.net.eq_tree = eq_tree
