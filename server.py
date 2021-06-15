import Pyro5.api as pra
from Pyro5.server import expose
from node import Node, ChordSystem
import threading
import os

m = 0

while True:
    try:
        print('Entre la cantidad de bits necesarias: ')
        m = int(input())
        if m < 1:
            raise TypeError()
        print('Iniciando servidor...')
        print('Servidor inicado.')
        break
    except TypeError:
        print("Entrada invalida. La entrada debe ser un entero (int) mayor que 0.")

chord = ChordSystem(m)


@pra.expose
class new_chord_node(object):
    def call(self):
        chord.add_new_node()
        # try:
        #     chord.add_new_node()
        # except KeyboardInterrupt:
        #     print(f'el nodo {key} ha sido eliminado')
        #     chord.delete_node()

@pra.expose
class new_client(object):
    def call(self, key):
        if key < 0 or key > pow(2, m) - 1:
            print('La llave a buscar no puede ser negativa o mayor que 2^m')
            return
        return chord.look_for_a_key(key)

@pra.expose
class finger_tables(object):
    def call(self):
        if not chord.nodes:
            print('\tNo hay nodos para mostrar')
            print(f'node: - finger-table: -')
        else:
            print('\tFinger Table:')
            for node in chord.nodes.values():
                print(f'node: {node.id} finger-table: {node.ft}')

@pra.expose
class update_tables(object):
    def call(self):
        thread = threading.Thread(target=chord.update_tables_by_time())
        thread.start()

pra.Daemon.serveSimple(
    {
        new_chord_node: "chord",
        new_client: "client",
        finger_tables: "ft",
        update_tables: "update"
    },
    ns=False, verbose=False, host="127.0.0.1", port=5600)

os.system('python3 update_tables.py')