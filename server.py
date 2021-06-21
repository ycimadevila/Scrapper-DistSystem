from Pyro5.client import Proxy
import Pyro5.nameserver as ns
import Pyro5.api as pra
import typer, random, threading, time
from utils.node import ChordSystem, ChordNode
from __utils__ import *
from utils.const import *

prog = typer.Typer()


@prog.command()
def test(id):
    system = ChordSystem(m__)
    nodes = system.locate_ns.yplookup(meta_all=["user.chord"])
    for node in nodes:
        print(node, type(node))
    node = pra.Proxy(f"PYRONAME:user.chord.{id}")
    print(node)


@prog.command()
def fingertable():
    system = ChordSystem(m__)
    id_available = system.get_alive_chord_identifier()
    
    for _id in id_available:
        node = pra.Proxy(f"PYRONAME:user.chord.{_id}") 
        print(f'{_id} -> {node.get_finger_table()}')


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
    
    try:
        threading.Thread(target=update_node).start()
        threading.Thread(target=update_finger_tables).start()
    except:
        pass
    
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
            print('El nodo fue encontrado')
            return


@prog.command()
def add_chord(id):
    system = ChordSystem(m__)
    router = pra.Proxy(f'PYRONAME:user.router')
    print(router)
    if id is None:
        poss_id = int(id)
    else:
        poss_id = system.get_id_available()

    if not router.get_storage_nodes():
        router.storage_nodes_add(poss_id)
        print('New Storage Node', router.get_storage_nodes())
    elif not router.get_scrapper_nodes():
        router.scrapper_nodes_add(poss_id)
        router.scrapper_nodes_available_add(poss_id)
        print('New Scrapper Node', router.get_scrapper_nodes())
    else:
        rd = router.get_randint(0, 1)
        print(rd)
        rd %= 2
        if rd:
            router.storage_nodes_add(poss_id)
            print('New Storage Node', router.get_storage_nodes())
        else:
            router.scrapper_nodes_add(poss_id)
            print('New Scrapper Node', router.get_scrapper_nodes())
    print('paso\n\n')

    alive_nodes = system.get_alive_chord_identifier()

    node = ChordNode(poss_id, m__)
    for _id in alive_nodes:
        node.add_node(int(_id))

    node.calculate_ft()

    system.register_node_chord(node)
    
    print('Waiting')
    system.requestLoop()

   
@prog.command()
def scrap(url):
    
    router = pra.Proxy(f'PYRONAME:user.router')
    if not router.get_scrapper_nodes() and not router.get_storage_nodes():
        print('Unavailable System')
        return

    if url not in router.get_storage_url_id().keys() and url not in router.get_scrapping_url():
        # add url to [scrapping_url]
        router.scrapping_url_add(url)
        
        # select available scrapper node (random)
        rd = router.get_scrapper_nodes_available()
        rd = rd[random.randint(0, len(rd) - 1)]
        router.scrapper_nodes_available_remove(rd)
        
        # scrappe url
        node = Proxy(f'PYRONAME:user.chord.{rd}')
        html = node.scrap_url(url)

        if html is None:
            print('The Url can\'t be scrapped')
            return
        
        # del url to [scrapping_url] and putting the node available again
        router.scrapper_nodes_available_add(rd)
        router.scrapping_url_remove(url)
        
        # select available storage node (random)
        rd = router.get_storage_nodes()
        rd = rd[random.randint(0, len(rd) - 1)]
        node = search_for_node(rd)
        
        # add url into node and add (url: nodeid) to {storage_url_id}
        filename = f'arch_{router.get_scrap_count()}'
        node.storage_html(url, html, filename)
        router.increment_scrap_count()
        
        # return html
        print (html)
        
    elif url in router.get_storage_url_id().keys():
        # get nodeid from storage_url_id 
        nodeid = router.get_storage_url_id(url)
        
        # search for node into chord ring 
        node = search_for_node(nodeid)

        # get filename and load html
        html = node.get_html(url)

        # return html
        return html

    elif url in router.get_scrapping_url():
        # wait until the url is scrapped
        while url in router.get_scrapping_url():
            time.sleep(1)
        
        if router.get_storage_url_id().keys():
            print('The Url can\'t be scrapped')
            return

        # get nodeid from storage_url_id 
        nodeid = router.get_storage_url_id(url)
        
        # search for node into chord ring 
        node = search_for_node(nodeid)

        # get filename and load html
        html = node.get_html(url)

        # return html
        return html    



if __name__ == "__main__":
    prog()
    