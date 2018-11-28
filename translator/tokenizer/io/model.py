# parser$ ~/anaconda3/bin/python3 -m translator.tokenizer.io.model

# import peewee as pw
from datetime import date

from translator.tokenizer.io.model_base import BaseDB
from translator.tokenizer.io.model_tables import create_dialect_table


class TokenizerDB(BaseDB):

    '''
    db consist from one dialect table,
    composed from the entries.

    each entry must be:
    (term_name, template, grammar_type, pattern_type)
    where
       template
          either re or txt or ex template.

       grammar_type type is list like one of thats:

          ('br_left', [True, False, False])
          ('br_right', [True, False, False])
          ('br_mid', [False, True, False])
          ('a',)

       pattern_type is list like one of thats:

          ('re', [+ order])
          ('txt', [+ order])
          ('ex',)

          where order is optional pattern order.

    Examples:

        ('let', r"Let(${defs}in:${clauses}",
        ('br_left', [True, True, False]),
        ('txt',)

        ('func', r"${{pred}}\(${args}",
        ('br_left', [True, False, False]),
        ('re', 6.1))

        # x, xs, normal_form_0
        ('var', r"(?P<obj>[a-z|_|0-9]+)", ('a'),
        ('re', 2)),

        ('eq', "Eq(${eqs})Eq",
        ('a',), ('ex',)),
    '''
    def __init__(self, path="translator/tokenizer/io/demo_dialect.db"):
        
        BaseDB.__init__(self, path)

    def create_dialect_db(self):
        BaseDB.create_db(self, create_dialect_table)

    def show_all_entries(self):

        out = BaseDB.show_all_entries(self, table_name="dialect")
        return(out)

    def fill_dialect_db(self):
        
        db = self.db
        table = self.tables[0]

        db.connect()

        # create entry:
        table.create(term_name="let",
                     template=r"Let(${defs}in:${clauses}",
                     grammar_type="('br_left', [True, True, False])",
                     pattern_type="('txt',)")
        # expirydate=date(2100, 1, 1)

        db.close()
        
    def add_pattern(self, entry):
        
        '''
        - ``entry`` -- entry dict to be added in db.
        see descrition above.
        (see BaseDB.add_table_entry)

        Examples:

        entry = {"term_name": "let",
                 "template": r"Let(${defs}in:${clauses}",
                 "grammar_type": ('br_left', [True, True, False]),
                 "pattern_type": ('txt',)}
        '''
                      
        table = self.tables[0]
        self.add_table_entry(table, entry)

    def edit_pattern(self, term_name, props):
        '''
        Edit  properties of pattern's with term_name.
        (see BaseDB.edit_table_entry)
        '''
        table = self.tables[0]
        self.edit_table_entry(table, 'term_name', term_name,
                              props)
        
    def del_pattern(self, term_name):
        '''
        Delete pattern with term_name.
        (see ``BaseDB.del_table_entry``)
        '''
        table = self.tables[0]
        self.del_table_entry(table, 'term_name', term_name)


if __name__ == '__main__':
    
    agent = TokenizerDB()
    agent.create_dialect_db()
    agent.fill_dialect_db()

    agent.add_pattern({"term_name": "func",
                       "template": r"${{pred}}\(${args}",
                       "grammar_type": ('br_left', [True, False, False]),
                       "pattern_type": ('re', 6.1)})
                      
    # sin, abelian, a:
    agent.add_pattern({"term_name": "pred",
                       "template": r"(?P<obj>\w+)",
                       "grammar_type": ('part',),
                       "pattern_type": ('re',)})

    agent.edit_pattern("pred", {"grammar_type": ('a',)})

    agent.del_pattern("pred")
    
    agent.show_all_entries()
