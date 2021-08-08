from typing import Optional

import inject

from ..user import UserRepository
from .file import File
from .file_repository import FileRepository


class FileInteractor:
    def __init__(self):
        self.pic_extentions = ('png', 'jpg', 'jpeg')

    @inject.params(file_repository=FileRepository,
                   user_repository=UserRepository)
    def create(self,
               owner: int,
               rules: str,
               filename: str,
               file_content: bytes,
               file_repository: FileRepository = None,
               user_repository: UserRepository = None) -> Optional[File]:

        extension = filename.split(".")[-1]
        if not self._is_allowed_extension(extension):
            raise ValueError(f"File extension \"{extension}\" is not allowed")

        if not self._is_valid_rules(rules):
            raise ValueError("Invalid rules assigned")

        if self._is_empty(file_content):
            raise ValueError("File shouldnt be empty")

        owner = user_repository.find_user_by_id(owner)
        if owner is None:
            raise RuntimeError("User with such id doesn't exist")

        file = file_repository.create(owner.id, rules, filename, file_content)
        return file

    def is_picture_extention(self, ext: str) -> bool:
        return ext in self.pic_extentions

    @inject.params(file_repository=FileRepository)
    def get(self, user_id: int, file_id: int, file_repository: FileRepository = None) -> Optional[File]:
        file = file_repository.get(file_id)
        if file is None:
            return None
        if file.owner == user_id:
            return file
        elif file.rules[1] == '1':
            return file

    def _is_valid_rules(self, rules: str) -> bool:
        # rule is: read for owner, other
        if len(rules) != len('11'):
            # да, я знаю, что можно числом. Сейчас трактуемость важнее
            return False

        if any(map(lambda c: c not in ('1', '0'), rules)):
            return False

        if rules[0] != '1':
            # read is required for owner
            return False

        return True

    def _is_allowed_extension(self, ext: str) -> bool:

        docs = ('doc', 'docx', 'txt')
        source_code = ('py', 'ipynb', 'java', 'cpp', 'hpp')
        empty = ('', )
        extensions = self.pic_extentions + docs + source_code + empty
        return ext in extensions

    def _is_empty(self, file_content: bytes) -> bool:
        # todo check
        return len(file_content) == 0
