# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zeromq/server/server_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos.Article import Article_pb2 as protos_dot_Article_dot_Article__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"zeromq/server/server_service.proto\x1a\x1cprotos/Article/Article.proto\"\\\n\x12GetArticlesRequest\x12\x13\n\x0b\x63lient_uuid\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\x12\x13\n\x04\x64\x61te\x18\x04 \x01(\x0b\x32\x05.Date\"5\n\x13GetArticlesResponse\x12\x1e\n\x0c\x61rticle_list\x18\x01 \x03(\x0b\x32\x08.Article\"G\n\x15PublishArticleRequest\x12\x13\n\x0b\x63lient_uuid\x18\x01 \x01(\t\x12\x19\n\x07\x61rticle\x18\x02 \x01(\x0b\x32\x08.Article\"k\n\x16PublishArticleResponse\x12.\n\x06status\x18\x01 \x01(\x0e\x32\x1e.PublishArticleResponse.Status\"!\n\x06Status\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\"(\n\x11ServerJoinRequest\x12\x13\n\x0b\x63lient_uuid\x18\x01 \x01(\t\"c\n\x12ServerJoinResponse\x12*\n\x06status\x18\x01 \x01(\x0e\x32\x1a.ServerJoinResponse.Status\"!\n\x06Status\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\")\n\x12ServerLeaveRequest\x12\x13\n\x0b\x63lient_uuid\x18\x01 \x01(\t\"e\n\x13ServerLeaveResponse\x12+\n\x06status\x18\x01 \x01(\x0e\x32\x1b.ServerLeaveResponse.Status\"!\n\x06Status\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'zeromq.server.server_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETARTICLESREQUEST._serialized_start=68
  _GETARTICLESREQUEST._serialized_end=160
  _GETARTICLESRESPONSE._serialized_start=162
  _GETARTICLESRESPONSE._serialized_end=215
  _PUBLISHARTICLEREQUEST._serialized_start=217
  _PUBLISHARTICLEREQUEST._serialized_end=288
  _PUBLISHARTICLERESPONSE._serialized_start=290
  _PUBLISHARTICLERESPONSE._serialized_end=397
  _PUBLISHARTICLERESPONSE_STATUS._serialized_start=364
  _PUBLISHARTICLERESPONSE_STATUS._serialized_end=397
  _SERVERJOINREQUEST._serialized_start=399
  _SERVERJOINREQUEST._serialized_end=439
  _SERVERJOINRESPONSE._serialized_start=441
  _SERVERJOINRESPONSE._serialized_end=540
  _SERVERJOINRESPONSE_STATUS._serialized_start=364
  _SERVERJOINRESPONSE_STATUS._serialized_end=397
  _SERVERLEAVEREQUEST._serialized_start=542
  _SERVERLEAVEREQUEST._serialized_end=583
  _SERVERLEAVERESPONSE._serialized_start=585
  _SERVERLEAVERESPONSE._serialized_end=686
  _SERVERLEAVERESPONSE_STATUS._serialized_start=364
  _SERVERLEAVERESPONSE_STATUS._serialized_end=397
# @@protoc_insertion_point(module_scope)
