# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: registry_server_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dregistry_server_service.proto\"F\n\x15RegisterServerRequest\x12\x13\n\x0bserver_name\x18\x01 \x01(\t\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\"1\n\x16RegisterServerResponse\x12\x17\n\x06status\x18\x01 \x01(\x0e\x32\x07.Status\"+\n\x14GetServerListRequest\x12\x13\n\x0b\x63lient_uuid\x18\x01 \x01(\t\"}\n\x15GetServerListResponse\x12\x34\n\x07servers\x18\x01 \x03(\x0b\x32#.GetServerListResponse.ServersEntry\x1a.\n\x0cServersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01*!\n\x06Status\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'registry_server_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETSERVERLISTRESPONSE_SERVERSENTRY._options = None
  _GETSERVERLISTRESPONSE_SERVERSENTRY._serialized_options = b'8\001'
  _STATUS._serialized_start=328
  _STATUS._serialized_end=361
  _REGISTERSERVERREQUEST._serialized_start=33
  _REGISTERSERVERREQUEST._serialized_end=103
  _REGISTERSERVERRESPONSE._serialized_start=105
  _REGISTERSERVERRESPONSE._serialized_end=154
  _GETSERVERLISTREQUEST._serialized_start=156
  _GETSERVERLISTREQUEST._serialized_end=199
  _GETSERVERLISTRESPONSE._serialized_start=201
  _GETSERVERLISTRESPONSE._serialized_end=326
  _GETSERVERLISTRESPONSE_SERVERSENTRY._serialized_start=280
  _GETSERVERLISTRESPONSE_SERVERSENTRY._serialized_end=326
# @@protoc_insertion_point(module_scope)
