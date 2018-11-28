import peewee as pw


class BaseDB():

    def __init__(self, path="translator/tokenizer/io/demo_dialect.db"):

        self.db = pw.SqliteDatabase(path)
        
    def create_db(self, tables_gen):
        
        '''Create all tables.

        Input:

        - ``tables_gen`` -- tables generator that is
        function which get's db and return table with
        all tables classes. (see ``model_tables.py``)'''
        
        db = self.db

        tables_dict = tables_gen(db)
        tables = list(tables_dict.values())
        # Dialect = self.create_dialect_table()

        db.connect()
        # tables = [Dialect]
        try:
            db.create_tables(tables)
        except pw.OperationalError:
            db.drop_tables(tables)
            db.create_tables(tables)
        db.close()
        self.tables = tables

    def show_all_entries(self, table_name="dialect"):

        db = self.db
        qs = db.execute_sql("select * from %s" % (table_name,))
        print("\n %s db entries:" % table_name)
        out = []
        for q in qs:
            print(q)
            out.append(q)
        return(out)

    def add_table_entry(self, table, entry: dict):
        
        '''

        Inputs:

        - ``table`` -- peewee table to be edit

        - ``entry`` -- entry dict to be added in db.
        see descrition above.
        
        Examples:

        entry = {"term_name": "let",
                 "template": r"Let(${defs}in:${clauses}",
                 "grammar_type": ('br_left', [True, True, False]),
                 "pattern_type": ('txt',)}
        '''                
        print("FROM add_table_entry:")
        res = table.insert(**entry).execute()

        print("\ninserted:")
        print(res)
        '''
        for query in res:
            print(query)
        '''

    def edit_table_entry(self, table,
                         filter_field_name: str,
                         filter_field_value: str,
                         props):
        
        '''
        Edit properties of entry if entries
        ``filter_field_name`` has ``filter_field_value``.

        Inputs:

        - ``table`` -- peewee table to be edit

        - ``filter_field_name`` -- name of entry's
        field to check for editing.

        - ``filter_field_value`` -- value of field in which case
        according entry will be edit.

        - ``props`` -- must be dict like
        {"template": r"Let(${defs}in:${clauses}",
         "grammar_type": ('br_left', [True, True, False]),}'''

        print("FROM edit_table_entry:")

        # convert all to str:
        for prop_name in props:
            props[prop_name] = str(props[prop_name])

        print("\nprops:")
        print(props)
        res = (table.update(**props)
               .filter(**{filter_field_name: filter_field_value})
               .execute())

        print("\nupdated:")
        print(res)
        '''
        for query in res:
            print(query)
        '''

    def del_table_entry(self, table,
                        filter_field_name: str,
                        filter_field_value: str):
        
        '''
        Delete entry if entries ``filter_field_name``
        has ``filter_field_value``.

        Inputs:

        - ``table`` -- peewee table to be used.

        - ``filter_field_name`` -- name of entry's
        field to check for deleting.

        - ``filter_field_value`` -- value of field in which case
        according entry will be deleted.
        '''
        print("FROM del_table_entry:")

        res = (table.delete()
               .filter(**{filter_field_name: filter_field_value})
               .execute())

        print("\ndeleted:")
        print(res)
        '''
        for query in res:
            print(query)
        '''
