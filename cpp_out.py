from code_gens.cpp.deriv import PureDerivGenerator
from code_gens.cpp.deriv import MixDerivGenerator


class Diff():
    def diff(self):
        pass

    def diff_pure(self):
        class Params():
            def __init__(self):
                # int: shift index for variable like
                # like (U,V)-> (source[+0], source[+1])
                self.unknownVarIndex = 0
                self.blockNumber = 0
                self.indepVarList = ['x']
                self.side = 0
                self.derivOrder = 2
                self.diffType = 'pure'
                self.diffMethod = 'vertex'
        params = Params()

        
        '''
        DESCRIPTION:
        self.params should be initiated first.
        '''
        # for debug
        self.print_dbg("FROM get_out_for_termDiff:")
        if self.params.diffType == 'pure':
            # for debug
            self.print_dbg("diffType: pure")

            diffGen = PureDerivGenerator(self.params)
        elif(self.params.diffType == 'mix'):
            # for debug
            self.print_dbg("diffType: mix")

            diffGen = MixDerivGenerator(self.params)

        # diffGen.make_general_data()

        if self.params.diffMethod == 'common':
            # for debug
            self.print_dbg("diffMethod: common")

            out = diffGen.common_diff()
        elif(self.params.diffMethod == 'special'):
            # for debug
            self.print_dbg("diffMethod: special")

            func = self.dataTermMathFuncForDiffSpec
            out = diffGen.special_diff(func)
        elif(self.params.diffMethod == 'interconnect'):
            # for debug
            self.print_dbg("diffMethod: interconnect")

            out = diffGen.interconnect_diff()
        elif(self.params.diffMethod == 'vertex'):
            # for debug
            self.print_dbg("diffMethod: vertex")

            func = self.dataTermMathFuncForDiffSpec
            out = diffGen.special_diff(func)
        else:
            # for debug
            self.print_dbg("diffMethod: None")

            func = self.dataTermMathFuncForDiffSpec
            out = diffGen.diff(func)
        
        return(out)
