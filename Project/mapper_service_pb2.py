# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mapper_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14mapper_service.proto\"N\n\nMapRequest\x12\r\n\x05query\x18\x01 \x01(\x05\x12\x16\n\x0einput_location\x18\x02 \x01(\t\x12\x19\n\x11input_split_files\x18\x03 \x03(\t\"y\n\x0bMapResponse\x12\"\n\x1aintermediate_file_location\x18\x01 \x01(\t\x12#\n\x06status\x18\x02 \x01(\x0e\x32\x13.MapResponse.Status\"!\n\x06Status\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x32\x33\n\rMapperService\x12\"\n\x03map\x12\x0b.MapRequest\x1a\x0c.MapResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mapper_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MAPREQUEST._serialized_start=24
  _MAPREQUEST._serialized_end=102
  _MAPRESPONSE._serialized_start=104
  _MAPRESPONSE._serialized_end=225
  _MAPRESPONSE_STATUS._serialized_start=192
  _MAPRESPONSE_STATUS._serialized_end=225
  _MAPPERSERVICE._serialized_start=227
  _MAPPERSERVICE._serialized_end=278
# @@protoc_insertion_point(module_scope)