import time
n = 0
def clock():
    global n
    if n == 50:
        return
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    print(hour,minute,second)
    n += 1
    clock()
    
clock()
