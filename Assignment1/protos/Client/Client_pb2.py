# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Client.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Client.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0c\x43lient.proto\"\x14\n\x06\x43lient\x12\n\n\x02id\x18\x01 \x01(\x05\x62\x06proto3'
)




_CLIENT = _descriptor.Descriptor(
  name='Client',
  full_name='Client',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Client.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=16,
  serialized_end=36,
)

DESCRIPTOR.message_types_by_name['Client'] = _CLIENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Client = _reflection.GeneratedProtocolMessageType('Client', (_message.Message,), {
  'DESCRIPTOR' : _CLIENT,
  '__module__' : 'Client_pb2'
  # @@protoc_insertion_point(class_scope:Client)
  })
_sym_db.RegisterMessage(Client)


# @@protoc_insertion_point(module_scope)