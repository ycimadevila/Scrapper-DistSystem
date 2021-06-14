import Pyro5.api as pr


th = pr.Proxy("PYRO:ft@127.0.0.1:5600")

while True:
    print('Mostrar finger-table actual')
    print(th.call())
    print('Para actualiza la finger-table presione Enter...')
    input()
