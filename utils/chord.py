import Pyro5.api as pr


th = pr.Proxy("PYRO:newchord@127.0.0.1:5600")

th.call() 
input()
exit()