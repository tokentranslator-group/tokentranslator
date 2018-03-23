from words import Word
from replacer_cpp import cpp


# this function work with lexems in postprocessing:
# in that case it just return lexem original value
# because Word.lex = [lexem, re.math object]
def lex_replacer(term):

    '''Replace term.

    Return:
       term if type(term) == str (like '+')
       cpp(term) if type(term) == Word (like 'D[U,{x,3}]')
       [cpp(tm) for tm in term] if type(term) == list.
                                   (like ['(', 'w']
                                    or ['f',')']'''

    if type(term) == str:
        # if term is not in lexem:
        X = term
    elif(type(term) == Word):
        # if term is type(Word)
        # it can be branch too
        # (in case of one argument
        # like (a)^3 or sin(a)):
        X = cpp(term)
    elif(type(term) == list):
        # for branches (a+...)^3 or sin(a+...):
        X = []
        for tm in term:
            if type(tm) == Word:
                # for )^n and sin(:
                X.append(cpp(tm))
            else:
                # for ():
                X.append(tm)
    return(X)
