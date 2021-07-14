import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBAccessor:
    def __init__(self):

        # If you change path of dao file -> fix this relative paths
        backend_dir = pathlib.Path(__file__).resolve().parent.parent.parent
        debug_db = pathlib.PurePath(backend_dir, 'tools', 'debug.db')
        uri = 'sqlite:///{}'.format(debug_db.as_posix())

        self.engine = create_engine(uri)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)

    def session(self):
        return self.Session()
