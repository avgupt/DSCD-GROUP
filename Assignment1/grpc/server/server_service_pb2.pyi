from protos.Client import Client_pb2 as _Client_pb2
from protos.Article import Article_pb2 as _Article_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetArticlesRequest(_message.Message):
    __slots__ = ["author", "client", "date", "type"]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    author: str
    client: _Client_pb2.Client
    date: _Article_pb2.Date
    type: str
    def __init__(self, client: _Optional[_Union[_Client_pb2.Client, _Mapping]] = ..., type: _Optional[str] = ..., author: _Optional[str] = ..., date: _Optional[_Union[_Article_pb2.Date, _Mapping]] = ...) -> None: ...

class GetArticlesResponse(_message.Message):
    __slots__ = ["article_list"]
    ARTICLE_LIST_FIELD_NUMBER: _ClassVar[int]
    article_list: _containers.RepeatedCompositeFieldContainer[_Article_pb2.Article]
    def __init__(self, article_list: _Optional[_Iterable[_Union[_Article_pb2.Article, _Mapping]]] = ...) -> None: ...

class PublishArticleRequest(_message.Message):
    __slots__ = ["article", "client"]
    ARTICLE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    article: _Article_pb2.Article
    client: _Client_pb2.Client
    def __init__(self, client: _Optional[_Union[_Client_pb2.Client, _Mapping]] = ..., article: _Optional[_Union[_Article_pb2.Article, _Mapping]] = ...) -> None: ...

class PublishArticleResponse(_message.Message):
    __slots__ = ["status"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    FAILED: PublishArticleResponse.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS: PublishArticleResponse.Status
    status: PublishArticleResponse.Status
    def __init__(self, status: _Optional[_Union[PublishArticleResponse.Status, str]] = ...) -> None: ...
