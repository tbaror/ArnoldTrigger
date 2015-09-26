# Windows Event Log Viewer
# FB - 201012116
import win32evtlog # requires pywin32 pre-installed
import pickle
import os ,sys
import base64
import json

class GetServerInfo:
    def __init__(self):

        self.DataPayload ={'EvtSourceName':'','EvtSourceNameII':'','EvtID':'','EvtIDII':'','EventData':'','TimeGenerated':'','AuthPass':''}

    def ReadConfig(self):

        try:
            with open('dataset.js') as json_file:
                #read config from config file
                DataSet = json.load(json_file)

                #connect to Dalet MS SQL retrieve Dalet Data
                builder = HostTypesStructureBuilder(DataSet['DaletSiteData'][0]['HostNameDb'],DataSet['DaletSiteData'][0]['UserDb'],DataSet['DaletSiteData'][0]['PasswordDb'],DataSet['DaletSiteData'][0]['DatabaseName'])

                #Structure and organized Data
                builder.daletDbGetData()
                dataStructure = builder.build()
                configuratinBuilder = IcingaConfgurationBuilder(dataStructure)

                #Make sure no old Data remained
                ctrlconfig = IcingaCheckConfig(dataStructure,DataSet['DaletSiteData'][0]['IcingaDaletConfPath'])
                ctrlconfig.icingaConfigTruncate()

                #Writing new data files
                configuratinBuilder.generateConfigurationFilepGroups()
                configuratinBuilder.generateConfigurationFileHosts()

                #Check for Valid config and apply to load it
                #ctrlconfig.applyConfig()

                #Save current config for later compare
                ctrlconfig.saveCurrentConfig()

        except(FileNotFoundError):
            print('No such file or directory:dataset.js')
            exit



class PassRetriever:
    def __init__(self,PassFile,DataPayload):

        self.PassFile = PassFile
        self.DataPayload = DataPayload

    def GetPassword(self):

        ReadPassword =  pickle.load(open(os.getcwd()+'/'+self.PassFile,'rb'))
        PassDecoded = base64.decode(ReadPassword)
        PassDecoded = PassDecoded.decod("utf-8")
        self.DataPayload['AuthPass'] = PassDecoded









class EvntCollector:
    def __init__(self,LogType,EvtSourceName,EvtID,NumEvt,DataPayload):

        self.LogType = LogType
        self.EvtSourceName = EvtSourceName
        self.EvtID = EvtID
        self.NumEvt = NumEvt
        self.Datapayload = DataPayload
        print(self.Datapayload)


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
                    if event.EventID == self.EvtID or self.EvtID == '' and event.SourceName == self.EvtSourceName:

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
        pass


eventb = EvntCollector('Application','Software Protection Platform Service',1073742726,1,{"EvtSourceName":'',"EvtID":'',"TimeGenerated":'',"EventData":''})
eventb.RetrieveEvent()