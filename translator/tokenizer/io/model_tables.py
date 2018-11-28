import peewee as pw


def create_base_model(db):

    '''Create base table for all tables'''

    class ModelBase(pw.Model):
        class Meta:
            database = db

    return(ModelBase)


def create_dialect_table(db):

    '''Create all environmant tables'''

    ModelBase = create_base_model(db)

    grammar_type_default = "('br_left', [True, False, False])"

    class Dialect(ModelBase):

        # automatic primary key named 'id'
        term_name = pw.CharField()
        template = pw.CharField()

        grammar_type = pw.TextField(default=grammar_type_default)
        pattern_type = pw.TextField(default="('re', 0)")

        created_date = pw.DateTimeField(default=pw.datetime.datetime.now)

    return({"dialect": Dialect})
