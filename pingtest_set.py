# Import modules
import subprocess
import time

t = '0.3'
def pinghost():
    timeout = time.time() + (60*float(t))   # 5 minutes from now
    # Configure subprocess to hide the console window
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = subprocess.SW_HIDE

    # For each IP address in the subnet,
    # run the ping command with subprocess.popen interface
    statusa = 0
    #timeout = time.time() + 60*1   # 5 minutes from now
    while statusa == 0:
        while True:
            if timeout == time.time() or time.time() > timeout:
                toto = 'failed'
                return toto



            output = subprocess.Popen(['ping', '-n', '1', '-w', '500', '212.143.237.155'], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]

            if "Destination host unreachable" in output.decode('utf-8'):
                pass
            elif "Request timed out" in output.decode('utf-8'):
                pass
            else:

                print('212.143.237.31', "is Online")
                toto = 'success'
                return toto
print(pinghost())