from sys import exec_prefix
import Pyro5.errors as perror
import Pyro5.api as pra
import time, random
from utils.node import ChordSystem
from utils.const import *

def search_for_node(key_):
    key = int(key_)
    system = ChordSystem(m__)
    actv_nodes = system.get_alive_chord_identifier()

    rd_node = random.choice(list(actv_nodes))
    if key not in actv_nodes:
        print('La llave no existe en el conjunto.')
        return None

    else:
        if rd_node not in actv_nodes:
            actv_nodes = system.get_alive_chord_identifier()
            rd_node = random.choice(list(actv_nodes))
        
        i = 0
        # get the node to use
        node = system.get_chord_node(rd_node) 
        print(type(node), node.get_id())

        while node.get_id() != key:
            nextid = node.local_succ_node(key)
            print(nextid)
            if nextid not in actv_nodes:
                update_all_nodes_after_deleting(nextid)
                nextid = node.local_succ_node(key)

            i += 1
            if i > pow(2, m__) - 1: # stop case (just in case)
                break
            
            node = pra.Proxy(f"PYRONAME:user.chord.{nextid}")
            print(node.get_id())
        else:
            return node
        return None
