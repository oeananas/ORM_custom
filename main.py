from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from orm import Base

from models import User
from models import Post


if __name__ == '__main__':
    # Create engine, connection for database
    engine = create_engine('sqlite:///my.db', echo=False)
    conn = engine.connect()

    # Create tables in database
    User.create_table(conn)
    Post.create_table(conn)

    user_1 = User(_id=1, name='Max')
    user_2 = User(_id=2, name='Alex')
    User.commit(user_1, conn)
    User.commit(user_2, conn)

    user_all_fields = User.select_all(conn)
    print('User.select_all(conn): \n', user_all_fields, '\n')

    user_name_fields = User.select(conn, 'name')
    print('User.select(conn, "name"): \n', user_name_fields, '\n')

    # update row in table 'user'
    user_1.name = 'John'
    User.update(user_1, conn)

    user_name_fields = User.select_all(conn)
    print('User.select_all(conn) after update: \n', user_name_fields, '\n')

    # Drop tables in database
    User.drop_table(conn)
    Post.drop_table(conn)
