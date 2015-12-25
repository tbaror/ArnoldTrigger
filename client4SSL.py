import socket ,ssl
import json

data = {'message':'hello world!', 'test':'tIoUIXthxKcwzYY9uEKnyyir_eKQUlCqvB1tKH5eG7U='}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(s,ca_certs='C:/Python34/Lib/site-packages/requests/cacert.pem',
                    cert_reqs=ssl.CERT_NONE)
s.connect(('127.0.0.1', 3031))
s.send(bytes(json.dumps(data), 'UTF-8'))
result = s.recv(1024)
text = result.decode('utf-8')
print(text)
#jsdata = json.loads(text)
#print("%s"%jsdata)
s.close()

