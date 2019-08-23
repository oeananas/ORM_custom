import sqlalchemy
from models import User


if __name__ == '__main__':
    user = User()

    engine = sqlalchemy.create_engine('sqlite:///my.db', echo=False)
    conn = engine.connect()

    user.create_table(conn)
    print(f'We have a table {engine.table_names()} into db\n')
    data = {
        'id': 99,
        'username': 'myUserName',
    }
    print(f'Creating a new row {data}...\n')
    user.update_table(data, conn)
    print('Output from "select_all" method: ', user.select_all(conn))
    print('Output from "select" method with "[id]" parameter: ', user.select(conn, ['id']))
    another_data = {
        'id': 11,
        'username': 'Username',
    }
    print()
    print(f'Creating an another row {data}...\n')
    user.update_table(another_data, conn)
    print('Output from "select_all" method: ', user.select_all(conn))
    print('Output from "select" method with "[id]" parameter: ', user.select(conn, ['id']))
