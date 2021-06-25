import time, subprocess, threading

def init():
    subprocess.call(['python3', 'server.py', 'start-service'])

def router():
    subprocess.call(['python3', 'router.py'])

def tables():
    subprocess.call(['python3', 'server.py', 'update-finger-tables'])

def nodes():
    subprocess.call(['python3', 'server.py', 'update-deleted-node'])

if __name__ == "__main__":
    threading.Thread(target=init).start()
    time.sleep(2)
    threading.Thread(target=router).start()
    time.sleep(2)
    threading.Thread(target=tables).start()
    time.sleep(.5)
    threading.Thread(target=nodes).start()
    time.sleep(.5)
    print("Service is Ready!")
    while True:
        pass