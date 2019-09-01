class Base:
    """
    Base custom ORM class
    """
    sep = ', '

    @classmethod
    def get_field_names(cls):
        return [k for k in cls.__dict__.keys() if k and not k.startswith('__')]

    @classmethod
    def get_field_types(cls):
        return [v[0] for k, v in cls.__dict__.items() if k and v and not k.startswith('__')]

    def get_field_values(self):
        return [v for k, v in self.__dict__.items() if k and not k.startswith('__')]

    @classmethod
    def select_all(cls, conn):
        result = conn.execute(f'SELECT * FROM {cls.__tablename__}')
        return [row for row in result]

    @classmethod
    def select(cls, conn, *args):
        columns_list = args
        result = conn.execute(f'SELECT {cls.sep.join(columns_list)} FROM {cls.__tablename__}')
        return [row for row in result]

    @classmethod
    def create_table(cls, conn):
        field_names = cls.get_field_names()
        field_types = cls.get_field_types()
        table_options = list(zip(field_names, field_types))
        columns = [f'{field} {_type}' for field, _type in table_options if _type != 'fk']
        sql_string = f'CREATE TABLE IF NOT EXISTS {cls.__tablename__} ({cls.sep.join(columns)})'
        if 'fk' in field_types:
            fk_fields = [field for field, _type in table_options if _type == 'fk']
            fk_columns = [f'{field} INT' for field in fk_fields]
            columns += fk_columns
            fk_tables = [v[1] for k, v in cls.__dict__.items() if not k.startswith('__') and v[0] == 'fk']
            fks = list(zip(fk_tables, fk_fields))
            fk_sql_columns = [f'FOREIGN KEY({field}) REFERENCES {table}(_id)' for table, field in fks]
            sql_string = f'CREATE TABLE IF NOT EXISTS {cls.__tablename__} ({cls.sep.join(columns)}, {cls.sep.join(fk_sql_columns)})'
        conn.execute(sql_string)

    @classmethod
    def drop_table(cls, conn):
        conn.execute(f'DROP TABLE IF EXISTS {cls.__tablename__}')

    @classmethod
    def commit(cls, instance, conn):
        field_names = instance.get_field_names()
        field_values = instance.get_field_values()
        table = instance.__class__.__tablename__
        conn.execute(f'INSERT INTO {table} ({instance.sep.join(field_names)}) VALUES {tuple(field_values)}')

    @classmethod
    def update(cls, instance, conn):
        field_names = instance.get_field_names()
        field_values = instance.get_field_values()
        id_val = field_values[field_names.index('_id')]
        expressions = [f'{name} = "{value}"' for name, value in zip(field_names, field_values)]
        table = instance.__class__.__tablename__
        conn.execute(f'UPDATE {table} SET {cls.sep.join(expressions)} WHERE _id = {id_val}')
