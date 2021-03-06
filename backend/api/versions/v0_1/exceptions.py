from enum import Enum


class JRPCErrorCode(Enum):
    """According to jRPC specification"""
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParameters = -32602
    InternalError = -32603
    ServerError = -32000

    AbsentUserIdentity = 1
    AccessTokenExpired = 2
    EntityAlreadyExists = 3


class InvalidRequestException(Exception):
    pass


class InvalidAccessCredentials(Exception):
    pass


class InvalidParametersException(Exception):
    pass
