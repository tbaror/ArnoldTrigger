import socketserver
import json,os


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




class InitTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

class StartTCPServerHandler(socketserver.BaseRequestHandler):
    def __init__(self,QuarantineIp,QrnPort):


        self.QuarantineIp = QuarantineIp
        self.QrnPort = QrnPort

    def handle(self):
        try:
            data = json.loads(self.request.recv(1024).decode('UTF-8').strip())
            # process the data, i.e. print it:
            print(str(self.client_address))
            print(data)
            # send some 'ok' back

            self.request.sendall(bytes(json.dumps({'return':'ok'}), 'UTF-8'))
        except Exception as e:
            print("Exception wile receiving message: ", e)


class EnforceAction:
    def __init__(self):
        pass

serverinit = GetServerInfo()
serverset = serverinit.ReadConfig()
server = InitTCPServer(('0.0.0.0', 3031), StartTCPServerHandler(serverset['QuarantineIp'],serverset['QrnPort']))
server.serve_forever()
