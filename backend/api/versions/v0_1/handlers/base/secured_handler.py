from .base_handler import BaseHandler


class SecuredHandler(BaseHandler):

    def is_secured(self) -> bool:
        return True

    def need_access_token(self) -> bool:
        return True
