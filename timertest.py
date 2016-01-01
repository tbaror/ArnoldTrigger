import time
timeout = time.time() + 60*1   # 5 minutes from now
while True:
    test = 0
    if timeout == time.time() or time.time() > timeout:
        break
    test = test - 1
print('finished:',time.time(),' timer:',timeout)