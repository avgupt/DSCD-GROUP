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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dregistry_server_service.proto\"2\n\x16RegisterReplicaRequest\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"\xd9\x01\n\x17RegisterReplicaResponse\x12\x1a\n\x12is_replica_primary\x18\x01 \x01(\x08\x12\x1a\n\x12primary_replica_ip\x18\x02 \x01(\t\x12\x1c\n\x14primary_replica_port\x18\x03 \x01(\x05\x12\x14\n\x0creplica_name\x18\x04 \x01(\t\x12/\n\x06status\x18\x05 \x01(\x0e\x32\x1f.RegisterReplicaResponse.Status\"!\n\x06Status\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\"\x17\n\x15GetReplicaListRequest\")\n\x16GetReplicaListResponse\x12\x0f\n\x07servers\x18\x01 \x03(\t2\xa4\x01\n\x15RegistryServerService\x12\x46\n\x0fRegisterReplica\x12\x17.RegisterReplicaRequest\x1a\x18.RegisterReplicaResponse\"\x00\x12\x43\n\x0eGetReplicaList\x12\x16.GetReplicaListRequest\x1a\x17.GetReplicaListResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'registry_server_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REGISTERREPLICAREQUEST._serialized_start=33
  _REGISTERREPLICAREQUEST._serialized_end=83
  _REGISTERREPLICARESPONSE._serialized_start=86
  _REGISTERREPLICARESPONSE._serialized_end=303
  _REGISTERREPLICARESPONSE_STATUS._serialized_start=270
  _REGISTERREPLICARESPONSE_STATUS._serialized_end=303
  _GETREPLICALISTREQUEST._serialized_start=305
  _GETREPLICALISTREQUEST._serialized_end=328
  _GETREPLICALISTRESPONSE._serialized_start=330
  _GETREPLICALISTRESPONSE._serialized_end=371
  _REGISTRYSERVERSERVICE._serialized_start=374
  _REGISTRYSERVERSERVICE._serialized_end=538
# @@protoc_insertion_point(module_scope)
