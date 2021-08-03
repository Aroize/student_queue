import os
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
from .base_db_accessor import BaseDBAccessor, Base


class TestDBAccessor(BaseDBAccessor):
    def __init__(self):
        backend_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent
        self.db_path = pathlib.PurePath(backend_dir, 'tools', 'tests_tmp.db')
        uri = 'sqlite:///{}'.format(self.db_path.as_posix())

        self.engine = create_engine(uri)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)

    def session(self):
        return self.Session()

    def explicit_delete(self):
        logger.debug('removing db')
        os.remove(self.db_path)

    def __del__(self):
        self.explicit_delete()
