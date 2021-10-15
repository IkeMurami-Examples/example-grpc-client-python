from encoder import encode, decode

from base64 import b64encode, b64decode

import time_pb2
import time_pb2_grpc

import grpc


TARGET = 'api.example.com:443'


channel_creds = grpc.ssl_channel_credentials()
channel = grpc.secure_channel(
    TARGET, 
    channel_creds,
    options=(
        # ('grpc.ssl_target_name_override', 'localhost'),
        # ('grpc.http_proxy', 'http://localhost:8080'),  # https://github.com/grpc/grpc/blob/v1.38.x/include/grpc/impl/codegen/grpc_types.h
    )
)

client = time_pb2_grpc.TimeServiceStub(channel)

try:
    request = time_pb2.GetTimeRequest()

    # serialized = request.SerializeToString()
    # serialized = b64encode(serialized).decode()

    response = client.GetTime.with_call(
        request
    )
    
    print(response)

except grpc.RpcError as e:
    # ouch!
    # lets print the gRPC error message
    # which is "Length of `Name` cannot be more than 10 characters"
    print(e.details())
    # lets access the error code, which is `INVALID_ARGUMENT`
    # `type` of `status_code` is `grpc.StatusCode`
    status_code = e.code()
    # should print `INVALID_ARGUMENT`
    print(status_code.name)
    # should print `(3, 'invalid argument')`
    print(status_code.value)
    # want to do some specific action based on the error?
    if grpc.StatusCode.INVALID_ARGUMENT == status_code:
        # do your stuff here
        pass