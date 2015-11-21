#!/usr/bin/env python

# skeleton from http://kmkeen.com/socketserver/2009-04-03-13-45-57-003.html

import socketserver, subprocess, sys
from threading import Thread
from pprint import pprint
import json ,os

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
        try:
            print(self.server.serverset)
            data = json.loads(self.request.recv(1024).decode('UTF-8').strip())
            # process the data, i.e. print it:
            #print(self.client_address)
            print(data)
            # send some 'ok' back
            self.request.sendall(bytes(json.dumps({'return':'ok','SERVERIP':'self.client_address[0]'}), 'UTF-8'))
        except Exception as e:
            print("Exception wile receiving message: ", e)
class TcpSessionServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True
    test = "test"

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        #read configuraiton and seve it as class member
        serverinit = GetServerInfo()
        self.serverset = serverinit.ReadConfig()

if __name__ == "__main__":
    serverinit = GetServerInfo()
    serverset = serverinit.ReadConfig()
    print(serverset['EnforcementHost'],int(serverset['SrvPort']))
    server = TcpSessionServer((serverset['EnforcementHost'], int(serverset['SrvPort'])), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
