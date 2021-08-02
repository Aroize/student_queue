import os
from typing import Optional
from pathlib import Path
from loguru import logger
from ..dao import DBAccessor
from .file import File


class FileRepository:

    def __init__(self, files_path: str):
        self.accessor = DBAccessor
        self.files_path = Path(files_path)

    def create(
        self,
        owner: int,
        rules: str,
        filename: str,
        file_content: bytes
    ) -> Optional[File]:
        with self.accessor().session() as session:
            # todo add size measuring
            file = File(owner=owner, rules=rules, filename=filename, size=0)

            session.add(file)
            session.flush()

            session.commit()


            with open(self.files_path / str(owner), 'wb') as f:
                f.write(file_content)
            return file

    def find_file_by_id(self, file_id: int) -> Optional[File]:
        with self.accessor().session() as session:
            return session.query(File) \
                .filter_by(id=file_id) \
                .first()
