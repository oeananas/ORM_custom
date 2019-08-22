import sqlalchemy
from orm import Base


class User(Base):
    __tablename__ = 'user'

    id = ('INT', 'required')
    username = ('CHAR(50)', 'not_required')


if __name__ == '__main__':
    engine = sqlalchemy.create_engine('sqlite:///my.db', echo=True)
    user = User()
    conn = engine.connect()
    user.create_table(conn)
    data = {
        'id': 99,
        'username': 'myUserName',
    }
    user.update_table(data, conn)
    print(user.select_all(conn))
    print(user.select(conn, ['id']))
