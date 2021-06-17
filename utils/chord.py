import Pyro5.api as pr
import os

th = pr.Proxy("PYRO:newchord@127.0.0.1:5600")

pid = os.getpid()
th.call(pid) 
input()
exit()