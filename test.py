import threading
from subprocess import call

def thread_second():
    call(["python3", "test1.py"])
processThread = threading.Thread(target=thread_second)  # <- note extra ','
processThread.start()