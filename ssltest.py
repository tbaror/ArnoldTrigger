import socket,ssl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 3031))
sslSocket = socket.ssl(s)
print repr(sslSocket.server())
print repr(sslSocket.issuer())
sslSocket.write('Hello secure socket\n')
s.close()