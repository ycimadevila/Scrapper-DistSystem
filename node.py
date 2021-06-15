import random, time
import threading

class ChordSystem:
    def __init__(self, m):
        self.m = m
        self.nodes = {}
        self.nodesid = []
        self.ip = {}
        self.ntotal = pow(2, m)
        
    
    def add_new_node(self):
        poss_id = random.choice(list(set([i for i in range(self.ntotal)]) - set(self.nodesid)))
        print("Se agrego el nodo:", poss_id)

        self.nodesid.append(poss_id)
        self.nodesid.sort()

        node = Node(poss_id, self.m, self)
        self.nodes[poss_id] = node

        first = len(self.nodes) == 1
        node.calculate_ft(first=first)

        self.update_hash_table()

    def delete_node(self, _id):
        if _id in self.nodesid: 
            print(f'No se pudo eliminar el nodo {_id} ya que no existe.')
            return

        self.nodesid.remove(_id)
        self.nodes.pop(_id)
        self.update_hash_table()

    def update_hash_table(self):
        first = len(self.nodes) == 1
        for node in self.nodes.values():
            node.calculate_ft(first=first)

    def update_tables_by_time(self):
        while True:
            time.sleep(60)
            print('updating table')
            self.update_hash_table()

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

    
class Node:
    def __init__(self, id, m, chord_system):
        self.id = id
        self.m = m
        self.nbits = pow(2, m)
        self.ntotal = chord_system.ntotal
        self.ft = [0 for _ in range(m + 1)]
        self.chord = chord_system


    def inbetween(self, key, lwb, upb):                                         
        if lwb <= upb:                                                            
            return lwb <= key and key < upb                                         
        
        return (lwb <= key and key < upb + self.ntotal) or (lwb <= key + self.ntotal and key < upb)                        


    def finger(self, i):
        succ = (self.id + pow(2, i-1)) % self.ntotal                                        
        lwbi = self.chord.nodesid.index(self.id)                                              
        upbi = (lwbi + 1) % len(self.chord.nodesid)                                           
        for _ in range(len(self.chord.nodesid)):                                              
            if self.inbetween(succ, self.chord.nodesid[lwbi] + 1, self.chord.nodesid[upbi] + 1):
                return self.chord.nodesid[upbi]                                               
            (lwbi,upbi) = (upbi, (upbi + 1) % len(self.chord.nodesid))                        
        return None  


    def calculate_ft(self, first=False):
        if first:
            self.ft = [self.id for _ in range(self.m + 1)]
            return
        
        self.ft[0]  = self.chord.nodesid[self.chord.nodesid.index(self.id) - 1] 
        self.ft[1:] = [self.finger(i) for i in range(1,self.m + 1)]     
 

    def local_succ_node(self, key):
        maxmin = self.id
        for i in range(1, len(self.ft)):
            if self.ft[i] == key:
                maxmin = self.ft[i]
                break
            elif self.ft[i] > key:
                break
            maxmin = self.ft[i]
        return maxmin
