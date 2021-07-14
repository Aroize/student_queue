from typing import Dict, Union, Callable, Any, Optional
from .exceptions import InvalidRequestException, InvalidAccessCredentials

# ################################## REQUESTS ###################################


class JRPCRequest:
    """Validates, parses and serializes jRPC request"""
    def __init__(self, jmsg: Dict):
        if not self._is_valid(jmsg):
            raise InvalidRequestException

        self.method = jmsg["method"]
        self.params = jmsg["params"]
        self.id = jmsg["id"]

    def _is_valid(self, jmsg) -> bool:
        """Validates request according to specification"""
        if len(jmsg.keys()) not in (3, 4):
            return False
        if "jsonrpc" not in jmsg.keys() or \
           "method"  not in jmsg.keys() or \
           "params"  not in jmsg.keys() or \
           "id"      not in jmsg.keys():
            return False
        else:
            if jmsg["jsonrpc"] != "2.0":
                return False

            return True

    def obtrain_param(self, param: str) -> Optional[Any]:
        if param in self.params:
            return self.params[param]
        return None

    @staticmethod
    def get_id(jmsg) -> Union[int, None]:
        return None if "id" not in jmsg.keys() else jmsg["id"]

    @property
    def json(self):
        return {"jsonrpc": "2.0",
                "method": self.method,
                "params": self.params,
                "id": self.id}


class SecuredJRPCRequest(JRPCRequest):

    def __init__(
        self,
        headers: dict,
        validator: Callable,
        other: JRPCRequest,
        need_valid_access_token: bool = True
    ):
        self.method = other.method
        self.params = other.params
        self.id = other.id

        credentials = validator.retreive_credentials(headers)

        if need_valid_access_token and not validator.is_access_token_valid(credentials):
            raise InvalidAccessCredentials

        self.credentials = credentials

# ###############################################################################


class BaseJRPCResponse:

    def __init__(self, id: int):
        self.id = id

    def response_field(self) -> str:
        raise NotImplementedError

    def response_value(self) -> Dict:
        raise NotImplementedError

    @property
    def json(self):
        return {
            "jsonrpc": "2.0",
            self.response_field(): self.response_value(),
            "id": self.id
        }


class JRPCSuccessResponse(BaseJRPCResponse):
    def __init__(self, result: Dict, id: int):
        super().__init__(id)
        self.result = result

    def response_field(self) -> str:
        return "result"

    def response_value(self) -> Dict:
        return self.result


class JRPCErrorResponse(BaseJRPCResponse):
    def __init__(self, code: int, message: str, id: int):
        super().__init__(id)
        self.error = {
            "code": code,
            "message": message
        }

    def response_field(self) -> str:
        return "error"

    def response_value(self) -> Dict:
        return self.error


__all__ = ["JRPCRequest", "SecuredJRPCRequest", "JRPCSuccessResponse"]
