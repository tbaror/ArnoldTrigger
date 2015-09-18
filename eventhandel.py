# Windows Event Log Viewer
# FB - 201012116
import win32evtlog # requires pywin32 pre-installed

server = 'localhost' # name of the target computer to get event logs
logtype = 'Application' # 'Application' # 'Security'
hand = win32evtlog.OpenEventLog(server,logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)
ev = 0
while ev == 0:
    events = win32evtlog.ReadEventLog(hand, flags,0)
    if events:
        for event in events:
            if event.EventID == 8216 and event.SourceName == 'System Restore':
                print ('Event Category:', event.EventCategory)
                print ('Time Generated:', event.TimeGenerated)
                print ('Source Name:', event.SourceName)
                print ('Event ID:', event.EventID)
                print ('Event Type:', event.EventType)
                data = event.StringInserts
                if data:
                    print ('Event Data:')
                    for msg in data:
                        print (msg)

                ev = 1
    else:
        ev = 1

class EvntCollector():
    def __init__(self,EvtHost='localhost',LogType='Application',EvtSourceName='Microsoft-Windows-Power-Troubleshooter',EvtID=51,NumEvt=1,DataPayload):
        self.EvtHost = EvtHost
        self.LogType = LogType
        self.EvtSourceName = EvtSourceName
        self.EvtID = EvtID
        self.NumEvt = NumEvt
        self.Datapayload = DataPayload


    def RetrieveEvent(self):
        hand = win32evtlog.OpenEventLog(self.EvtHost,self.LogType)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        ev = 0
        while ev != self.NumEvt:
            events = win32evtlog.ReadEventLog(hand, flags,0)
            if events:
                for event in events:
                    if event.EventID == self.EvtID and event.SourceName == self.EvtSourceName:

                        self.Datapayload["EvtSourceName"] = event.SourceName ,self.Datapayload["EvtID"]= self.EvtID
                    data = event.StringInserts
                if data:

                    for msg in data:
                        self.Datapayload["EventData"]= msg

                ev += 1
        else:
            ev += 1




print('exit')
