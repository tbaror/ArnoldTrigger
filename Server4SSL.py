import socketserver
import json

class MyTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data = json.loads(self.request.recv(1024).decode('UTF-8').strip())
            # process the data, i.e. print it:
            #print(self.client_address)
            print(data)
            # send some 'ok' back
            self.request.sendall(bytes(json.dumps({'return':'ok'}), 'UTF-8'))
        except Exception as e:
            print("Exception wile receiving message: ", e)

server = MyTCPServer(('0.0.0.0', 3031), MyTCPServerHandler)
server.serve_forever()