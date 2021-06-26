import Pyro5.api as pra
import time, random
from utils.node import ChordSystem
from utils.const import *

def __update_deleted_node__():
    try:
        router = pra.Proxy(f"PYRONAME:user.router@{host__}:{port__}")
        id_available = router.get_alive_nodes()
        deleted_nodes = set()

        for _id in id_available:
            try:
                n = pra.Proxy(f"PYRONAME:user.chord.{_id}@{host__}:{port__}")
                n.get_id()
            except:
                print(f"Deleted node detected -> {_id}")
                deleted_nodes.add(_id)
        
        router.alive_nodes_remove(deleted_nodes)

        for _ in router.get_alive_nodes():
            for del_id in deleted_nodes:
                try:
                    greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}@{host__}:{port__}") 
                    greeting_maker.del_node(del_id)
                except:
                    pass
        
        for url, nodesid in router.get_storage_url_id().items():
            for del_node in deleted_nodes:
                if del_node in nodesid:
                    router.storage_url_id_remove_id(url, del_id)
        
        for url, nodesid in router.get_storage_url_id().items():
            for del_node in deleted_nodes:
                if del_node in nodesid:
                    router.storage_url_id_remove_id(url, del_id)
        
        for del_node in deleted_nodes:
            router.scrapper_nodes_remove(del_id)
            router.storage_nodes_remove(del_id)
            
        print('Searching for deleted nodes...')
        time.sleep(2)

    except KeyboardInterrupt:
        print('Closing...')
        exit(1)
    except:
        print('Closing by error...')
        pass

def __update_finger_tables__():
    try:
        router = pra.Proxy(f"PYRONAME:user.router@{host__}:{port__}")
        id_available = router.get_alive_nodes()
        for _id in id_available:
            try:
                greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}@{host__}:{port__}")
                for i in id_available:
                    greeting_maker.add_node(i)
                greeting_maker.calculate_ft()
            except:
                print(_id)
    except KeyboardInterrupt:
        exit(1)
    except:
        pass

def search_for_node(key_):
    key = int(key_)
    system = ChordSystem(m__)
    router = pra.Proxy(f'PYRONAME:user.router@{host__}:{port__}')
    actv_nodes = router.get_alive_nodes()
    actv_nodes.sort()

    rd_node = actv_nodes[0]
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

        while node.get_id() != key:
            nextid = node.local_succ_node(key)
            if nextid not in router.get_alive_nodes():
                __update_deleted_node__()
                __update_finger_tables__()
                nextid = node.local_succ_node(key)
            i += 1
            if i > pow(2, m__) - 1: # stop case (just in case)
                break
            
            node = pra.Proxy(f"PYRONAME:user.chord.{nextid}@{host__}:{port__}")
        else:
            return node
        
        return None
