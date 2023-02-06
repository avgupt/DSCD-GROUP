# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc/server/server_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.Client import Client_pb2 as protos_dot_Client_dot_Client__pb2
from protos.Article import Article_pb2 as protos_dot_Article_dot_Article__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grpc/server/server_service.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n grpc/server/server_service.proto\x1a\x1aprotos/Client/Client.proto\x1a\x1cprotos/Article/Article.proto\"`\n\x12GetArticlesRequest\x12\x17\n\x06\x63lient\x18\x01 \x01(\x0b\x32\x07.Client\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\x12\x13\n\x04\x64\x61te\x18\x04 \x01(\x0b\x32\x05.Date\"5\n\x13GetArticlesResponse\x12\x1e\n\x0c\x61rticle_list\x18\x01 \x03(\x0b\x32\x08.Article\"K\n\x15PublishArticleRequest\x12\x17\n\x06\x63lient\x18\x01 \x01(\x0b\x32\x07.Client\x12\x19\n\x07\x61rticle\x18\x02 \x01(\x0b\x32\x08.Article\"k\n\x16PublishArticleResponse\x12.\n\x06status\x18\x01 \x01(\x0e\x32\x1e.PublishArticleResponse.Status\"!\n\x06Status\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x32\x8c\x01\n\rServerService\x12\x38\n\x0bGetArticles\x12\x13.GetArticlesRequest\x1a\x14.GetArticlesResponse\x12\x41\n\x0ePublishArticle\x12\x16.PublishArticleRequest\x1a\x17.PublishArticleResponseb\x06proto3'
  ,
  dependencies=[protos_dot_Client_dot_Client__pb2.DESCRIPTOR,protos_dot_Article_dot_Article__pb2.DESCRIPTOR,])



_PUBLISHARTICLERESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='PublishArticleResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=398,
  serialized_end=431,
)
_sym_db.RegisterEnumDescriptor(_PUBLISHARTICLERESPONSE_STATUS)


_GETARTICLESREQUEST = _descriptor.Descriptor(
  name='GetArticlesRequest',
  full_name='GetArticlesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='client', full_name='GetArticlesRequest.client', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='GetArticlesRequest.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author', full_name='GetArticlesRequest.author', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date', full_name='GetArticlesRequest.date', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=190,
)


_GETARTICLESRESPONSE = _descriptor.Descriptor(
  name='GetArticlesResponse',
  full_name='GetArticlesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='article_list', full_name='GetArticlesResponse.article_list', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=192,
  serialized_end=245,
)


_PUBLISHARTICLEREQUEST = _descriptor.Descriptor(
  name='PublishArticleRequest',
  full_name='PublishArticleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='client', full_name='PublishArticleRequest.client', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='article', full_name='PublishArticleRequest.article', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=247,
  serialized_end=322,
)


_PUBLISHARTICLERESPONSE = _descriptor.Descriptor(
  name='PublishArticleResponse',
  full_name='PublishArticleResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='PublishArticleResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PUBLISHARTICLERESPONSE_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=324,
  serialized_end=431,
)

_GETARTICLESREQUEST.fields_by_name['client'].message_type = protos_dot_Client_dot_Client__pb2._CLIENT
_GETARTICLESREQUEST.fields_by_name['date'].message_type = protos_dot_Article_dot_Article__pb2._DATE
_GETARTICLESRESPONSE.fields_by_name['article_list'].message_type = protos_dot_Article_dot_Article__pb2._ARTICLE
_PUBLISHARTICLEREQUEST.fields_by_name['client'].message_type = protos_dot_Client_dot_Client__pb2._CLIENT
_PUBLISHARTICLEREQUEST.fields_by_name['article'].message_type = protos_dot_Article_dot_Article__pb2._ARTICLE
_PUBLISHARTICLERESPONSE.fields_by_name['status'].enum_type = _PUBLISHARTICLERESPONSE_STATUS
_PUBLISHARTICLERESPONSE_STATUS.containing_type = _PUBLISHARTICLERESPONSE
DESCRIPTOR.message_types_by_name['GetArticlesRequest'] = _GETARTICLESREQUEST
DESCRIPTOR.message_types_by_name['GetArticlesResponse'] = _GETARTICLESRESPONSE
DESCRIPTOR.message_types_by_name['PublishArticleRequest'] = _PUBLISHARTICLEREQUEST
DESCRIPTOR.message_types_by_name['PublishArticleResponse'] = _PUBLISHARTICLERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetArticlesRequest = _reflection.GeneratedProtocolMessageType('GetArticlesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETARTICLESREQUEST,
  '__module__' : 'grpc.server.server_service_pb2'
  # @@protoc_insertion_point(class_scope:GetArticlesRequest)
  })
_sym_db.RegisterMessage(GetArticlesRequest)

GetArticlesResponse = _reflection.GeneratedProtocolMessageType('GetArticlesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETARTICLESRESPONSE,
  '__module__' : 'grpc.server.server_service_pb2'
  # @@protoc_insertion_point(class_scope:GetArticlesResponse)
  })
_sym_db.RegisterMessage(GetArticlesResponse)

PublishArticleRequest = _reflection.GeneratedProtocolMessageType('PublishArticleRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHARTICLEREQUEST,
  '__module__' : 'grpc.server.server_service_pb2'
  # @@protoc_insertion_point(class_scope:PublishArticleRequest)
  })
_sym_db.RegisterMessage(PublishArticleRequest)

PublishArticleResponse = _reflection.GeneratedProtocolMessageType('PublishArticleResponse', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHARTICLERESPONSE,
  '__module__' : 'grpc.server.server_service_pb2'
  # @@protoc_insertion_point(class_scope:PublishArticleResponse)
  })
_sym_db.RegisterMessage(PublishArticleResponse)



_SERVERSERVICE = _descriptor.ServiceDescriptor(
  name='ServerService',
  full_name='ServerService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=434,
  serialized_end=574,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetArticles',
    full_name='ServerService.GetArticles',
    index=0,
    containing_service=None,
    input_type=_GETARTICLESREQUEST,
    output_type=_GETARTICLESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='PublishArticle',
    full_name='ServerService.PublishArticle',
    index=1,
    containing_service=None,
    input_type=_PUBLISHARTICLEREQUEST,
    output_type=_PUBLISHARTICLERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SERVERSERVICE)

DESCRIPTOR.services_by_name['ServerService'] = _SERVERSERVICE

# @@protoc_insertion_point(module_scope)
