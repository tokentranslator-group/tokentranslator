parser$ python3 -m env.equation.tests
parser$ python3 -m env.equation_net.tests
parser$ python3 -m env.system.tests_sys
python3 -m translator.grammar.tests_cyk
python3 -m translator.tree.tests_map
python3 -m translator.main.test_parser_general

# Test sampling:
parser$ python3 -m translator.sampling.slambda.tree_editor
parser$ python3 -m translator.sampling.slambda.tests_slambda
parser$ python3 -m translator.sampling.slambda.tests_slambda_synch

# Test model:
# parser$ ~/anaconda3/bin/python3 -m gui.web.model.model_main

# Run server:
# parser$ ~/anaconda3/bin/python3 -m gui.web.server.server_main
# lex in "http://localhost:8888/
# net in "http://localhost:8888/net
