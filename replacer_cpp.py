

class CppGen():
    def __init__(self, term):
        pattern = term.lex[-1]
        if pattern == 'diff_pattern':
            pass
        elif pattern == 'bdp':
            pass
        elif pattern == 'val_pattern':
            pass
        elif pattern == 'coefs_pattern':
            pass
        elif pattern == 'pow_pattern':
            pass
        elif pattern == 'func_pattern':
            pass
        elif pattern == 'float_pattern':
            pass
        

def cpp(term):
    # gen = CppGen(term)
    return(term.lex[-1])


class CppOutsForTerms():
    '''
    DESCRIPTION:
    If pattern (termDemo) should contain
    cpp out
    then
    there should exist function
    (get_out_for_termDemo)
    and 
    if this function use some
    parameters, they must exist
    and initiated in params before.
    (all that happened in Parser.py)
    '''
    # use varIndexs for all
    # CppOutsForTerms objects
    dataTermVarsSimpleGlobal = {'varIndexs': []}

    def __init__(self, params):
        self.params = params
        
        self.dataTermVarsPoint = []
        self.dataTermVarsPointDelay = []
        self.dataTermVarSimpleLocal = {'delays': [],
                                       'varIndexs': []}
        self.dataTermVarsSimpleIndep = {'delays': [],
                                        'varIndexs': []}

        #!!!self.diffGen = PureDerivGenerator(params)
        self.dataTermOrder = {'indepVar': [],
                              'order': []}
        
        self.dataTermVarsForDelay = {}
        
        self.dataTermMathFuncForDiffSpec = "empty_func"

        self.dataTermRealForPower = {'real': []}

        # for debugging:
        self.dbg = True
        self.dbgInx = 4

    def get_out_for_term(self, termName):
        '''
        DESCRIPTION:
        Find out for term (termDemo) with termName
        (from Patterns.py). For that method with name
        get_out_for_termDemo must exists.

        INPUT:
        termName - name of term like termVarsPoint1D

        Return:
        function replacer \f args: method(self, args)

        Tests:
        >>> f = cpp.get_out_for_term('diff');
        >>> f()
        '''
        methods = self.__class__.__dict__
        for methodName in methods.keys():
            methodTermName = methodName.split('_')[-1]
            if methodTermName == termName:
                return(lambda *args: methods[methodName](self, *args))

    def get_out_for_termPower(self):
        return("pow(arg_val, arg_power)")

    def get_out_for_termArgsForUnary(self):
        '''
        DESCRIPTION:
        If Arg should by X:
        return idxX
        '''
        return('idxArg')


    def get_out_for_termVarsPoint(self):
        '''
        DESCRIPTION:
        For patterns like
        U(t,{x,0.7})
        U(t,{x,0.7}{y,0.3})
        '''
        if self.params.dim == '1D':
            return(self.get_out_for_termVarsPoint1D())
        elif self.params.dim == '2D':
            return(self.get_out_for_termVarsPoint2D())

    def get_out_for_termVarsPoint1D(self):
        '''
        DESCRIPTION:
        For patterns like U(t,{x,0.7})
        '''
        blockNumber = self.params.blockNumber
        return('source[0][arg1'+'*'
               + 'Block'+str(blockNumber)+'CELLSIZE]')
        
    def get_out_for_termVarsPoint2D(self):
        '''
        DESCRIPTION:
        For U(t,{x,0.7}{y,0.3})
        '''
        blockNumber = self.params.blockNumber
        return(('source[0][(arg1'
                + '+'
                + 'arg2'+'*Block'
                + str(blockNumber)
                + 'StrideY)*'
                + 'Block'+str(blockNumber)+'CELLSIZE]'))

    def get_out_for_termVarsPointDelay(self):
        '''
        DESCRIPTION:
        For patterns like U(t-1.3,{x,0.7}{y,0.3})
        '''
        if self.params.dim == '1D':
            return(self.get_out_for_termVarsPoint1DDelay())
        elif self.params.dim == '2D':
            return(self.get_out_for_termVarsPoint2DDelay())

    def get_out_for_termVarsPoint1DDelay(self):
        blockNumber = self.params.blockNumber
        return('source[arg_T_var][arg_X_var'+'*'
               + 'Block'+str(blockNumber)+'CELLSIZE'
               + '+'+'arg_varIndex'+']')
        
    def get_out_for_termVarsPoint2DDelay(self):
        blockNumber = self.params.blockNumber
        return(('source[arg_T_var][(arg_X_var'
                + '+'
                + 'arg_Y_var'+'*Block'
                + str(blockNumber)
                + 'StrideY)*'
                + 'Block'+str(blockNumber)+'CELLSIZE'
                + '+'+'arg_varIndex' + ']'))

    def get_out_for_termVarsDelay(self):
        return('source['
               + 'arg_delay'  # delay
               + '][idx + '
               + 'arg_varIndex'  # str(varIndex)
               + ']')

    def get_out_for_termVarsSimpleIndep(self):
        '''
        DESCRIPTION:
        varIndex usage:
        source[][idx+0] - x
        source[][idx+1] - y
        source[][idx+2] - z
        
        '''
        return('source['
               + '0'  # delay
               + '][idx + '
               + 'arg_varIndex'  # str(varIndex)
               + ']')

    def get_out_for_termParam(self):
        return('params['
               + 'arg_param'  # str(parIndex)
               + ']')

    def get_out_for_termBinary(self):
        return(' '
               + 'arg1'  # expressionList
               + ' ')

    def get_out_for_termFunc(self):
        return('arg1')  # expressionList

    def print_dbg(self, *args):
        if self.dbg:
            for arg in args:
                print(self.dbgInx*' '+str(arg))
            print('')

