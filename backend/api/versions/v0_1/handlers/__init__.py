from .auth import RegistrationHandler, AuthHandler, RefreshCredentialsHandler
from .base import BaseHandler, SecuredHandler
from .debug import EchoHandler, SecuredEchoHandler, FakeEmailVerificationHandler
from .group import CreateGroupHandler
from .course import CreateCourseHandler, RemoveCourseHandler, FindCourseByTeacherHandler
from .course.lab import CreateLabHandler, FindLabsByCourseHandler
from .rest import EmailVerificationHandler, FilesHandler
