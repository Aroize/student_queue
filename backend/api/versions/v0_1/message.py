from typing import Dict, Union
from .exceptions import InvalidRequestException



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

    @staticmethod
    def get_id(jmsg) -> Union[int, None]:
        return None if "id" not in jmsg.keys() else jmsg["id"]

    @property
    def json(self):
        return {"jsonrpc": "2.0",
                "method": self.method,
                "params": self.params,
                "id": self.id}


class BaseJRPCResponse:
    def __init__(self):
        # TODO
        raise NotImplementedError


class JRPCSuccessResponse:
    def __init__(self, result: Dict, id: Union[int, None]):
        self.result = result
        self.id = id

    @property
    def json(self):
        return {"jsonrpc": "2.0",
                "result": self.result,
                "id": self.id}



class JRPCFailedResponse:
    def __init__(self):
        #TODO
        raise NotImplementedError


__all__ = ["JRPCRequest", "JRPCSuccessResponse", "JRPCFailedResponse"]
