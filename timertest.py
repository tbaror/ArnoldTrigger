import time
timeout = time.time() + 60*1   # 5 minutes from now
while True:
    test = 0
    if timeout == time.time() or time.time() > timeout:
        break
    test = test - 1
print('finished:',time.time(),' timer:',timeout)



# Get NIC list and index number:
wmic nic get name, index

# Enable NIC with index number: (eg: 7)
wmic path win32_networkadapter where index=7 call enable

# Disable NIC with index number: (eg: 7)
wmic path win32_networkadapter where index=7 call disable

So in Python you would use something like

import subprocess
# get list of adapters and find index of adapter you want to disable.
subprocess.check_output('wmic nic get name, index')