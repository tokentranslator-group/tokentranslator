'''Contain tree for cyk algorithm.
NodeR contain some addition functions
for parse to operator tree convetion (convert func in tree.py)'''
from functools import reduce


class Node():
    def __init__(self, rule, parent=None, children=[],
                 visited=False):
        self.rule = rule
        self.parent = parent
        # self.left = left
        # self.right = right
        self.children = children
        self.visited = visited

    def add_parent(self):

        '''Add self to each child as parent'''

        for child in self.children:
            child.parent = self
            child.add_parent()

    def __repr__(self, begin=0):
        return(self.print_node(begin=begin))

    def print_node(self, begin=0, out_gen=None):

        '''Show node and all it's children.
        If out_gen is not None it should be like:
        out_gen = lambda _self: _self.name'''

        start = reduce(lambda x, acc: x+acc, [' ' for i in range(begin)], "")
        begin += 3
        if out_gen is None:
            out = str(self.rule)
        else:
            out = str(out_gen(self))

        for id, child in enumerate(self.children):
            if child is not None:
                out += ('\n' + start + "child %s: " % (id)
                        + str(child.print_node(begin, out_gen)))
        return(out)


class NodeR(Node):
    ''' Node for transformation to operator's tree.

    :atr name is either like 'a' or '+' or 'AB'.
    '''
    def __init__(self, rule, parent=None, children=[],
                 visited=False):
        Node.__init__(self, rule, parent, children, visited)

        self.trs = ['a']
        self.ops = ['+', '-', '*']
        self.brs = ['(', ')', 'w', 'f']
        self.sps = [',']
        self.ars = ['arg', 'args']

        self.name = self.rule[1]

    def __iter__(self):
        yield(self)
        for _id, child in enumerate(self.children):
            if child is not None:
                for node in child:
                    yield(node)

    def __repr__(self, begin=0):
        return(self.print_node(begin=begin,
                               out_gen=lambda _self: _self.name))

    def show_original(self):
        def gen(_self):
            try:
                out = _self.name.lex[0]
            except:
                out = _self.name
            return(out)
        return(self.print_node(begin=0,
                               out_gen=gen))
            
    def show_cpp_out(self):
        def gen(_self):
            try:
                out = _self.cpp.out
            except:
                out = _self.name
            return(out)

        return(self.print_node(begin=0,
                               out_gen=gen))

    def show_cpp_data(self):
        def gen(_self):
            try:
                out = _self.cpp.global_data
            except:
                out = None
            return(out)

        return(self.print_node(begin=0,
                               out_gen=gen))

    def py_bug_fix(self):

        '''For strange python bug'''

        self.children = [child for child in self.children]

    def remove_child(self, child):
        child.parent = None
        # remove old_child from self
        node_id = self.find_child(child)
        self.children.pop(node_id)

    def replace_child(self, old_child, new_child):
        # remove old_child from self
        node_id = self.find_child(old_child)
        self.children.pop(node_id)

        # add new_child to self as new child
        new_child.parent = self
        self.py_bug_fix()
        self.children.insert(node_id, new_child)

    def add_child(self, new_child):

        # add new_child to parent as child
        new_child.parent = self
        # import pdb; pdb.set_trace()
        self.py_bug_fix()
        self.children.append(new_child)

    def insert_child(self, new_child, _id=0):
        # add new_child to parent as child
        new_child.parent = self
        # import pdb; pdb.set_trace()
        self.py_bug_fix()
        self.children.insert(_id, new_child)
        
    def get_unvisited(self):
        unvisited = [child for child in self.children
                     if not child.visited]
        return(unvisited)

    def find_child(self, node):
        
        '''Find node_id in self.children'''
        
        for id, child in enumerate(self.children):
            if child.name == node.name:
                return(id)

    def get_children(self, node_type_list):

        '''Find all children with name from node_type_list'''

        children = [child for id, child in enumerate(self.children)
                    if child.name in node_type_list]
        return(children)

    def get_operators(self):

        ''' Find children with node op'''

        return(self.get_children(self.ops))

    def get_brackets(self):

        ''' Find children with node brackets'''

        return(self.get_children(self.brs))

    def get_separators(self):

        ''' Find children with node ","'''

        return(self.get_children(self.sps))

    def get_args(self):

        '''Find children with name args '''

        return(self.get_children(self.ars))

    def find_one(self, condition):

        '''Find first children with name in satisfy condition'''

        for id, child in enumerate(self.children):
            if condition(child.name):
                return(child)

    def find_op_child(self):
        
        ''' Find first operator child'''

        return(self.find_one(lambda name: name in self.ops))

    def find_unop_child(self):
        
        ''' Find first unoperator child'''

        return(self.find_one(lambda name: name not in self.ops))

    def find_br_child(self):
        
        ''' Find first brach child'''

        return(self.find_one(lambda name: name in self.brs))

    def find_unbr_child(self):
        
        ''' Find first unbranch child'''

        return(self.find_one(lambda name: name not in self.brs))

    def find_sp_child(self):
        
        ''' Find first brach child'''

        return(self.find_one(lambda name: name in self.sps))

    def find_unsp_child(self):
        
        ''' Find first unbranch child'''

        return(self.find_one(lambda name: name not in self.sps))

    def find_arg_child(self):
        
        ''' Find first brach child'''

        return(self.find_one(lambda name: name in self.ars))

    def find_unarg_child(self):
        
        ''' Find first unbranch child'''

        return(self.find_one(lambda name: name not in self.ars))

    def find_term_child(self):
        
        ''' Find first brach child'''
        return(self.find_one(lambda name: name in self.trs))


def copy_node(node: NodeR)->NodeR:
    new_node = NodeR(rule=node.rule,
                     parent=node.parent,
                     children=node.children,
                     visited=node.visited)
    return(new_node)
