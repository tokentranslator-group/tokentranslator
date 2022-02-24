'''
 Cocke–Younger–Kasami algorithm:

let the input be a string I consisting of n characters: a1 ... an.
let the grammar contain r nonterminal symbols R1 ... Rr, with start symbol R1.
let P[n,n,r] be an array of booleans. Initialize all elements of P to false.
for each s = 1 to n
  for each unit production Rv -> as
    set P[1,s,v] = true
for each l = 2 to n -- Length of span
  for each s = 1 to n-l+1 -- Start of span
    for each p = 1 to l-1 -- Partition of span
      for each production Ra -> Rb Rc
        if P[p,s,b] and P[l-p,s+p,c] then set P[l,s,a] = true
if P[n,1,1] is true then
  I is member of language
else
  I is not member of language
REF: https://en.wikipedia.org/wiki/CYK_algorithm#As_pseudocode
'''
# from nodes import Node, copy_node
from tokentranslator.translator.tree.nodes import NodeR as Node, copy_node
'''
FOR
   E -> E+T|T
   T->T*F|F
   F->(E)|a
'''
grammar = [('E', 'EX'), ('E', 'TY'), ('E', 'LZ'), ('E', 'a'),
           ('X', 'PT'),
           ('T', 'TY'), ('T', 'LZ'), ('T', 'a'),
           ('Y', 'MF'),
           ('F', 'LZ'), ('F', 'a'),
           ('Z', 'ER'),

           ('P', r'+'), ('M', r'*'),
           ('L', '('), ('R', ')')]
# END FOR


def get_rules(grammar, term=True):

    ''' If term True return rulels like ['F', 'a'],
    else return rules like ['E', 'TX']'''

    # cond = lambda elm, term: not elm.isupper() if term else elm.isupper()
    cond = lambda elm, term: not elm[0].isupper() if term else elm[0].isupper()
    rules = [(parent, child) for parent, child in grammar
             if cond(child, term)]
    return(rules)


def init_P(grammar, length):
    P = dict([[(parent, s, p), False] for parent, child in grammar
              for s in range(1, length+1)
              for p in range(1, length+1)])
    return(P)


def cyk(goal=["(", "a", "+", "a", ")", "*", "a"],
        grammar=grammar, node_data=None, return_all=False):

    '''Cocke–Younger–Kasami algorithm.
    
    Input:
    
    - ``goal`` -- either list of string
    or list of Word's objects.

    - ``grammar`` -- grammar must be in Chomsky normal form (CNF)
    so use ``grammars.gm_to_cnf`` first. See examples in ``grammars.py``.

    - ``node_data`` -- dict, contained ops key (operators),
    special for each dialect. (ex: ["+", "-", "*"]).

    Output:

    parse tree.'''
    
    if type(goal) == str:
        words = list(goal)
    elif type(goal) == list:
        words = goal

    N = len(words)
    rule_term = get_rules(grammar, term=True)
    rule_unterm = get_rules(grammar, term=False)
    # print("rule_term")
    # print(rule_term)
    # print("rule_unterm")
    # print(rule_unterm)

    P = init_P(grammar, N)
    Tree = {}

    for s in range(1, N+1):  # 1..N
        for parent, child in rule_term:
            if child[0] == words[s-1]:
                P[(parent, s, 1)] = True
                # Tree[(parent, s, 1)] = [parent, child]
                # Tree[(parent, s, 1)] = Node(rule=(parent, child[0]))
                Tree[(parent, s, 1)] = Node(rule=(parent, words[s-1]),
                                            node_data=node_data)

    for l in range(2, N+1):  # 2..N
        for s in range(1, N-l+2):  # 1..N-l+1
            for p in range(1, l):  # 1..l-1
                for parent, child in rule_unterm:
                    left, right = child
                    # print("left, right: %s, %s" % (left, right))
                    '''
                    P[(parent, s, l)] = ((P[(left, s, p)]
                                          and P[(right, s+p, l-p)])
                                         or P[(parent, s, l)])
                    '''

                    if (P[(left, s, p)] and P[(right, s+p, l-p)]):
                        P[(parent, s, l)] = True
                        '''
                        # add node to simple tree:
                        Tree[(parent, s, l)] = [(parent, child),
                                                Tree[(left, s, p)],
                                                Tree[(right, s+p, l-p)], False]
                        '''
                        # add node to tree:
                        nodes_children = [copy_node(Tree[(left, s, p)]),
                                          copy_node(Tree[(right, s+p, l-p)])]
                        node_parent = Node(rule=(parent, child),
                                           children=nodes_children,
                                           node_data=node_data)
                        node_parent.add_parent()
                        Tree[(parent, s, l)] = node_parent

    # return only top node:
    # return(P, Tree)

    try:
        # if more then one solution found, remove
        # parent uncentrality:
        Tree[('E', 1, len(goal))].add_parent()
        if return_all:
            result = (P, Tree)
        else:
            result = (P[('E', 1, len(goal))], Tree[('E', 1, len(goal))])
    except KeyError:
        print("cyk fail, founded rules will be returned")
        result = (P, Tree)
    return(result)
            

def preproc(goal_sent_list):
    
    if type(goal_sent_list) != list:
        raise(BaseException("preproc: type of "
                            + "goal_sent_list must be a list"))

    # remove all subsents like "*(", ")*":
    # (cannot use just [o] because str separation is needed
    # (like: "*("|->["*","("]
    #  and ")*"|-> [")", "*"]))
    s = sum([list(o) if type(o) == str else [o] for o in goal_sent_list], [])
    # print(s)
    '''
    for letter in s:
        print("type of %s: %s" % (letter, type(letter)))
    '''
    result = [letter if type(letter) == str
              else letter if letter != "m"
              else letter.lex["term_name"] for letter in s]
    return(result)
