# Windows Event Log Viewer
# FB - 201012116
import win32evtlog # requires pywin32 pre-installed


class EvntCollector:
    def __init__(self,LogType,EvtSourceName,EvtID,NumEvt,DataPayload):

        self.LogType = LogType
        self.EvtSourceName = EvtSourceName
        self.EvtID = EvtID
        self.NumEvt = NumEvt
        self.Datapayload = DataPayload
        print(self.Datapayload)


    def RetrieveEvent(self):

        hand = win32evtlog.OpenEventLog('localhost',self.LogType)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        ev = 0
        while ev != self.NumEvt:
            events = win32evtlog.ReadEventLog(hand, flags,0)
            if events:
                for event in events:
                    if event.EventID == self.EvtID and event.SourceName == self.EvtSourceName:

                        self.Datapayload["EvtSourceName"] = event.SourceName ,self.Datapayload["EvtID"]= self.EvtID,self.Datapayload['TimeGenerated']= event.TimeGenerated

                        data = event.StringInserts
                        if data:

                            for msg in data:
                                self.Datapayload["EventData"]= msg

                        ev += 1
            else:
                ev += 1
        print(self.Datapayload)

eventb = EvntCollector('Application','System Restore',8216,1,{"EvtSourceName":'',"EvtID":'',"TimeGenerated":'',"EventData":''})
eventb.RetrieveEvent()