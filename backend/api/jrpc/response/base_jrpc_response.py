from typing import Dict


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
