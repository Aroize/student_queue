import os
from typing import Optional
from pathlib import Path
import inject
from ..dao import BaseDBAccessor
from .file import File


class FileRepository:

    @inject.params(accessor=BaseDBAccessor)
    def __init__(self, files_path: str, accessor: BaseDBAccessor = None):
        self.accessor = accessor
        self.files_path = Path(files_path)

    def create(
        self,
        owner: int,
        rules: str,
        filename: str,
        file_content: bytes
    ) -> Optional[File]:
        with self.accessor.session() as session:
            # todo add size measuring
            file = File(owner=owner, rules=rules, filename=filename, size=len(file_content))
            session.add(file)
            session.flush()
            session.commit()

            with open(self.files_path / str(file.id), 'wb') as f:
                f.write(file_content)
                print('content written')
            return file

    def find_file_by_id(self, file_id: int) -> Optional[File]:
        with self.accessor.session() as session:
            return session.query(File) \
                .filter_by(id=file_id) \
                .first()
