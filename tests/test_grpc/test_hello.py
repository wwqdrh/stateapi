import asyncio
import logging

import grpc
import pytest

from protos import simple_pb2_grpc, simple_pb2

@pytest.mark.asyncio
async def test_simple_grpc():
    class Greeter(simple_pb2_grpc.GreeterServicer):
        async def SayHello(
                self, request: simple_pb2.HelloRequest,
                context: grpc.aio.ServicerContext) -> simple_pb2.HelloReply:
            return simple_pb2.HelloReply(message='Hello, %s!' % request.name)

    async def start_server():
        server = grpc.aio.server()
        simple_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
        listen_addr = '[::]:50051'
        server.add_insecure_port(listen_addr)
        logging.info("Starting server on %s", listen_addr)
        await server.start()
        # await server.wait_for_termination()

        await asyncio.sleep(10)

        await server.stop(grace=True)
    
    async def start_client():
        await asyncio.sleep(3) # wait server start

        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = simple_pb2_grpc.GreeterStub(channel)
            response = await stub.SayHello(simple_pb2.HelloRequest(name='you'))
        
        print("Greeter client received: " + response.message)
    
    await asyncio.gather(start_server(), start_client())

