import socket
import json

data = {'message':'hello world!', 'test':bytes('tIoUIXthxKcwzYY9uEKnyyir_eKQUlCqvB1tKH5eG7U=', 'utf-8')}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
s.send(bytes(json.dumps(data), 'UTF-8'))
result = json.loads(s.recv(1024).decode('UTF-8'))
print("%s"%result)
s.close()

