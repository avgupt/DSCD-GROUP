# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: primaryBlocking/server_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import status_pb2 as primaryBlocking_dot_status__pb2
import time_stamp_pb2 as primaryBlocking_dot_time__stamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$primaryBlocking/server_service.proto\x1a\x1cprimaryBlocking/status.proto\x1a primaryBlocking/time_stamp.proto\"E\n\x0cWriteRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\t\x12\x0c\n\x04uuid\x18\x03 \x01(\t\"S\n\rWriteResponse\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x1b\n\x07version\x18\x02 \x01(\x0b\x32\n.TimeStamp\x12\x17\n\x06status\x18\x03 \x01(\x0b\x32\x07.Status\"\x1b\n\x0b\x46ileRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"h\n\x0cReadResponse\x12\x11\n\tfile_name\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x1b\n\x07version\x18\x04 \x01(\x0b\x32\n.TimeStamp\x12\x17\n\x06status\x18\x01 \x01(\x0b\x32\x07.Status2\x83\x01\n\rServerService\x12(\n\x05write\x12\r.WriteRequest\x1a\x0e.WriteResponse\"\x00\x12%\n\x04read\x12\x0c.FileRequest\x1a\r.ReadResponse\"\x00\x12!\n\x06\x64\x65lete\x12\x0c.FileRequest\x1a\x07.Status\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'primaryBlocking.server_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _WRITEREQUEST._serialized_start=104
  _WRITEREQUEST._serialized_end=173
  _WRITERESPONSE._serialized_start=175
  _WRITERESPONSE._serialized_end=258
  _FILEREQUEST._serialized_start=260
  _FILEREQUEST._serialized_end=287
  _READRESPONSE._serialized_start=289
  _READRESPONSE._serialized_end=393
  _SERVERSERVICE._serialized_start=396
  _SERVERSERVICE._serialized_end=527
# @@protoc_insertion_point(module_scope)
