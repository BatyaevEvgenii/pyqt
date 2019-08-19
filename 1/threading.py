import time
import threading

def sample(name, num):
    for item in range(1, num+1):
        time.sleep(1)
        print(f' {name} was called {item} times')

thread2 = threading.Thread(target=sample, args=('thear', 10))
thread2.start()

sample('asda', 5)