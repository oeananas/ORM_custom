class Base:
    """
    Base custom ORM class
    """
    sep = ', '

    def get_field_names(self):
        return [k for k in self.__class__.__dict__.keys() if k and not k.startswith('__')]

    def get_field_types(self):
        return [v[0] for k, v in self.__class__.__dict__.items() if k and v and not k.startswith('__')]

    def select_all(self, conn):
        result = conn.execute(f'SELECT * FROM {self.__class__.__tablename__}')
        return [row for row in result]

    def select(self, conn, columns):
        result = conn.execute(f'SELECT {self.sep.join(columns)} FROM {self.__class__.__tablename__}')
        return [row for row in result]

    def create_table(self, conn):
        field_names = self.get_field_names()
        field_types = self.get_field_types()
        columns = [f'{field} {_type}' for field, _type in zip(field_names, field_types)]
        conn.execute(f'CREATE TABLE IF NOT EXISTS {self.__class__.__tablename__} ({self.sep.join(columns)})')

    def drop_table(self, conn):
        conn.execute(f'DROP TABLE IF EXISTS {self.__class__.__tablename__}')

    def update_table(self, data, conn):
        field_names = [k for k in data.keys()]
        field_values = [v for v in data.values()]
        conn.execute(f'INSERT INTO {self.__class__.__tablename__} ({self.sep.join(field_names)}) VALUES {tuple(field_values)}')
