from typing import Optional
from ..user import UserRepository
from .file import File
from .file_repository import FileRepository


class FileInteractor:

    def __init__(
            self,
            file_repository: FileRepository,
            user_repository: UserRepository
    ):
        self.file_repository = file_repository
        self.user_repository = user_repository

    def create(self, owner: int, rules: str, filename: str, file_content: bytes) -> Optional[File]:

        extension = filename.split(".")[-1]
        if not self._is_allowed_extension(extension):
            raise ValueError(f"File extension \"{extension}\" is not allowed")

        if not self._is_valid_rules(rules):
            raise ValueError("Invalid rules assigned")

        if self._is_empty(file_content):
            raise ValueError("File shouldnt be empty")

        owner = self.user_repository.find_user_by_id(owner)
        if owner is None:
            raise RuntimeError("User with such id doesn't exist")

        file = self.file_repository.create(owner, owner.id, filename, file_content)
        return file

    def get(self, user_id: int, file_id: int) -> Optional[File]:
        file = self.file_repository.find_file_by_id(file_id)
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
        pics = ('png', 'jpg', 'jpeg')
        docs = ('doc', 'docx', 'txt')
        source_code = ('py', 'ipynb', 'java', 'cpp', 'hpp')
        empty = ('', )
        extensions = pics + docs + source_code + empty
        return ext in extensions

    def _is_empty(self, file_content: bytes) -> bool:
        # todo check
        return len(file_content) > 0
