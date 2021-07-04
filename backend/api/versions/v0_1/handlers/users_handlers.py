from hashlib import sha256
from versions.v0_1.message import JRPCSuccessResponse, JRPCRequest
from .base_handlers import BaseHandler, SecuredHandler
from versions.v0_1.dao import DBAccessor, Users
from versions.v0_1.exceptions import InvalidParametersException



class RegistrationHandler(BaseHandler):
    """Allows register new users"""
    def method(self) -> str:
        return "users.create"


    def _get_user_by_creds(self, login) -> list:
        """Returns list of users with such a login"""
        dao = DBAccessor()
        existed_user = dao.get_session().query(Users). \
                                            filter(Users.login == login). \
                                            all()
        return existed_user


    def _create_user(self, login: str, password: str) -> None:
        dao = DBAccessor()
        session = dao.get_session()

        psw_hash = sha256(password.encode()).hexdigest()
        new_user = Users(login=login,
                         password_hash=psw_hash,
                         first_name='name1',
                         second_name='name2',
                         third_name='name3',
                         isu_number='228228',
                         registration_timestamp=11111111)

        session.add(new_user)
        session.commit()
        session.close()



    def process(self, payload: JRPCRequest) -> JRPCSuccessResponse:
        # TODO: add error case
        try:
            login = payload.params['login']
            password = payload.params['password']
        except KeyError:
            raise InvalidParametersException

        if len(self._get_user_by_creds(login)) == 0:
            self._create_user(login, password)
            return JRPCSuccessResponse({"status": "ok"}, 0)
        else:
            return JRPCSuccessResponse({"status": "already existed"}, 0)
