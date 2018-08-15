
import logging

# create logger
log_level = logging.DEBUG  # logging.DEBUG
logging.basicConfig(level=log_level)
logger = logging.getLogger('postproc.py')
logger.setLevel(level=log_level)


def source_result_postproc(node):
    
    '''Replace source[delay] or source in eq.lhs to result.
    Ex: source[delay][idx+0]|->result[idx+0]'''
    
    if node.name == '=':
        try:
            out = node[1].output.cpp.out
        except AttributeError:
            logger.debug("source_result_postproc eq has no cpp output")
            return
        if 'source[delay]' in out:
            node[1].output.cpp.out = (node[1].output.cpp.out
                                      .replace('source[delay]', 'result'))
        elif 'source' in out:
            node[1].output.cpp.out = (node[1].output.cpp.out
                                      .replace('source', 'result'))
        

def delay_postproc(node):

    '''Convert delays for all term's that have it.
    node have or have not global_data['delay_data'] value.
    If have, it will be transformed into cpp corect
    order (for ex: [5.1, 1.5, 2.7]->[3, 1, 2])

    First it collect delays (and remember from whom)
    then convert them,
    finely replace them into it's term.cpp.out string.

    var (like U(t-1.1)) used for factorize delays. In
    that case used only var[0] (U).

    Examples:
    for node:
       term.cpp.global_data['delay_data'] = (1, 'V(t-1.1)', '1.1')
       term.cpp.out = source[delay]
    return:
       term.cpp.out_new = source[coverted delay for 1.1]

    Return:
    (in sent U*U(t-3.1)*V(t-3.3)*U(t-1.3)*V(t-1.1) ...)

    {'converted_delay': 2, 'delay_data': (1, 'U(t-3.1)', '3.1')}
    for U(t-3.1) where:
    converted_delay : source[converted_delay][0]
    delay_data[0] - number of delay's term U(t-3.1)
                    in all delays terms.

    {'converted_delay': 2, 'delay_data': (2, 'V(t-3.3)', '3.3')}
    for V(t-3.3) where:
    converted_delay : source[converted_delay][1]
    delay_data[0] - number of delay's term V(t-3.3)
                    in all delays terms.

    {'converted_delay': 1, 'delay_data': (3, 'U(t-1.3)', '1.3')}
    for U(t-1.3) where:
    converted_delay : source[converted_delay][0]
    delay_data[0] - number of delay's term U(t-1.3)
                    in all delays terms.

    Update:
    It now use term instead of term_id for term identification
    in res[var][delay] = [term] and in map_td.
    '''
    out = node

    def convert_delays(delays):

        '''Convert float delay to int,
        according it's value.

        For ex:
        [5.1, 1.5, 2.7]->[3, 1, 2]
        '''
        # delays = copy(delays)
        delays.sort()
        sdelays = [delays.index(val)+1 for val in delays]
        logger.debug(sdelays)
        return(zip(delays, sdelays))

    logger.debug("FROM postproc")

    # FOR factorize terms delays for var:
    # res[val] = [(delay_0, term_id_0), ...]
    res = {}
    for term in out:
        '''
        if type(term) == str:
            continue
        '''
        try:
            delay_data = term.output.cpp.global_data['delay_data']
            term_id, var, delay = delay_data
            # U(t-1.1)->U
            var = var[0]
            if var in res.keys():
                if delay in res[var].keys():
                    res[var][delay].append(term)  # term_id
                else:
                    res[var][delay] = [term]  # term_id
            else:
                res[var] = {delay: [term]}  # term_id
        except KeyError:
            pass
        except AttributeError:
            # if term not have out:
            # (like +):
            continue
    logger.debug("res")
    logger.debug(res)
    # END FOR

    # FOR map float delays to it's source equivalent:
    # map_dsd: var -> delay, sdelay
    map_dsd = lambda var: convert_delays(list(res[var].keys()))

    # map_td: term_id -> source delay
    map_td = dict([(equal_term, sdelay) for var in res.keys()
                   for delay, sdelay in map_dsd(var)
                   for equal_term in res[var][delay]])
    logger.debug("map_td")
    logger.debug(map_td)
    # END FOR

    # FOR find terms for converted delay:
    out_new = []
    for term in out:
        try:
            '''
            if type(term) == str:
                out_new.append(term)
                continue
            '''
            # if delay
            # transform source[delay]->source[1]:
            delay_data = term.output.cpp.global_data['delay_data']
            term_id, var, delay = delay_data
            sdelay = map_td[term]  # term_id
            term.output.cpp.out = (term.output
                                   .cpp.out.replace('delay', str(sdelay)))
            term.output.cpp.global_data['converted_delay'] = sdelay
            out_new.append(term)
        except KeyError:
            try:
                # if no delay
                # transform source[delay]->source[0]
                term.output.cpp.out = (term.output.
                                       cpp.out.replace('delay', str(0)))
                out_new.append(term)
            except:
                pass
        except AttributeError:
            # if term not have out:
            # (like +):
            out_new.append(term)
    # logger.debug([o.out for o in out_new if type(o) != str])
    # return(out)  # out_new

