from typing import Dict
from .base_jrpc_response import BaseJRPCResponse


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
