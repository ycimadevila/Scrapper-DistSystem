from Pyro5.api import Daemon, Proxy, expose, locate_ns
import random, os
from urllib.request import urlopen
from utils.const import *


class ChordSystem:
    def __init__(self, m):
        self.daemon = Daemon()
        self.locate_ns = locate_ns(host=host__, port=port__)

        self.m = m
        self.ntotal = pow(2, m)
        self.total_nodes = set(range(self.ntotal))

    @staticmethod
    def node_chord_uri(_id, _host, _port):
        return f"PYRONAME:user.chord.{_id}@{_host}:{_port}"

    def register_node_chord(self, node: 'ChordNode'):
        object_id = f"user.chord.{node.id}"
        uri = self.daemon.register(node, object_id)
        self.locate_ns.register(
            object_id, uri, metadata=["user.chord"]
        )
        return uri

    def get_id_available(self):
        nodes = self.locate_ns.yplookup(meta_all=["user.chord"])
        alive_nodes = set(int(node_name.replace("user.chord.", "")) for node_name in nodes)
        aviables_nodes = list(self.total_nodes - alive_nodes)
        return random.choice(aviables_nodes)

    def get_alive_chord_identifier(self):
        nodes = self.locate_ns.yplookup(meta_all=["user.chord"])
        return set(int(node_name.replace("user.chord.", "")) for node_name in nodes)

    def get_identifier(self):
        return self.locate_ns.yplookup(meta_all=["user.chord"])

    def requestLoop(self):
        try:
            self.daemon.requestLoop()
        except:
            pass

    
    def get_chord_node(self, _id):
        uri = self.node_chord_uri(_id, host__, port__)
        return Proxy(uri)
        

    def look_for_a_key(self, key):
        print(f"Iniciando búsqueda del nodo {key}.")

        if key not in self.nodesid:
            print(f"El nodo {key} no se encuentra en el conjunto.")
            return
        
        current_id = self.nodesid[0]

        i = 0
        while current_id != key:
            current_node = self.nodes[current_id]
            current_id = current_node.local_succ_node(key)

            i += 1
            if i > self.ntotal - 1: # forzando un caso de parada (just in case)
                break
        else:
            print(f"El nodo {key} fue encontrado en {i} iteraciones.")
            return
        print("Error en la busqueda del nodo")

                    

@expose
class ChordNode:
    def __init__(self, id, m):
        self.id = id
        self.m = m
        self.nbits = pow(2, m)
        
        self.ft = [0 for _ in range(m + 1)]
        self.nodesid = [self.id]

        # (url, filename)
        self.storage_filename = {}

    #############################
    # storage and scrap methods #
    #############################

    def storage_html(self, url, html: str, filename):
        try:
            os.mkdir('downloads')
        except FileExistsError:
            pass
        f = open (f'downloads/{filename}.txt','w')
        f.write(html)
        f.close()
        self.storage_filename[url] = filename

    def get_html(self, url):
        filename = self.storage_filename[url]
        try:
            f = open (f'downloads/{filename}.txt','r')
            f.read()
            f.close()
            return filename
        except:
            return None

    def scrap_url(self, url):
        print(f'Scrapping {url}')
        try:
            page = urlopen(url) # devuelve un objeto HTTPResponse

            html_bytes = page.read() # devuelve el html como una secuencia de bytes
            html = html_bytes.decode("utf-8") # convierte a string
            print('Scrap Done!\n\nWaiting')
        except:
            html = None
            print('Scrap Fail!\n\nWaiting')
        return html


    #################
    # chord methods #
    #################

    def get_id(self):
        return self.id
        
    def predecessor(self):
        return self.ft[0]

    def succesor(self):
        return self.ft[1]

    def get_finger_table(self):
        return [_ for _ in self.ft]

    def add_node(self, _id):
        self.nodesid = set(self.nodesid)
        self.nodesid.add(_id)
        self.nodesid = list(self.nodesid)
        self.calculate_ft()
    
    def del_node(self, _id):
        try:
            self.nodesid.discard(_id)
            self.calculate_ft()
        except KeyError:
            pass

    def inbetween(self, key, lwb, upb):                                         
        if lwb <= upb:                                                            
            return lwb <= key and key < upb                                         
        
        return (lwb <= key and key < upb + self.nbits) or (lwb <= key + self.nbits and key < upb)                        


    def finger(self, i):
        succ = (self.id + pow(2, i-1)) % self.nbits                                        
        lwbi = self.nodesid.index(self.id)                                              
        upbi = (lwbi + 1) % len(self.nodesid)                                           
        for _ in range(len(self.nodesid)):                                              
            if self.inbetween(succ, self.nodesid[lwbi] + 1, self.nodesid[upbi] + 1):
                return self.nodesid[upbi]                                               
            (lwbi,upbi) = (upbi, (upbi + 1) % len(self.nodesid))                        
        return None  


    def calculate_ft(self):
        self.nodesid.sort()
        if len(self.nodesid) == 1:
            self.ft = [self.id for _ in range(self.m + 1)]
            return
        self.ft[0]  = self.nodesid[self.nodesid.index(self.id) - 1] 
        self.ft[1:] = [self.finger(i) for i in range(1,self.m + 1)]     
 

    def local_succ_node(self, key):
        maxmin = self.id
        for i in range(1, len(self.ft)):
            if self.ft[i] == key:
                return self.ft[i]
            elif self.ft[i] > key:
                break
            elif self.ft[i] > maxmin:
                maxmin = self.ft[i]
        return maxmin
