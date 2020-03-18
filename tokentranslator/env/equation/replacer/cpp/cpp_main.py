from tokentranslator.env.equation.data.terms.output.cpp.replacer_cpp import CppGen
from tokentranslator.env.equation.replacer.cpp.cpp_editor import Editor
from tokentranslator.env.equation.data.terms.output.cpp.postproc import source_result_postproc


class ReplCpp():
    
    '''Convert tree's nodes to cpp'''
    
    def __init__(self, net):
        self.net = net
        self.gen = CppGen()
        self.editor = Editor(net)

    def map_cpp(self):
        return(self.net.tree.map_out(self.gen))
        
    def make_cpp(self):
        self.map_cpp()

        # replace source to result in lhs:
        source_result_postproc(self.gen, self.net.eq_tree)

        self.net.eq_cpp = self.net.tree.flatten('cpp')
        return(self.net.eq_cpp)

    def show_cpp(self):
        print(self.net.tree.flatten('cpp'))

    def show_tree_cpp_out(self):
        print(self.net.eq_tree.show_cpp_out())
        
    def show_tree_cpp_data(self):
        print(self.net.eq_tree.show_cpp_data())
