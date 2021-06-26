import time, subprocess, threading, sys


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
    time.sleep(1)

    threading.Thread(target=router).start()
    time.sleep(1)

    threading.Thread(target=tables).start()
    threading.Thread(target=nodes).start()

    print("Service is Ready!")
