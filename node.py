import random, time

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

        self.update_hash_table()

    def update_hash_table(self):
        first = len(self.nodes) == 1
        for node in self.nodes.values():
            node.calculate_ft(first=first)

    def update_tables_by_time(self):
        while True:
            time.sleep(60)
            self.update_hash_table()

    def look_for_a_key(self, key):
        if key not in self.nodesid:
            print(f"El nodo {key} no se encuentra en el conjunto.")
            return
        initial_node_id = self.nodesid[0]
        current_id = initial_node_id

        i = 1
        while current_id != key:
            current_node = self.nodes[current_id]
            print(f'node: {current_id}, {current_node.id}')
            current_id = current_node.local_succ_node(current_id)
            print(current_id)
            i += 1
            if i > 30:
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


    def local_succ_node_(self, key): 
        if self.inbetween(key, self.ft[0] + 1, self.id - 1):  
            print('sali1')                
            return self.ft[0]                                                   
        elif self.inbetween(key, self.id + 1, self.ft[1]):                    
            print('sali2')                
            return self.ft[1]                                                 
        for i in range(1, self.m):                                    
            if self.inbetween(key, self.ft[i], self.ft[(i + 1) % self.nbits]):
                print('sali3')                
                return self.ft[i]  
            print('ando dando vueltas')

    def local_succ_node(self, key):
        maxmin = self.ft[1]
        for i in range(1, len(self.ft)):
            if self.ft[i] > key:
                break
            maxmin = self.ft[i]
        return maxmin

            




####################################################################################################################

'''
    def run(self): 
        self.chan.bind(self.nodeID) 
        self.addNode(self.nodeID) 
        others = list(self.chan.channel.smembers('node') - set([str(self.nodeID)])) 
        for i in others: 
        self.addNode(i) 
        self.chan.sendTo([i], (JOIN)) 
        self.recomputeFingerTable() 
    
        while True: 
            message = self.chan.recvFromAny() # Wait for any request 
            sender  = message[0]              # Identify the sender 
            request = message[1]              # And the actual request 
            if request[0] != LEAVE and self.chan.channel.sismember('node',str(sender)): 
                self.addNode(sender) 
            if request[0] == STOP: 
                break 
            if request[0] == LOOKUP_REQ:                       # A lookup request 
                nextID = self.localSuccNode(request[1])          # look up next node 
                self.chan.sendTo([sender], (LOOKUP_REP, nextID)) # return to sender 
                if not self.chan.exists(nextID): 
                    self.delNode(nextID)    
            elif request[0] == JOIN: 
                continue 
            elif request[0] == LEAVE: 
                self.delNode(sender) 
            self.recomputeFingerTable() 
            print('FT[','%04d'%self.nodeID,']: ',['%04d' % k for k in self.FT]) #
 
class ChordClient: 
    def __init__(self, chan):                
        self.chan    = chan 
        self.nodeID  = int(self.chan.join('client')) 
    
    def run(self): 
        self.chan.bind(self.nodeID) 
        procs = [int(i) for i in list(self.chan.channel.smembers('node'))] 
        procs.sort() 
        print(['%04d' % k for k in procs]) 
        p = procs[random.randint(0,len(procs)-1)] 
        key = random.randint(0,self.chan.MAXPROC-1) 
        print(self.nodeID, "sending LOOKUP request for", key, "to", p) 
        self.chan.sendTo([p],(LOOKUP_REQ, key)) 
        msg = self.chan.recvFrom([p]) 
        while msg[1][1] != p: 
            p = msg[1][1] 
            self.chan.sendTo([p],(LOOKUP_REQ, key)) 
            msg = self.chan.recvFrom([p]) 
        print(self.nodeID, "received final answer from", p) 
        self.chan.sendTo(procs, (STOP)) 
 
'''