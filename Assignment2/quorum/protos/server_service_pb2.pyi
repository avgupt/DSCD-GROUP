import status_pb2 as _status_pb2
import time_stamp_pb2 as _time_stamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ["content", "file_name", "status", "version"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    content: str
    file_name: str
    status: _status_pb2.Status
    version: _time_stamp_pb2.TimeStamp
    def __init__(self, file_name: _Optional[str] = ..., content: _Optional[str] = ..., version: _Optional[_Union[_time_stamp_pb2.TimeStamp, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ["file_content", "file_name", "uuid"]
    FILE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    file_content: str
    file_name: str
    uuid: str
    def __init__(self, file_name: _Optional[str] = ..., file_content: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ["status", "uuid", "version"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    status: _status_pb2.Status
    uuid: str
    version: _time_stamp_pb2.TimeStamp
    def __init__(self, uuid: _Optional[str] = ..., version: _Optional[_Union[_time_stamp_pb2.TimeStamp, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...
