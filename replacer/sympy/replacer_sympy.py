from replacer.replacer import Gen


import logging

# create logger
log_level = logging.DEBUG  # logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger('replacer_cpp.py')
logger.setLevel(level=log_level)


class Out():
    pass


class SympyGen(Gen):
    def __init__(self):
        pass

    def postproc(self, node):
        pass

    def translate_brackets(self, left_term, right_term):
        pattern = left_term.name.lex[-1]
        if pattern == 'func_pattern':
            
            func = left_term.name.lex[0]
            logger.debug("func_pattern:")
            logger.debug(func)

            # transform to sympy:
            left_term.sympy = "sympy.%s" % (func)

        return((left_term, right_term))

    def add_out_to(self, term):

        '''Add pattern out to term and return it'''

        term = self.print_cpp(term)
        return(term)

    def print_cpp(self, term):
        '''
        term.lex = ['D[U,{x,2}]', <_sre.SRE_Match object>, 'diff_pattern']
        add out to term
        transform term to sympy.
        extract data from pattern (if any exist for such pattern)
        and add it to term.
        
        '''
        pattern = term.name.lex[-1]
        logger.debug("pattern")
        logger.debug(pattern)
        if pattern == 'diff_pattern':

            reg_pattern = term.name.lex[1]
            
            # diff var (U):
            var = reg_pattern.group('val')
            
            # find diff orders (free_var: x, order: 1):
            for free_var in 'xyz':
                order = reg_pattern.group('val_'+free_var)
                if order is not None:
                    break
                    
            # add args x, y to var:
            var = self._add_args(var)
            
            # transform to sympy:
            term.sympy = "sympy.diff(%s, %s, %s)" % (var, free_var, order)

        elif pattern == 'diff_time_var_pattern':
            
            reg_pattern = term.name.lex[1]
            
            # diff var (U):
            var = reg_pattern.group('val')

            # add args x, y to var:
            var = self._add_args(var)
            
            # transform to sympy:
            term.sympy = "sympy.diff(%s, t)" % (var)

        elif pattern == 'var_pattern':
            
            reg_pattern = term.name.lex[1]
            
            # diff var (U):
            var = reg_pattern.group('val')

            # add args x, y to var:
            var = self._add_args(var)
            
            # transform to sympy:
            term.sympy = var

        return(term)

    def _add_args(self, var):
        
        '''Add x, y to var'''

        # FOR add args to var:
        if self.dim == 1:
            x = ', x)'
        elif self.dim == 2:
            x = ', x, y)'

        # U(t-1)
        if '(' in var:
            var = var[:-1] + x
        else:
            var = var + '(' + 't'+x
        # END FOR
        
        return(var)
        
    def set_dim(self, **kwargs):
        self.dim = kwargs['dim']
