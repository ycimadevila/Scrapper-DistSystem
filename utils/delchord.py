import Pyro5.api as pr
import sys

_id = int(sys.argv[1])

th = pr.Proxy("PYRO:delchord@127.0.0.1:5600")

th.call(_id) 
exit()