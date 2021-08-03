import smtplib
from pathlib import Path
import random
import unittest
import inject
from backend.api.domain.dao import TestDBAccessor, BaseDBAccessor
from backend.api.domain.user import UserInteractor, UserRepository, UserEmailConfirmationRepository
from backend.api.mail_service import MailSenderService


class CreateTests(unittest.TestCase):
    def _maybe_config_injector(self):
        if inject.is_configured():
            return

        def config(binder: inject.Binder):
            binder.bind_to_constructor(BaseDBAccessor, TestDBAccessor)
            binder.bind_to_constructor(MailSenderService,
                                       lambda: MailSenderService(config_path=Path('tools/smtp_config.json'),
                                                                 template_path=Path('res/email.html')))
            binder.bind_to_constructor(UserEmailConfirmationRepository, UserEmailConfirmationRepository)
            binder.bind_to_constructor(UserRepository, UserRepository)
            binder.bind_to_constructor(UserInteractor, UserInteractor)

        inject.configure(config)

    @staticmethod
    def _random_letter() -> str:
        return chr(random.randint(ord('a'), ord('z')))

    def _random_string(self, length: int = 10) -> str:
        return ''.join([self._random_letter() for _ in range(length)])

    def _random_valid_user(self):
        return dict(login=self._random_string(),
                    password='aAzA12323rfw',
                    email=f'{self._random_string()}@yandex.ru',
                    name=self._random_string(),
                    surname=self._random_string())

    def test_can_create(self):
        self._maybe_config_injector()
        user = self._random_valid_user()
        user = inject.instance(UserInteractor).create(**user)
        self.assertIsNotNone(user.id)
