import Pyro5.nameserver as ns
import Pyro5.api as pra
from utils.const import *
import typer, random, threading, time
from utils.node import ChordSystem, ChordNode


prog = typer.Typer()

def update_node():
    while True:
        print('actualice')
        system = ChordSystem(m__)
        id_available = set(system.get_alive_chord_identifier())

        print('actualice', id_available)
        nodes = set()

        for _id in id_available:
            greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}")
            print(_id, greeting_maker)
            nodes.union(greeting_maker.get_ft_values())

        print('actualice')
        nodes = nodes - id_available

        print('actualice:', id_available, nodes)
        for node in nodes:
            update_all_nodes_after_deleting(node)
        
        time.sleep(15)


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

@prog.command()
def active_nodes():
    system = ChordSystem(m__)
    id_available = system.get_alive_chord_identifier()
    
    for _id in id_available:
        print(_id)

@prog.command()
def start_service():
    uri, daemon, _ = ns.start_ns(host=host__, port=port__)
    print(f"NS running on {uri.location}")
    print(f"URI => {uri.protocol}:{uri.object}@{uri.location}")
    threading.Thread(target=update_node).start()
    daemon.requestLoop()

@prog.command()
def client(id_):
    key = int(id_)
    system = ChordSystem(m__)
    actv_nodes = system.get_alive_chord_identifier()

    rd_node = random.choice(list(actv_nodes))
    if key not in actv_nodes:
        print('La llave no existe en el conjunto.')

    else:
        if rd_node not in actv_nodes:
            actv_nodes = system.get_alive_chord_identifier()
            rd_node = random.choice(list(actv_nodes))
        
        i = 0
        # get the node to use
        node = pra.Proxy(f"PYRONAME:user.chord.{rd_node}") 

        while node.get_id() != key:
            nextid = node.local_succ_node(key)
            if nextid not in actv_nodes:
                update_all_nodes_after_deleting(nextid)
                nextid = node.local_succ_node(key)

            i += 1
            if i > pow(2, m__) - 1: # forzando un caso de parada (just in case)
                break
            
            node = pra.Proxy(f"PYRONAME:user.chord.{nextid}")
        else:
            print('El nodo fue encontrado')
            return
        


@prog.command()
def add_chord(_id):
    system = ChordSystem(m__)

    poss_id = int(_id)
    # poss_id = system.get_id_available()

    node = ChordNode(poss_id, m__)
    alive_nodes = system.get_alive_chord_identifier()

    for _id in alive_nodes:
        node.add_node(int(_id))

    node.calculate_ft()

    system.register_node_chord(node)
    update_all_nodes_after_adding(poss_id)
    
    system.requestLoop()


@prog.command()
def fingertable():
    system = ChordSystem(m__)
    id_available = system.get_alive_chord_identifier()
    
    for _id in id_available:
        greeting_maker = pra.Proxy(
            f"PYRONAME:user.chord.{_id}"
        )  # use name server object lookup uri shortcut
        print(f'{_id} -> {greeting_maker.get_finger_table()}')

if __name__ == "__main__":
    prog()
    