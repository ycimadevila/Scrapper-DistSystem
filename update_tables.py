import Pyro5.api as pr


th = pr.Proxy("PYRO:update@127.0.0.1:5600")

th.call()
