from google.protobuf import message
from google.protobuf import timestamp_pb2
import grpc
from base64 import b64encode, b64decode
import struct
import hashlib


from google.protobuf.timestamp_pb2 import Timestamp


def encode(message, isMetadata=False):
    """message -> объект протобаф структуры
       isMetadata -> параметр для gRPC-Web
    """
    serialized = message.SerializeToString()
    length = len(serialized)
    header = struct.pack('>?I', isMetadata, length)

    serialized = header + serialized
    serialized = b64encode(serialized).decode()

    return serialized


def decode(message, pbMessageTypeObject):
    """
    Это дибилизм какой-то, но может быть такое, что просто заканкатенатят base64 сообщения, надо такое разбивать
    """
    messages = []
    flag = False
    res = ''
    for ch in message:
        if ch == '=':
            flag = True
            res += ch
        else:
            if flag:
                messages.append(res)
                res = ''
            res += ch
            flag = False

    if res:
        messages.append(res)

    res = {
        'messages': [],
        'metadata': None
    }


    for message in messages:
        message = b64decode(message)
        while message:
            type, length = struct.unpack('>bI', message[:5])
            if type == 0:  # \x00
                # data
                msg, message = message[5:5 + length], message[5 + length:]
                # TODO: Decode msg
                pbMessageTypeObject.ParseFromString(msg)
                
                res['messages'].append(msg)
            else:          # \x80
                metadata, message = message[5:5 + length], message[5 + length:]
                # TODO: Decode metadata
                res['metadata'] = metadata
        
    print('Object:', pbMessageTypeObject)
    print('Metadata:', res['metadata'])

    return res['metadata']


if __name__ == '__main__':
    import time_pb2

    # Encode

    message = time_pb2.GetTimeRequest(

    )

    serialized = encode(message)
    print(serialized)

    # Decode

    decode(
        'AAAAANoKJDN...JDv4==',
        time_pb2.GetTimeResponse()
    )