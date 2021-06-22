from sys import exec_prefix
import Pyro5.errors as perror
import Pyro5.api as pra
import time, random
from utils.node import ChordSystem
from utils.const import *

def __update_deleted_node__():
    try:
        router = pra.Proxy(f"PYRONAME:user.router")
        while True:
            id_available = router.get_alive_nodes()
            print(id_available)
            deleted_nodes = set()

            for _id in id_available:
                try:
                    n = pra.Proxy(f"PYRONAME:user.chord.{_id}")
                    n.get_id()
                except:
                    print(f"Deleted node detected -> {_id}")
                    deleted_nodes.add(_id)
            
            router.alive_nodes_remove(deleted_nodes)

            for _ in router.get_alive_nodes():
                for del_id in deleted_nodes:
                    try:
                        greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}") 
                        greeting_maker.del_node(del_id)
                    except:
                        pass
            
            for url, nodesid in router.get_storage_url_id().items():
                for del_node in deleted_nodes:
                    if del_node in nodesid:
                        router.storage_url_id_remove_id(url, del_id)
            
            print('Searching for deleted nodes...')
            time.sleep(5)

    except KeyboardInterrupt:
        print('Closing...')
        exit(1)
    except:
        print('Closing by error...')
        pass

def __update_finger_tables__():
    try:
        router = pra.Proxy(f"PYRONAME:user.router")
        while True:
            id_available = router.get_alive_nodes()
            for _id in id_available:
                try:
                    greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}")
                    for i in id_available:
                        greeting_maker.add_node(i)
                    greeting_maker.calculate_ft()
                except:
                    print(_id)
            print('update hash table')
            time.sleep(6)
    except KeyboardInterrupt:
        exit(1)
    except:
        pass

def search_for_node(key_):
    key = int(key_)
    system = ChordSystem(m__)
    router = pra.Proxy(f'PYRONAME:user.router')
    actv_nodes = router.get_alive_nodes()

    rd_node = random.choice(list(actv_nodes))
    if key not in actv_nodes:
        print('Key isn\'t in the set.')
        return None

    else:
        if rd_node not in actv_nodes:
            actv_nodes = router.get_alive_nodes()
            rd_node = random.choice(list(actv_nodes))
        
        i = 0
        # get the node to use
        node = system.get_chord_node(rd_node) 
        print(type(node), node.get_id())

        while node.get_id() != key:
            nextid = node.local_succ_node(key)
            print('nextid', nextid)
            if nextid not in actv_nodes:
                __update_deleted_node__()
                __update_finger_tables__()
                nextid = node.local_succ_node(key)

            i += 1
            if i > pow(2, m__) - 1: # stop case (just in case)
                print('sdfghjkl', key)
                break
            
            node = pra.Proxy(f"PYRONAME:user.chord.{nextid}")
            print(node.get_id())
        else:
            return node
        
        return None
