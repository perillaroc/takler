# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: takler/server/protocol/takler.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#takler/server/protocol/takler.proto\x12\x0ftakler_protocol\"0\n\x0fServiceResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"(\n\x13\x43hildCommandOptions\x12\x11\n\tnode_path\x18\x01 \x01(\t\"[\n\x0bInitCommand\x12;\n\rchild_options\x18\x01 \x01(\x0b\x32$.takler_protocol.ChildCommandOptions\x12\x0f\n\x07task_id\x18\x02 \x01(\t\"N\n\x0f\x43ompleteCommand\x12;\n\rchild_options\x18\x01 \x01(\x0b\x32$.takler_protocol.ChildCommandOptions\"[\n\x0c\x41\x62ortCommand\x12;\n\rchild_options\x18\x01 \x01(\x0b\x32$.takler_protocol.ChildCommandOptions\x12\x0e\n\x06reason\x18\x02 \x01(\t\"_\n\x0c\x45ventCommand\x12;\n\rchild_options\x18\x01 \x01(\x0b\x32$.takler_protocol.ChildCommandOptions\x12\x12\n\nevent_name\x18\x02 \x01(\t\"t\n\x0cMeterCommand\x12;\n\rchild_options\x18\x01 \x01(\x0b\x32$.takler_protocol.ChildCommandOptions\x12\x12\n\nmeter_name\x18\x02 \x01(\t\x12\x13\n\x0bmeter_value\x18\x03 \x01(\t\"#\n\x0eRequeueCommand\x12\x11\n\tnode_path\x18\x01 \x01(\t\"#\n\x0eSuspendCommand\x12\x11\n\tnode_path\x18\x01 \x03(\t\".\n\nRunCommand\x12\r\n\x05\x66orce\x18\x01 \x01(\x08\x12\x11\n\tnode_path\x18\x02 \x03(\t\"\xd9\x01\n\x0c\x46orceCommand\x12\x37\n\x05state\x18\x01 \x01(\x0e\x32(.takler_protocol.ForceCommand.ForceState\x12\x11\n\trecursive\x18\x02 \x01(\x08\x12\x0c\n\x04path\x18\x03 \x03(\t\"o\n\nForceState\x12\x0b\n\x07unknown\x10\x00\x12\x0c\n\x08\x63omplete\x10\x01\x12\n\n\x06queued\x10\x02\x12\r\n\tsubmitted\x10\x03\x12\n\n\x06\x61\x63tive\x10\x04\x12\x0b\n\x07\x61\x62orted\x10\x05\x12\t\n\x05\x63lear\x10\x06\x12\x07\n\x03set\x10\x07\"\r\n\x0bShowRequest\"\x1e\n\x0cShowResponse\x12\x0e\n\x06output\x18\x01 \x01(\t2\xc6\x07\n\x0cTaklerServer\x12R\n\x0eRunInitCommand\x12\x1c.takler_protocol.InitCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12Z\n\x12RunCompleteCommand\x12 .takler_protocol.CompleteCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12T\n\x0fRunAbortCommand\x12\x1d.takler_protocol.AbortCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12T\n\x0fRunEventCommand\x12\x1d.takler_protocol.EventCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12T\n\x0fRunMeterCommand\x12\x1d.takler_protocol.MeterCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12X\n\x11RunRequeueCommand\x12\x1f.takler_protocol.RequeueCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12X\n\x11RunSuspendCommand\x12\x1f.takler_protocol.SuspendCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12W\n\x10RunResumeCommand\x12\x1f.takler_protocol.SuspendCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12P\n\rRunRunCommand\x12\x1b.takler_protocol.RunCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12T\n\x0fRunForceCommand\x12\x1d.takler_protocol.ForceCommand\x1a .takler_protocol.ServiceResponse\"\x00\x12O\n\x0eRunShowRequest\x12\x1c.takler_protocol.ShowRequest\x1a\x1d.takler_protocol.ShowResponse\"\x00\x42\x35Z3github.com/perillaroc/takler-client/takler_protocolb\x06proto3')



_SERVICERESPONSE = DESCRIPTOR.message_types_by_name['ServiceResponse']
_CHILDCOMMANDOPTIONS = DESCRIPTOR.message_types_by_name['ChildCommandOptions']
_INITCOMMAND = DESCRIPTOR.message_types_by_name['InitCommand']
_COMPLETECOMMAND = DESCRIPTOR.message_types_by_name['CompleteCommand']
_ABORTCOMMAND = DESCRIPTOR.message_types_by_name['AbortCommand']
_EVENTCOMMAND = DESCRIPTOR.message_types_by_name['EventCommand']
_METERCOMMAND = DESCRIPTOR.message_types_by_name['MeterCommand']
_REQUEUECOMMAND = DESCRIPTOR.message_types_by_name['RequeueCommand']
_SUSPENDCOMMAND = DESCRIPTOR.message_types_by_name['SuspendCommand']
_RUNCOMMAND = DESCRIPTOR.message_types_by_name['RunCommand']
_FORCECOMMAND = DESCRIPTOR.message_types_by_name['ForceCommand']
_SHOWREQUEST = DESCRIPTOR.message_types_by_name['ShowRequest']
_SHOWRESPONSE = DESCRIPTOR.message_types_by_name['ShowResponse']
_FORCECOMMAND_FORCESTATE = _FORCECOMMAND.enum_types_by_name['ForceState']
ServiceResponse = _reflection.GeneratedProtocolMessageType('ServiceResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVICERESPONSE,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.ServiceResponse)
  })
_sym_db.RegisterMessage(ServiceResponse)

ChildCommandOptions = _reflection.GeneratedProtocolMessageType('ChildCommandOptions', (_message.Message,), {
  'DESCRIPTOR' : _CHILDCOMMANDOPTIONS,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.ChildCommandOptions)
  })
_sym_db.RegisterMessage(ChildCommandOptions)

InitCommand = _reflection.GeneratedProtocolMessageType('InitCommand', (_message.Message,), {
  'DESCRIPTOR' : _INITCOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.InitCommand)
  })
_sym_db.RegisterMessage(InitCommand)

CompleteCommand = _reflection.GeneratedProtocolMessageType('CompleteCommand', (_message.Message,), {
  'DESCRIPTOR' : _COMPLETECOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.CompleteCommand)
  })
_sym_db.RegisterMessage(CompleteCommand)

AbortCommand = _reflection.GeneratedProtocolMessageType('AbortCommand', (_message.Message,), {
  'DESCRIPTOR' : _ABORTCOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.AbortCommand)
  })
_sym_db.RegisterMessage(AbortCommand)

EventCommand = _reflection.GeneratedProtocolMessageType('EventCommand', (_message.Message,), {
  'DESCRIPTOR' : _EVENTCOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.EventCommand)
  })
_sym_db.RegisterMessage(EventCommand)

MeterCommand = _reflection.GeneratedProtocolMessageType('MeterCommand', (_message.Message,), {
  'DESCRIPTOR' : _METERCOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.MeterCommand)
  })
_sym_db.RegisterMessage(MeterCommand)

RequeueCommand = _reflection.GeneratedProtocolMessageType('RequeueCommand', (_message.Message,), {
  'DESCRIPTOR' : _REQUEUECOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.RequeueCommand)
  })
_sym_db.RegisterMessage(RequeueCommand)

SuspendCommand = _reflection.GeneratedProtocolMessageType('SuspendCommand', (_message.Message,), {
  'DESCRIPTOR' : _SUSPENDCOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.SuspendCommand)
  })
_sym_db.RegisterMessage(SuspendCommand)

RunCommand = _reflection.GeneratedProtocolMessageType('RunCommand', (_message.Message,), {
  'DESCRIPTOR' : _RUNCOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.RunCommand)
  })
_sym_db.RegisterMessage(RunCommand)

ForceCommand = _reflection.GeneratedProtocolMessageType('ForceCommand', (_message.Message,), {
  'DESCRIPTOR' : _FORCECOMMAND,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.ForceCommand)
  })
_sym_db.RegisterMessage(ForceCommand)

ShowRequest = _reflection.GeneratedProtocolMessageType('ShowRequest', (_message.Message,), {
  'DESCRIPTOR' : _SHOWREQUEST,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.ShowRequest)
  })
_sym_db.RegisterMessage(ShowRequest)

ShowResponse = _reflection.GeneratedProtocolMessageType('ShowResponse', (_message.Message,), {
  'DESCRIPTOR' : _SHOWRESPONSE,
  '__module__' : 'takler.server.protocol.takler_pb2'
  # @@protoc_insertion_point(class_scope:takler_protocol.ShowResponse)
  })
_sym_db.RegisterMessage(ShowResponse)

_TAKLERSERVER = DESCRIPTOR.services_by_name['TaklerServer']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z3github.com/perillaroc/takler-client/takler_protocol'
  _SERVICERESPONSE._serialized_start=56
  _SERVICERESPONSE._serialized_end=104
  _CHILDCOMMANDOPTIONS._serialized_start=106
  _CHILDCOMMANDOPTIONS._serialized_end=146
  _INITCOMMAND._serialized_start=148
  _INITCOMMAND._serialized_end=239
  _COMPLETECOMMAND._serialized_start=241
  _COMPLETECOMMAND._serialized_end=319
  _ABORTCOMMAND._serialized_start=321
  _ABORTCOMMAND._serialized_end=412
  _EVENTCOMMAND._serialized_start=414
  _EVENTCOMMAND._serialized_end=509
  _METERCOMMAND._serialized_start=511
  _METERCOMMAND._serialized_end=627
  _REQUEUECOMMAND._serialized_start=629
  _REQUEUECOMMAND._serialized_end=664
  _SUSPENDCOMMAND._serialized_start=666
  _SUSPENDCOMMAND._serialized_end=701
  _RUNCOMMAND._serialized_start=703
  _RUNCOMMAND._serialized_end=749
  _FORCECOMMAND._serialized_start=752
  _FORCECOMMAND._serialized_end=969
  _FORCECOMMAND_FORCESTATE._serialized_start=858
  _FORCECOMMAND_FORCESTATE._serialized_end=969
  _SHOWREQUEST._serialized_start=971
  _SHOWREQUEST._serialized_end=984
  _SHOWRESPONSE._serialized_start=986
  _SHOWRESPONSE._serialized_end=1016
  _TAKLERSERVER._serialized_start=1019
  _TAKLERSERVER._serialized_end=1985
# @@protoc_insertion_point(module_scope)
