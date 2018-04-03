'''Convert operator tree to out

Function lex_replacer must be given by user
it transform Word's object to what it shuld be.
If no given, it transform itro original lexems.
This because of type is Word for each node.name in op_tree,
so it contain lex atribute:
   Word.lex = [lexem, re.math object]
function lambda x:x[1] return original sent.

'''

'''
def replace(term, lex_replacer):

    ''Replace term with lex_replacer function.
    If term is not of type Word then return term.''

    if type(term) == str:
        # if term is not in lexem:
        X = term
    else:
        # if term is type(Word)
        X = term.replace_lex(lex_replacer)
    return(X)
'''
from replacer_cpp import CppGen


def flatten_tree(op_tree, node_replacer):
    if len(op_tree.children) == 0:
        # finish:
        X = node_replacer(op_tree)
        return([X])
        
    elif op_tree.name != 'br':
        # main:

        left = flatten_tree(op_tree.children[1], node_replacer)
        X = node_replacer(op_tree)
        right = flatten_tree(op_tree.children[0], node_replacer)

        return(left+[X]+right)

    elif(op_tree.name == 'br'):
        # if brackets:
    
        # work with brackets itself:
        _res = node_replacer(op_tree)
        print("_res")
        print(type(op_tree))
        print(_res)
        leftb, rightb = _res

        # work with brackets args:
        out = []
        out.append(leftb)
        for _id, arg in enumerate(op_tree.children[1].children):
            # if more than one arg
            # (for complex brackets):
            if _id != 0:
                out.append(',')
            X = flatten_tree(arg, node_replacer)
            out.extend(X)
        out.append(rightb)
        return(out)


def flatten(o, lex_replacer):
    
    if type(o) == list:
        # for case goal_sent = a (like s='U'):
        out = lex_replacer(o[0])
    else:
        # for other:
        out = flatten_tree(o, lex_replacer)

    out = lex_replacer.postproc(out)
    # lex_replacer
    return(out)


def map_tree(tree, node_replacer):

    if len(tree.children) == 0:
        # finish:
        node_replacer(tree)
        
    elif tree.name != 'br':
        # main:

        map_tree(tree.children[1], node_replacer)
        node_replacer(tree)
        map_tree(tree.children[0], node_replacer)

    elif(tree.name == 'br'):
        # if brackets:
    
        # work with brackets itself:
        node_replacer(tree)

        # work with brackets args:
        for _id, arg in enumerate(tree.children[1].children):
            map_tree(arg, node_replacer)
    return(tree)
    

def map_tree_postproc(mapped_tree, node_replacer):
    node_replacer.postproc(mapped_tree)
    return(mapped_tree)
