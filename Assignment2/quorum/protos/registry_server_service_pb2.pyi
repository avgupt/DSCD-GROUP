import server_pb2 as _server_pb2
import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ["type"]
    class REQUEST_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DELETE: Request.REQUEST_TYPE
    GET: Request.REQUEST_TYPE
    READ: Request.REQUEST_TYPE
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WRITE: Request.REQUEST_TYPE
    type: Request.REQUEST_TYPE
    def __init__(self, type: _Optional[_Union[Request.REQUEST_TYPE, str]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["server_list"]
    SERVER_LIST_FIELD_NUMBER: _ClassVar[int]
    server_list: _containers.RepeatedCompositeFieldContainer[_server_pb2.Server]
    def __init__(self, server_list: _Optional[_Iterable[_Union[_server_pb2.Server, _Mapping]]] = ...) -> None: ...
