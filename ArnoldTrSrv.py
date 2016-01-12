#!/usr/bin/env python
'''
ArnoldTrSr -- Server Demon to manage Clients Detaining request

ArnoldTrSr is a Server Demon to manage Clients Detaining request TCP server to handle multiple IP clients

It defines classes_and_methods

@author:     Tal Bar-Or

@copyright:  2015 Dalet. All rights reserved.

@license:    Openlicense

@contact:    tbaror@gmail.com
@deffield    updated: 29/12/2015
'''
import socketserver, subprocess, sys,ssl
from threading import Thread
from pprint import pprint
from cryptography.fernet import Fernet
import json ,os
import base64 ,datetime

class GetServerInfo:
    def __init__(self):
        self.ServerSet ={'EnforcementHost':'','SrvPort':'','QuarantineIp':'','QrnPort':'','CryptKey':'','Password':'','StartArnoldLocation':'','DetantionProfile':''}

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
                self.ServerSet['StartArnoldLocation'] = DataSet['ArnoldSite'][0]['StartArnoldLocation']
                self.ServerSet['DetantionProfile'] = DataSet['ArnoldSite'][0]['DetantionProfile']

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
            #print(data['AuthPass'],self.server.serverset['CryptKey'],self.server.serverset['Password'])
            Authstart = AuthMec(data['AuthPass'],self.server.serverset['CryptKey'],self.server.serverset['Password'])
            if Authstart.DecPass():
                # send that auth process passed OK back
                self.request.sendall(bytes(json.dumps({'QuarantineIp':self.server.serverset['QuarantineIp'],'QrnPort':self.server.serverset['QrnPort'],'AUTHPASS':'OKPASS'}), 'UTF-8'))
                #Start Detain process
                DetainSession = DetainService(self.server.serverset['StartArnoldLocation'],self.server.serverset['DetantionProfile'],data['ComputerName'],self.client_address[0])
                DetainSession.DetainAction()
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


class DetainService:

    def __init__(self,StartArnoldLocation,DetantionProfile,ComputerName,IpToDetained):

        self.StartArnoldLocation = StartArnoldLocation
        self.DetantionProfile = DetantionProfile
        self.ComputerName = ComputerName
        self.IpToDetained = IpToDetained

    def DetainAction(self):

        #create detained file info
        detainfile = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + self.ComputerName
        infofile = open(os.getcwd()+'/'+ detainfile,'w')
        infofile.write(self.IpToDetained)
        infofile.close()
        os.system('cat '+os.getcwd()+'/'+ detainfile+' | '+self.StartArnoldLocation+' -i'+self.DetantionProfile)








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
