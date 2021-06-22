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
def update_deleted_node():
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
            
            print(router.get_alive_nodes())

            for _ in router.get_alive_nodes():
                for del_id in deleted_nodes:
                    try:
                        greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}") 
                        greeting_maker.del_node(del_id)
                    except:
                        print(del_id, _id)

            
            print('Searching for deleted nodes...')
            time.sleep(15)

    except KeyboardInterrupt:
        print('Closing...')
        exit(1)
    except:
        print('Closing by error...')
        pass

@prog.command()
def update_finger_tables():
    try:
        router = pra.Proxy(f"PYRONAME:user.router")
        while True:
            id_available = router.get_alive_nodes()
            print(id_available)
            for _id in id_available:
                try:
                    greeting_maker = pra.Proxy(f"PYRONAME:user.chord.{_id}")
                    for i in id_available:
                        greeting_maker.add_node(i)
                    greeting_maker.calculate_ft()
                except:
                    print(_id)
            print('update hash table')
            time.sleep(20)
    except KeyboardInterrupt:
        exit(1)
    except:
        pass

@prog.command()
def fingertable():
    router = pra.Proxy(f'PYRONAME:user.router')
    id_available = router.get_alive_nodes()
    
    for _id in id_available:
        node = pra.Proxy(f"PYRONAME:user.chord.{_id}") 
        print(f'{_id} -> {node.get_finger_table()}')

@prog.command()
def active_nodes():
    router = pra.Proxy(f'PYRONAME:user.router')
    id_available = router.get_alive_nodes()
    
    for _id in id_available:
        print(_id)

@prog.command()
def start_service():
    uri, daemon, _ = ns.start_ns(host=host__, port=port__)
    print(f"NS running on {uri.location}")
    print(f"URI => {uri.protocol}:{uri.object}@{uri.location}")
    daemon.requestLoop()

@prog.command()
def add_chord(id):
    system = ChordSystem(m__)
    router = pra.Proxy(f'PYRONAME:user.router')
    print(router)

    if id is None:
        poss_id = int(id)
    else:
        print('hey', router.get_alive_nodes())

        poss_id = router.get_available_id()
        print('hey')

    
    print('id', id)
    router.alive_nodes_add(poss_id)

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
    print('\n\n')

    alive_nodes = router.get_alive_nodes()
    print(alive_nodes)

    node = ChordNode(poss_id, m__)
    for _id in alive_nodes:
        node.add_node(int(_id))

    node.calculate_ft()

    system.register_node_chord(node)
    
    print('Waiting\n\n')
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
        return html
        
    elif url in router.get_storage_url_id().keys():
        print('Searching in Data Base...')

        # get nodeid from storage_url_id 
        nodeid = router.get_storage_url_id()[url][0]
        
        # search for node into chord ring 
        node = search_for_node(nodeid)

        # get filename and load html
        html = node.get_html(url)

        # return html
        return html

    elif url in router.get_scrapping_url():
        # wait until the url is scrapped
        timeout = 0
        while url in router.get_scrapping_url():
            timeout += 1
            if timeout == 120:
                break
            time.sleep(1)
        
        if url not in router.get_storage_url_id().keys():
            print('The Url can\'t be scrapped')
            return

        print('Searching in Data Base...')
        # get nodeid from storage_url_id 
        nodeid = router.get_storage_url_id()[url][0]
        
        # search for node into chord ring 
        node = search_for_node(nodeid)

        # get filename and load html
        html = node.get_html(url)
        
        print(html)
        # return html
        return html    


if __name__ == "__main__":
    prog()
    