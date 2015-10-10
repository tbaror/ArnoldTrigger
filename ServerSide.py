#!/usr/bin/env python

# skeleton from http://kmkeen.com/socketserver/2009-04-03-13-45-57-003.html

import socketserver, subprocess, sys
from threading import Thread
from pprint import pprint
import json

my_unix_command =
HOST = '0.0.0.0'
PORT = 2000
class GetServerInfo:
    def __init__(self):
        self.ServerSet ={'EnforcementHost':'','SrvPort':'','QuarantineIp':'','QrnPort':''}

    def ReadConfig(self):

        try:
            with open(os.getcwd()+'/srvdataset.js') as json_file:
                #read config from config file
                DataSet = json.load(json_file)

                #Retrieve Json Data setting

                self.ServerSet['EnforcementHost'] = DataSet['ArnoldSite'][0]['EnforcementHost']
                self.ServerSet['SrvPort'] = DataSet['ArnoldSite'][0]['SrvPort']
                self.ServerSet['QuarantineIp'] = DataSet['ArnoldSite'][0]['QuarantineIp']
                self.ServerSet['QrnPort'] = DataSet['ArnoldSite'][0]['QrnPort']

                return self.ServerSet


        except(FileNotFoundError):
            print('No such file or directory:dataset.js')
            exit



class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        # self.request is the client connection
        data = self.request.recv(1024)  # clip input at 1Kb
        text = data.decode('utf-8')
        pprint(json.loads(text))
        self.request.send('OK'.encode('utf-8'))
        self.request.close()

class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
