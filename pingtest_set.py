# Import modules
import subprocess
import time


timeout = time.time() + 60*1   # 5 minutes from now
# Configure subprocess to hide the console window
info = subprocess.STARTUPINFO()
info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE

# For each IP address in the subnet, 
# run the ping command with subprocess.popen interface
statusa = 0
timeout = time.time() + 60*1   # 5 minutes from now
while statusa == 0:
    while True:
        if timeout == time.time() or time.time() > timeout:
            statusa = 1
            break



        output = subprocess.Popen(['ping', '-n', '1', '-w', '500', '212.143.237.31'], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]

        if "Destination host unreachable" in output.decode('utf-8'):
            print('212.143.237.31', "is Offline")
        elif "Request timed out" in output.decode('utf-8'):
            print('212.143.237.31', "is Offline")
        else:

            print('212.143.237.31', "is Online")
            statusa = 1
            break
print('finished')