# Example a Python-client for a gRPC service

## Build

```
$ python3 -m venv .venv
$ source .venv/bin/activate

$ python -m pip install grpcio
$ python -m pip install grpcio-tools

$ python -m grpc_tools.protoc -I ./proto --python_out=. --grpc_python_out=. ./proto/web/*/*.proto
```

## encoder.py

Есть расширение формата сообщений gRPC — gRPC-Web

Пример таких сообщений:

```
POST /my.example.timeservice.TimeService/GetTime HTTP/2
Host: api.example.com
Content-Type: application/grpc-web-text+proto
Authorization: Bearer ...
...

AAAAAAA=


HTTP/2 200 OK
Content-Type: application/grpc-web-text+proto
...

AAAAAAA=gAAAAB5ncnBjLXN0YXR1czowDQpncnBjLW1lc3NhZ2U6DQo=
```

В encoder.py реализовал кодирование/декодированиие таких сообщениий

## client.py

Пример запроса/ответа по протоколу gRPC.