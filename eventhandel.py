# Windows Event Log Viewer
# FB - 201012116
import win32evtlog # requires pywin32 pre-installed
import pickle
import os ,socket
import base64
import json

class GetServerInfo:
    def __init__(self):

        self.QuarantineSet ={'EnforcementHost':'','SrvPort':'','EvtSourceName':'','EvtSourceNameII':'','EventID':'','EventIdII':'','LogType':'','EventData':'','NumEvt':'','AuthPass':''}

    def ReadConfig(self):

        try:
            with open(os.getcwd()+'\dataset.js') as json_file:
                #read config from config file
                DataSet = json.load(json_file)

                #Retrieve Json Data setting

                self.QuarantineSet['EnforcementHost'] = DataSet['ArnoldSite'][0]['EnforcementHost']
                self.QuarantineSet['SrvPort'] = DataSet['ArnoldSite'][0]['SrvPort']
                self.QuarantineSet['EvtSourceName'] = DataSet['ArnoldSite'][0]['EvtSourceName']
                self.QuarantineSet['EvtSourceNameII'] = DataSet['ArnoldSite'][0]['EvtSourceNameII']
                self.QuarantineSet['EventID'] = DataSet['ArnoldSite'][0]['EventID']
                self.QuarantineSet['EventIdII'] = DataSet['ArnoldSite'][0]['EventIdII']
                self.QuarantineSet['LogType'] = DataSet['ArnoldSite'][0]['LogType']
                self.QuarantineSet['NumEvt'] = DataSet['ArnoldSite'][0]['NumEvt']
                return self.QuarantineSet


        except(FileNotFoundError):
            print('No such file or directory:dataset.js')
            exit



class PassRetriever:
    def __init__(self):

        self.PassFile = ''
        self.AuthPass = ''
    def ReadConfig(self):

        try:
            with open(os.getcwd()+'\dataset.js') as json_file:
                #read config from config file
                DataSet = json.load(json_file)

                self.PassFile = DataSet['ArnoldSite'][0]['PassFile']

                #Retrieve Json Data setting
                return self.PassFile
        except(FileNotFoundError):
            print('No such file or directory:dataset.js')
            exit


    def GetPassword(self):


        ReadPassword =  pickle.load(open(os.getcwd()+'/'+self.ReadConfig(),'rb'))
        PassDecoded = base64.decode(ReadPassword)
        PassDecoded = PassDecoded.decod("utf-8")
        self.AuthPass = PassDecoded
        return self.AuthPass









class EvntCollector:
    def __init__(self,LogType,EvtSourceName,EvtSourceNameII,EvntID,EvntIdII,NumEvt):

        self.LogType = LogType
        self.EvtSourceName = EvtSourceName
        self.EvtSourceNameII =EvtSourceNameII
        self.EvntID = EvntID
        self.EvntIdII = EvntIdII
        self.NumEvt = NumEvt
        self.Datapayload = ''



    def RetrieveEvent(self):
        Datmsg = ''
        hand = win32evtlog.OpenEventLog('localhost',self.LogType)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        ev = 0
        while ev != self.NumEvt:
            events = win32evtlog.ReadEventLog(hand, flags,0)
            if events:
                for event in events:
                    if event.EventID == self.EvntID or self.EvntID == '' and event.SourceName == self.EvtSourceName:

                        self.Datapayload["EvtSourceName"] = event.SourceName
                        self.Datapayload["EvtID"]= self.EvtID
                        self.Datapayload['TimeGenerated']= str(event.TimeGenerated)

                        data = event.StringInserts
                        if data:

                            for msg in data:

                                Datmsg = Datmsg + msg
                                print(msg)
                                self.Datapayload["EventData"]= Datmsg

                        ev += 1
            else:
                ev += 1
        print(self.Datapayload)

class TcpClientConnect:
    def __init__(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 13373))
        s.send(bytes(json.dumps(data), 'UTF-8'))
        result = json.loads(s.recv(1024).decode('UTF-8'))
        print("%s"%result)
        s.close()



eventb = EvntCollector('Application','Software Protection Platform Service',1073742726,1,{"EvtSourceName":'',"EvtID":'',"TimeGenerated":'',"EventData":''})
eventb.RetrieveEvent()
readconfig = GetServerInfo()
test = readconfig.ReadConfig()
print(test['LogType'])