import Pyro5.api as pra
import time, random
from utils.node import ChordSystem
from utils.const import *

'''
# (url: nodeid)
storage_url_id = {}

# storage the url while it's scrapping
scrapping_url = []

storage_nodes = []
scrapper_nodes = []
scrapper_nodes_available = []
rand = random.Random()

scrap_count = 0
'''

def update_node():
    try:
        while True:
            system = ChordSystem(m__)
            id_available = system.get_alive_chord_identifier()

            nodes = set()

            for _id in id_available:
                greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}")
                print(_id, greeting_maker.get_finger_table())
                nodes.union(greeting_maker.get_finger_table())

            nodes = nodes - id_available

            for node in nodes:
                update_all_nodes_after_deleting(node)
            
            print('Searching for deleted nodes...')
            time.sleep(20)
    except KeyboardInterrupt:
        exit(1)
    except:
        pass


def update_finger_tables():
    try:
        while True:
            system = ChordSystem(m__)
            id_available = system.get_alive_chord_identifier()

            for _id in id_available:
                greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}")
                for i in id_available:
                    greeting_maker.add_node(i)
                greeting_maker.calculate_ft()
            print('update hash table')
            time.sleep(20)
    except KeyboardInterrupt:
        exit(1)
    except:
        pass


def update_all_nodes_after_adding(poss_node):
    system = ChordSystem(m__)
    id_available = system.get_alive_chord_identifier()
    
    for _id in id_available:
        greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}")  # use name server object lookup uri shortcut
        greeting_maker.add_node(poss_node)

def update_all_nodes_after_deleting(poss_node):
    system = ChordSystem(m__)
    id_available = system.get_alive_chord_identifier()
    
    for _id in id_available:
        greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}")  # use name server object lookup uri shortcut
        greeting_maker.delete(poss_node)


def update_all_nodes_fingertable():
    system = ChordSystem(m__)
    id_available = system.get_alive_chord_identifier()
    
    for _id in id_available:
        greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}")  # use name server object lookup uri shortcut
        greeting_maker.calculate_ft()

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
            if i > pow(2, m__) - 1: # forzando un caso de parada (just in case)
                break
            
            node = pra.Proxy(f"PYRONAME:user.chord.{nextid}")
            print(node.get_id())
        else:
            return node
        return None
