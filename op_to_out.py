'''Convert operator tree to out

Function lex_replacer must be given by user
it transform Word's object to what it shuld be.
If no given, it transform itro original lexems.
This because of type is Word for each node.name in op_tree,
so it contain lex atribute:
   Word.lex = [lexem, re.math object]
function lambda x:x[1] return original sent.

'''


def replace_branches(left, right, lex_replacer):
    left, right = lex_replacer(['branches', left, right])
    return((left, right))


def replace(term, lex_replacer):

    '''Replace term with lex_replacer function.
    If term is not of type Word then return term.'''

    if type(term) == str:
        # if term is not in lexem:
        X = term
    else:
        # if term is type(Word)
        X = term.replace_lex(lex_replacer)
    return(X)


def convert_tree(op_tree, lex_replacer=lambda x: x[0]):
    if len(op_tree.children) == 0:
        # finish:

        X = replace(op_tree.name, lex_replacer)

        return(X)

    elif len(op_tree.children) == 2:
        # main:

        left = convert_tree(op_tree.children[1])
        X = replace(op_tree.name, lex_replacer)
        right = convert_tree(op_tree.children[0])

        return(left+X+right)

    elif(len(op_tree.children) == 4):
        # if branches:

        leftb = replace(op_tree.children[-1].name, lex_replacer)
        left = convert_tree(op_tree.children[1])
        X = replace(op_tree.name, lex_replacer)
        right = convert_tree(op_tree.children[0])
        rightb = replace(op_tree.children[-2].name, lex_replacer)

        return(leftb+left+X+right+rightb)


def convert(o, lex_replacer=lambda x: x[0]):
    if type(o) == list:
        return(replace(o[0], lex_replacer))
    else:
        return(convert_tree(o, lex_replacer))
