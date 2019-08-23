from orm import Base


class User(Base):
    """
    Example class for using custom ORM
    """
    __tablename__ = 'user'

    id = ('INT', 'required')
    username = ('CHAR(50)', 'not_required')
