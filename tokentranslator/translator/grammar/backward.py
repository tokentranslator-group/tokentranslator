# python -c "import tokentranslator.translator.grammar.backward as bw; bw.test_gen_sent()"
# python -c "import tokentranslator.translator.grammar.backward as bw; bw.test_gen_states0(10)"

import tokentranslator.translator.grammar.cyk as cyk
from functools import reduce
from collections import OrderedDict
import random
'''
   E -> E+T|T
   T->T*F|F
   F->a
'''

grammar = [('E', 'E+T'), ('E', 'T'),
           ('T', 'T*F'), ('T', 'F'),
           ('F', 'a')]


grammar1 = [('E', 'AE'), ('E', 'BE'),
            ('E', 'e'), ('A', 'a'), ('B', 'b'),
            ('B', 'c')]


def gen_states0(sent):

    def simplify(sent, op):
        '''
        simplify("a*a+a", "*")-> "a+a"
        simplify("a+a", "*")-> "a"
        '''
        # count = 1
        idx = sent.index(op)
        node = sent[idx-1]+sent[idx]+sent[idx+1]
        return(sent.replace(node, "b"))
        # return(str(sent.replace(node, "a", count)))

    def gen(sent, op, states):

        '''simplify all "*" and "+" in sent,
        fill states'''

        while op in sent:
            sent_new = simplify(sent, op)
            states.append([op, (sent, sent_new)])
            sent = sent_new.replace("b", "a")
        return(sent, states)

    sent, states = gen(sent, "*", [])
    sent, states1 = gen(sent, "+", [])
    
    return(states+states1)
   
        
def gen_sent(grammar, size):
    es = get_probabilities(grammar, term=True)
    ts = get_probabilities(grammar, term=False)
    probs = ts
    probs.update(es)

    fgrammar = factorize(grammar)
    
    def gen(v, step, steps):
        if v is None:
            v = 'E'
        step += 1

        if step > steps:
            # go to exist through rules like
            # ("E"->"T", "T"->"F", "F"->"a")
            choicer = list(map(lambda rule: len(rule) == 1, fgrammar[v]))
            choiced_id = choicer.index(True)
        else:
            # choice rule according to probabilities:
            v_probs = [probs[(v, rule)] for rule in fgrammar[v]]
            choicer = list(map(lambda p: random.gauss(p, 0.5) > 0.5, v_probs))

            if True in choicer:
                choiced_id = choicer.index(True)
            else:
                choiced_id = 0

        # use choiced rule:
        rule = fgrammar[v][choiced_id]

        # exit
        if len(rule) == 1:
            if rule.isupper():
                return(gen(rule, step, steps))
            else:
                return([rule])
        else:
            return(gen(rule[0], step, steps)+[rule[1]]
                   + gen(rule[2], step, steps))

    return(gen(None, 0, size))
    # return("".join(gen(None, 0, size)))


def get_probabilities(grammar=grammar1, term=True):

    '''Set t_{v}(y, z) (transition probabilities)
    for all unterminal rules ('v', 'yz')
    to sum to 1 for each v'''
    '''Set e_{v}('a') (emission probabilities)
    for all terminal rules ('v', 'a')
    to sum to 1 for each v'''

    rules = cyk.get_rules(grammar, term=term)

    # FOR factorization:
    def succ(acc, elm):
        if elm[0] in acc:
            acc[elm[0]] += 1.0
        else:
            acc[elm[0]] = 1.0
        return(acc)

    d = reduce(succ, rules, OrderedDict())
    # END FOR

    # all equal probabilities:
    probabilities = dict(map(lambda x: [x] + [1/d[x[0]]], rules))
    return(probabilities)


def factorize(grammar=grammar1):
    # FOR factorization:
    def succ(acc, elm):
        if elm[0] in acc:
            acc[elm[0]].append(elm[1])
        else:
            acc[elm[0]] = [elm[1]]
        return(acc)

    d = reduce(succ, grammar, OrderedDict())
    return(d)
    # END FOR


def test_gen_sent(size=3):
    print("gen_sent(grammar, %d):" % size)
    res = gen_sent(grammar, size)
    print(res)
    return(res)


def test_gen_states0(size=3):
    sent_list = test_gen_sent(size)
    sent = "".join(sent_list)
    print("gen_states0(%s):" % sent)
    res = gen_states0(sent)
    print(res)
    return(res)


if __name__ == "__main__":

    test_gen_sent(3)
    test_gen_states0(3)
