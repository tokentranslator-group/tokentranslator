
class Clause():

    def __init__(self, sent, trace=0):

        self.parser = EqParser(self)
        
        # remove spaces:
        self.sent = sent.replace(' ', "")

        self.operator_tree = None

        # for debugging:
        self.trace = trace

    def show_original(self):
        print(self.tree.flatten("original"))
    
    def __repr__(self):
        out = self.sent
        return(out)

    def show_tree_original(self):
        print(self.eq_tree.show_original())
    
