
'"wevtutil qe Application /rd:true /f:text /q:"*[System[Provider[@Name='Symantec AntiVirus'] and (Level=1  or Level=2 or Level=3 or Level=4 or Level=0) and TimeCreated[timediff(@SystemTime) <= 3600000]]]"'
import re
import  os,json,datetime ,subprocess ,sys
ts = (str(datetime.datetime.now()))
jsarray = []
dictable = {}
KeyTyp = ''
KeComm = ''
ipad = 'ip.addr==172.18.4.10'
logfile = open("C:/Trace_test/stat.txt", 'w')
tsharkCall = ["wevtutil","qe",'Application','/rd:true','-qz','smb,srt,' + ipad]
tsharkProc = subprocess.Popen(tsharkCall,executable=os.environ["ProgramFiles"] + "/Wireshark/tshark.exe",universal_newlines=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

for plot in tsharkProc.stdout:
    sys.stdout.write(plot)
    logfile.write(plot)