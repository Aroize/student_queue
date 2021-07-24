from typing import Dict, Union, Callable, Any, Optional, Type
from ..exceptions import InvalidRequestException, InvalidAccessCredentials

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

    def _obtain_typed_param(self, param: str, param_type: Type) -> Optional[Any]:
        if param in self.params and isinstance(self.params[param], param_type):
            return self.params[param]
        return None

    def obtrain_str(self, param: str) -> Optional[str]:
        return self._obtain_typed_param(param, str)

    def obtain_int(self, param: str) -> Optional[int]:
        return self._obtain_typed_param(param, int)

    def obtain_float(self, param: str) -> Optional[float]:
        return self._obtain_typed_param(param, float)

    def obtain_bool(self, param: str) -> Optional[bool]:
        return self._obtain_typed_param(param, bool)

    @staticmethod
    def get_id(jmsg) -> Union[int, None]:
        return None if "id" not in jmsg.keys() else jmsg["id"]

    @property
    def json(self):
        return {"jsonrpc": "2.0",
                "method": self.method,
                "params": self.params,
                "id": self.id}
