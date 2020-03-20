# parser$ python3 -m env.system.tests_sys

import os
import sys
import inspect

# add import's path:
'''
currentdir = (os.path
              .dirname(os.path
                       .abspath(inspect.getfile(inspect.currentframe()))))
env = currentdir.find("env")
env_dir = currentdir[:env]
# print(env_dir)
if env_dir not in sys.path:
    sys.path.insert(0, env_dir)
'''
from tokentranslator.env.system.sys_main import sysNet as System
from tokentranslator.env.equation_net.equation import Equation as EquationNet
from tokentranslator.env.equation.equation import Equation


def test_sys(EqBilder):
    '''
    s = ts.test_sys()
    s[0].show_cpp()
    or
    out = s[0].make_cpp()
    '''
    eq_1 = "U' = D[U(t-1.1), {x, 2}] + D[U(t-0.9), {y, 1}] + U(t-1.2) + V + V(t-1.1)"
    eq_2 = "U' = D[U(t-1.1), {y, 2}] + D[U(t-0.7), {x, 1}] + U(t-1.2) + V(t-0.3)"
    eq_3 = "U' = D[U(t-1.2), {x, 1}] + D[U(t-0.7), {y, 1}] + U(t-1.3)"

    # create system and parse equations:
    system = System(system=[eq_1, eq_2, eq_3],
                    EqBilder=EqBilder)

    # generate cpp:
    system.cpp.set_default()
    system.cpp.gen_cpp()

    # collect all nodes in one place
    # (system.postproc.nodes):
    system.postproc.collect_nodes()

    # convert delays:
    system.postproc.postproc_delay_nodes()
    return(system)


def test_copy(EqBilder):

    sys_from = test_sys(EqBilder)
    sys_from.cpp.set_diff_type_special(diffType='pure',
                                       diffMethod='borders',
                                       side=2, func="func")
    sys_to = sys_from.copy()
    sys_to.cpp.gen_cpp()

    print("\nsys_from.cpp:")
    sys_from.plotter.show_cpp()

    print("\nsys_to.cpp:")
    sys_to.plotter.show_cpp()

    
def test_sinch_sys(EqBilder):

    eq_1 = "U' = U(t-1.1) + U(t-0.9) + U(t-1.2) + V + V(t-1.1)"
    eq_2 = "U' = U(t-1.1) + U(t-0.7) + U(t-1.2) + V(t-0.3)"
    eq_3 = "U' = U(t-1.2) + U(t-0.5) + U(t-1.3)"
    eq_4 = "U'=a*(D[U,{x,2}]+ D[U,{y,2}])"

    # create system and parse equations:
    sys_1 = System(system=[eq_1, eq_2], EqBilder=EqBilder)
    sys_2 = System(system=[eq_2, eq_3, eq_4], EqBilder=EqBilder)

    # generate cpp:
    sys_1.cpp.set_default()
    sys_1.cpp.gen_cpp()
    sys_2.cpp.set_default()
    sys_2.cpp.gen_cpp()

    # collect all nodes in one place
    # (system.postproc.nodes):
    sys_1.postproc.collect_nodes()
    sys_2.postproc.collect_nodes()

    # sinch systems:
    sys_1.postproc.postproc_delay_sys([sys_2])

    print("sys_1.original")
    sys_1.plotter.show_original()

    print("sys_2.original")
    sys_2.plotter.show_original()

    print("sys_1.cpp")
    sys_1.plotter.show_cpp()

    print("sys_2.cpp")
    sys_2.plotter.show_cpp()

    print('sys_1.global_data:')
    sys_1.postproc.show_nodes_global_data()
    print('sys_2.global_data:')
    sys_2.postproc.show_nodes_global_data()
    return(sys_1)


def run():
    test_sys(Equation)
    test_sinch_sys(EquationNet)
    test_copy(EquationNet)
    # test_sinch_sys(Equation)
    # test_copy(Equation)


if __name__ == '__main__':
    run()
