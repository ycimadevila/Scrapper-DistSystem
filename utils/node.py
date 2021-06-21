from Pyro5.api import Daemon, Proxy, expose, locate_ns
import random

try:
    from utils.const import *
except: 
    from const import *


class ChordSystem:
    def __init__(self, m):
        self.daemon = Daemon()
        self.locate_ns = locate_ns()

        self.m = m
        self.ntotal = pow(2, m)
        self.total_nodes = set(range(self.ntotal))


    def register_node_chord(self, node: 'ChordNode'):
        object_id = f"user.chord.{node.id}"
        uri = self.daemon.register(node, object_id)
        self.locate_ns.register(
            object_id, uri, metadata=["user.chord"]
        )
        print(self.locate_ns)
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

    @staticmethod
    def node_chord_uri(_id):
        return f"PYRONAME:user.chord.{_id}"
    
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
            print(current_id)
            i += 1
            if i > self.ntotal - 1: # forzando un caso de parada (just in case)
                break
        else:
            print(f"El nodo {key} fue encontrado en {i} iteraciones.")
            return
        print("Error en la busqueda del nodo")
'''
    # def add_new_node(self, pid):
    #     if len(self.nodesid) != self.ntotal:
    #         poss_id = random.choice(list(set([i for i in range(self.ntotal)]) - set(self.nodesid)))
    #         print("Se agrego el nodo:", poss_id)

    #         self.nodes_pid_id[pid] = poss_id

    #         self.nodesid.append(poss_id)
    #         self.nodesid.sort()

    #         node = Node(poss_id, self.m, self)
    #         self.nodes[poss_id] = node

    #         first = len(self.nodes) == 1
    #         node.calculate_ft(first=first)

    #         self.update_hash_table()
    #     else:
    #         print('El sistema esta lleno, no acepta nuevos nodos')
    #         os.kill(pid, 1)
            
    # def delete_node(self, _id):
    #     if _id not in self.nodesid: 
    #         print(f'No se pudo eliminar el nodo {_id} ya que no existe.')
    #         return

    #     self.nodesid.remove(_id)
    #     self.nodes.pop(_id)
    #     self.update_hash_table()

    # def update_hash_table(self):
    #     first = len(self.nodes) == 1
    #     for node in self.nodes.values():
    #         node.calculate_ft(first=first)

    # def update_tables_by_time(self):
    #     while True:
    #         time.sleep(60)
    #         print('updating table')
    #         self.update_hash_table()

    

    # def append_url(self, url):
    #     self.url_stack.append(url)

    # def get_html_from_url(self, url):
    # if url in self.urls:
    #     counter = 120
    #     while url not in self.url_location.keys():
    #         time.sleep(.5)
    #         counter -= 1
    #         if counter == 0:
    #             break
    #     else:
    #         #buscar el nodo que contiene a la llave
    #         node_id = self.url_location[url]
            
    #         pass
    # else:
    #     # mandar a scrappear la url
    #     if self.scrapper_nodes_available:
    #         rd = random.randint(0, len(self.scrapper_nodes_available) - 1)
    #         node_available = self.scrapper_nodes_available[rd]
    #     else:
    #         pass
'''
                    

@expose
class ChordNode:
    def __init__(self, id, m):
        self.id = id
        self.m = m
        self.nbits = pow(2, m)
        
        self.ft = [0 for _ in range(m + 1)]
        self.nodesid = [self.id]

    def get_id(self):
        return self.id
              
    def get_ft_values(self):
        return set(self.ft)
        
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
            self.nodesid.remove(_id)
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
