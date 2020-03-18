from tokentranslator.env.equation_net.data.terms.output.cpp.replacer_cpp import CppGen
from tokentranslator.env.equation_net.replacer.cpp.cpp_editor import Editor
from tokentranslator.env.equation.data.terms.output.cpp.postproc import source_result_postproc


class ReplCpp():
    
    '''Convert tree's nodes to cpp'''
    
    def __init__(self, net):
        self.net = net
        self.gen = CppGen()
        self.editor = Editor(net)

    def map_cpp(self):
        self.net.net_editor.map_out(self.gen)
        
    def make_cpp(self):

        self.gen.set_parsed_net(self.net.net_out)
        self.gen.set_mid_replacers(self.net.parser.mid_replacers)

        self.map_cpp()

        # replace source to result in lhs:
        source_result_postproc(self.gen, str(['s']),
                               eq_terms_names=["eq", "uneq"])

        out = self.net.net_editor.flatten("cpp", self.gen)
        self.net.eq_cpp = "".join(out)
        return(self.net.eq_cpp)

    def show_cpp(self):
        out = self.net.net_editor.flatten("cpp", self.gen)
        print("".join(out))
    
    def get_cpp(self):
        out = self.net.net_editor.flatten("cpp", self.gen)
        return("".join(out))
    
    def show_tree_cpp_out(self):
        print(self.net.eq_tree.show_cpp_out())
        
    def show_tree_cpp_data(self):
        print(self.net.eq_tree.show_cpp_data())
