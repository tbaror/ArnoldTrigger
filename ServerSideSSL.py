#!/usr/bin/env python

# skeleton from http://kmkeen.com/socketserver/2009-04-03-13-45-57-003.html

import socketserver, subprocess, sys,ssl
from threading import Thread
from pprint import pprint
from cryptography.fernet import Fernet
import json ,os
import base64 ,datetime

class GetServerInfo:
    def __init__(self):
        self.ServerSet ={'EnforcementHost':'','SrvPort':'','QuarantineIp':'','QrnPort':'','CryptKey':'','Password':''}

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
                self.ServerSet['CryptKey'] = DataSet['ArnoldSite'][0]['CryptKey']
                self.ServerSet['Password'] = DataSet['ArnoldSite'][0]['Password']

                return self.ServerSet


        except(FileNotFoundError):
            print('No such file or directory:dataset.js')
            exit



class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."


    def handle(self):
        try:

            
            #print(self.server.serverset)
            data = json.loads(self.request.recv(1024).decode('UTF-8').strip())
            # process the data, i.e. print it:
            #print(self.client_address)
            print(data['AuthPass'],self.server.serverset['CryptKey'],self.server.serverset['Password'])
            Authstart = AuthMec(data['AuthPass'],self.server.serverset['CryptKey'],self.server.serverset['Password'])
            if Authstart.DecPass():
                # send some 'ok' back
                self.request.sendall(bytes(json.dumps({'QuarantineIp':self.server.serverset['QuarantineIp'],'QrnPort':self.server.serverset['QrnPort'],'AUTHPASS':'OKPASS'}), 'UTF-8'))
            else:
                self.request.sendall(bytes(json.dumps({'AUTHPASS':'NOGO'}), 'UTF-8'))

        except Exception as e:
            print("Exception wilhe receiving message: ", e)


class TcpSessionServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True
    test = "test"

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.socket = ssl.wrap_socket(
        self.socket, server_side=True, certfile="cert.pem",do_handshake_on_connect=False)
        #read configuraiton and seve it as class member
        serverinit = GetServerInfo()
        
        self.serverset = serverinit.ReadConfig()

class AuthMec:
    def __init__(self,AuthPass,CryptKey,Password):
        self.AuthPass = AuthPass
        self.CryptKey = CryptKey
        self.Password = Password

    def DecPass(self):

        Token2byte = bytes(self.AuthPass,'utf-8')

        PassDecoded = base64.b64decode(Token2byte)
        LocalPassword = bytes(self.CryptKey,'utf-8')
        KeyDec = Fernet(PassDecoded)


        Passdec = KeyDec.decrypt(LocalPassword)
        print(Passdec)
        if Passdec.decode("utf-8") == self.Password:
            print('pass is equel')
            return True
        else:
            print('pass not equel')
            return  False


class DetainAction:

    def __init__(self,StartArnoldLocation,DetantionProfile,ComputerName,IpToDetained):

        self.StartArnoldLocation = StartArnoldLocation
        self.DetantionProfile = DetantionProfile
        self.ComputerName = ComputerName
        self.IpToDetained = IpToDetained





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
