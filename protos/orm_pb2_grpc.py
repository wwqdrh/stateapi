# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import orm_pb2 as protos_dot_orm__pb2


class OrmApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TableBuild = channel.unary_unary(
                '/protos.OrmApi/TableBuild',
                request_serializer=protos_dot_orm__pb2.TableBuildRequest.SerializeToString,
                response_deserializer=protos_dot_orm__pb2.TableBuildResponse.FromString,
                )
        self.TableQuery = channel.unary_unary(
                '/protos.OrmApi/TableQuery',
                request_serializer=protos_dot_orm__pb2.QueryRequest.SerializeToString,
                response_deserializer=protos_dot_orm__pb2.QueryResponse.FromString,
                )
        self.TableInsert = channel.unary_unary(
                '/protos.OrmApi/TableInsert',
                request_serializer=protos_dot_orm__pb2.TableInsertRequest.SerializeToString,
                response_deserializer=protos_dot_orm__pb2.TableInsertResponse.FromString,
                )
        self.TableUpdate = channel.unary_unary(
                '/protos.OrmApi/TableUpdate',
                request_serializer=protos_dot_orm__pb2.UpdateRequest.SerializeToString,
                response_deserializer=protos_dot_orm__pb2.UpdateResponse.FromString,
                )
        self.TableDelete = channel.unary_unary(
                '/protos.OrmApi/TableDelete',
                request_serializer=protos_dot_orm__pb2.DeleteRequest.SerializeToString,
                response_deserializer=protos_dot_orm__pb2.DeleteResponse.FromString,
                )


class OrmApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def TableBuild(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TableQuery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TableInsert(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TableUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TableDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrmApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TableBuild': grpc.unary_unary_rpc_method_handler(
                    servicer.TableBuild,
                    request_deserializer=protos_dot_orm__pb2.TableBuildRequest.FromString,
                    response_serializer=protos_dot_orm__pb2.TableBuildResponse.SerializeToString,
            ),
            'TableQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.TableQuery,
                    request_deserializer=protos_dot_orm__pb2.QueryRequest.FromString,
                    response_serializer=protos_dot_orm__pb2.QueryResponse.SerializeToString,
            ),
            'TableInsert': grpc.unary_unary_rpc_method_handler(
                    servicer.TableInsert,
                    request_deserializer=protos_dot_orm__pb2.TableInsertRequest.FromString,
                    response_serializer=protos_dot_orm__pb2.TableInsertResponse.SerializeToString,
            ),
            'TableUpdate': grpc.unary_unary_rpc_method_handler(
                    servicer.TableUpdate,
                    request_deserializer=protos_dot_orm__pb2.UpdateRequest.FromString,
                    response_serializer=protos_dot_orm__pb2.UpdateResponse.SerializeToString,
            ),
            'TableDelete': grpc.unary_unary_rpc_method_handler(
                    servicer.TableDelete,
                    request_deserializer=protos_dot_orm__pb2.DeleteRequest.FromString,
                    response_serializer=protos_dot_orm__pb2.DeleteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'protos.OrmApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrmApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def TableBuild(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.OrmApi/TableBuild',
            protos_dot_orm__pb2.TableBuildRequest.SerializeToString,
            protos_dot_orm__pb2.TableBuildResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TableQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.OrmApi/TableQuery',
            protos_dot_orm__pb2.QueryRequest.SerializeToString,
            protos_dot_orm__pb2.QueryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TableInsert(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.OrmApi/TableInsert',
            protos_dot_orm__pb2.TableInsertRequest.SerializeToString,
            protos_dot_orm__pb2.TableInsertResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TableUpdate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.OrmApi/TableUpdate',
            protos_dot_orm__pb2.UpdateRequest.SerializeToString,
            protos_dot_orm__pb2.UpdateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TableDelete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.OrmApi/TableDelete',
            protos_dot_orm__pb2.DeleteRequest.SerializeToString,
            protos_dot_orm__pb2.DeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)