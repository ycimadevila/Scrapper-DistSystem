import Pyro5.api as pr


th = pr.Proxy("PYRO:client@127.0.0.1:5600")

while True:
    print('Elija la llave que desea buscar ')
    i = int(input())
    th.call(i)
