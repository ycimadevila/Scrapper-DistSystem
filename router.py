from Pyro5.api import Daemon, expose, locate_ns
import random
from utils.const import * 


@expose
class Router:
    def __init__(self) -> None:
        # (url: nodeid)
        self.storage_url_id = {}

        # storage the url while it's scrapping
        self.scrapping_url = []

        # containers
        self.storage_nodes = []
        self.scrapper_nodes = []
        self.scrapper_nodes_available = []       

        self.rand = random.Random(656)
        self.scrap_count = 0
        self.alive_nodes = []
        self.all_nodes = set(range(pow(2, m__)))

    def get_alive_nodes(self):
        return [_ for _ in self.alive_nodes]

    def alive_nodes_add(self, id):
        self.alive_nodes.append(id)
    
    def alive_nodes_remove(self, list):
        for id in list:
            self.alive_nodes.remove(id)

    def get_available_id(self):
        return random.choice(list(self.all_nodes - set(self.alive_nodes)))

    def get_scrap_count(self):
        return self.scrap_count

    def increment_scrap_count(self):
        self.scrap_count += 1

    def get_storage_url_id(self):
        return self.storage_url_id.copy()
    
    def get_scrapping_url(self):
        return [_ for _ in self.scrapping_url]
    
    def get_storage_nodes(self):
        return [_ for _ in self.storage_nodes]

    def get_scrapper_nodes(self):
            return [_ for _ in self.scrapper_nodes]

    def get_scrapper_nodes_available(self):
            return [_ for _ in self.scrapper_nodes_available]

    def get_randint(self, lwb, upb):
        return self.rand.randint(lwb, upb)


    def storage_url_id_add(self, key, value):
        if key not in self.storage_url_id.keys():
            self.storage_url_id[key] = [value]
        else:
            self.storage_url_id[key].append(value)
    

    def storage_url_id_remove_url(self, key):
        self.storage_url_id.pop(key)
    
    def storage_url_id_remove_id(self, key, id):
        self.storage_url_id[key].remove(id)
        # del key (information get lost)
        if not self.storage_url_id[key]:
            self.storage_url_id.pop(key)


    def scrapping_url_add(self, url):
        self.scrapping_url.append(url)
    
    def scrapping_url_remove(self, url):
        try:
            self.scrapping_url.remove(url)
        except:
            pass

    
    def storage_nodes_add(self, id):
        self.storage_nodes.append(id)
        
    def storage_nodes_remove(self, id):
        try:
            self.storage_nodes.remove(id)
        except:
            pass
        
    def scrapper_nodes_add(self, id):
        self.scrapper_nodes.append(id)

    def scrapper_nodes_remove(self, id):
        try:
            self.scrapper_nodes.remove(id)
            self.scrapper_nodes_available.remove(id)
        except:
            pass

        
    def scrapper_nodes_available_add(self, id):
        self.scrapper_nodes_available.append(id)
    
    def scrapper_nodes_available_remove(self, id):
        self.scrapper_nodes_available.remove(id)


daemon = Daemon()
ns = locate_ns(host=host__, port=port__) 
uri = daemon.register(Router(), "user.router")
print(uri)
ns.register(f"user.router", uri, metadata=["user.router"])

print("Router is Ready.")
daemon.requestLoop()