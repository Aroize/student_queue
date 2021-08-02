from typing import Dict, List, Union
from .base_jrpc_response import BaseJRPCResponse


class JRPCSuccessResponse(BaseJRPCResponse):
    def __init__(self, result: Union[Dict, List], id: int):
        super().__init__(id)
        self.result = result

    def response_field(self) -> str:
        return "result"

    def response_value(self) -> Dict:
        return self.result
