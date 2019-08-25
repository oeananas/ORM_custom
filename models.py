from orm import Base


class User(Base):
    """
    Example class for using custom ORM
    """
    __tablename__ = 'user'

    _id = ('INT', 'required')
    name = ('CHAR(50)', 'not_required')

    def __init__(self, _id, name):
        self._id = _id
        self.name = name


class Post(Base):
    """
    Example class for using custom ORM
    """

    __tablename__ = 'post'

    _id = ('INT', 'required')
    title = ('CHAR(50)', 'not_required')
    user_id = ('INT', 'required')

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id
