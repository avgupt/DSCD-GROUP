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


from . import server_pb2 as server__pb2
from . import status_pb2 as status__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dregistry_server_service.proto\x1a\x0cserver.proto\x1a\x0cstatus.proto\"h\n\x07Request\x12#\n\x04type\x18\x04 \x01(\x0e\x32\x15.Request.REQUEST_TYPE\"8\n\x0cREQUEST_TYPE\x12\x07\n\x03GET\x10\x00\x12\x08\n\x04READ\x10\x01\x12\t\n\x05WRITE\x10\x02\x12\n\n\x06\x44\x45LETE\x10\x03\"(\n\x08Response\x12\x1c\n\x0bserver_list\x18\x01 \x03(\x0b\x32\x07.Server2[\n\x15RegistryServerService\x12#\n\ngetServers\x12\x08.Request\x1a\t.Response\"\x00\x12\x1d\n\x07\x63onnect\x12\x07.Server\x1a\x07.Status\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'registry_server_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=61
  _REQUEST._serialized_end=165
  _REQUEST_REQUEST_TYPE._serialized_start=109
  _REQUEST_REQUEST_TYPE._serialized_end=165
  _RESPONSE._serialized_start=167
  _RESPONSE._serialized_end=207
  _REGISTRYSERVERSERVICE._serialized_start=209
  _REGISTRYSERVERSERVICE._serialized_end=300
# @@protoc_insertion_point(module_scope)
