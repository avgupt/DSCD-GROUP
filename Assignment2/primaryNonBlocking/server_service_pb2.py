# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import status_pb2 as status__pb2
import time_stamp_pb2 as time__stamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14server_service.proto\x1a\x0cstatus.proto\x1a\x10time_stamp.proto\";\n\x1fSendReplicaInfoToPrimaryRequest\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"\x7f\n SendReplicaInfoToPrimaryResponse\x12\x38\n\x06status\x18\x01 \x01(\x0e\x32(.SendReplicaInfoToPrimaryResponse.Status\"!\n\x06Status\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\"E\n\x0cWriteRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\t\x12\x0c\n\x04uuid\x18\x03 \x01(\t\"S\n\rWriteResponse\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x1b\n\x07version\x18\x02 \x01(\x0b\x32\n.TimeStamp\x12\x17\n\x06status\x18\x03 \x01(\x0b\x32\x07.Status\"\x1d\n\rDeleteRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"\x1b\n\x0bReadRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"h\n\x0cReadResponse\x12\x11\n\tfile_name\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x1b\n\x07version\x18\x04 \x01(\x0b\x32\n.TimeStamp\x12\x17\n\x06status\x18\x01 \x01(\x0b\x32\x07.Status2\xe5\x02\n\rServerService\x12\x34\n\x0fwriteFromClient\x12\r.WriteRequest\x1a\x0e.WriteResponse\"\x00\x30\x01\x12\x33\n\x10writeFromPrimary\x12\r.WriteRequest\x1a\x0e.WriteResponse\"\x00\x12%\n\x04read\x12\x0c.ReadRequest\x1a\r.ReadResponse\"\x00\x12.\n\x11\x64\x65leteFromPrimary\x12\x0e.DeleteRequest\x1a\x07.Status\"\x00\x12/\n\x10\x64\x65leteFromClient\x12\x0e.DeleteRequest\x1a\x07.Status\"\x00\x30\x01\x12\x61\n\x18SendReplicaInfoToPrimary\x12 .SendReplicaInfoToPrimaryRequest\x1a!.SendReplicaInfoToPrimaryResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'server_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SENDREPLICAINFOTOPRIMARYREQUEST._serialized_start=56
  _SENDREPLICAINFOTOPRIMARYREQUEST._serialized_end=115
  _SENDREPLICAINFOTOPRIMARYRESPONSE._serialized_start=117
  _SENDREPLICAINFOTOPRIMARYRESPONSE._serialized_end=244
  _SENDREPLICAINFOTOPRIMARYRESPONSE_STATUS._serialized_start=211
  _SENDREPLICAINFOTOPRIMARYRESPONSE_STATUS._serialized_end=244
  _WRITEREQUEST._serialized_start=246
  _WRITEREQUEST._serialized_end=315
  _WRITERESPONSE._serialized_start=317
  _WRITERESPONSE._serialized_end=400
  _DELETEREQUEST._serialized_start=402
  _DELETEREQUEST._serialized_end=431
  _READREQUEST._serialized_start=433
  _READREQUEST._serialized_end=460
  _READRESPONSE._serialized_start=462
  _READRESPONSE._serialized_end=566
  _SERVERSERVICE._serialized_start=569
  _SERVERSERVICE._serialized_end=926
# @@protoc_insertion_point(module_scope)