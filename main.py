import random, threading, subprocess, sys, time


#######################
## GETTING ARGUMENTS ##
#######################

while True:
    try:
        if len(sys.argv) == 2:
            try:
                m = int(sys.argv[1])
                break
            except TypeError:
                print("La entrada debe ser un entero positivo mayor o igual que 1")
        else:
            raise InterruptedError('Cantidad de argumentos invalida')
    except InterruptedError as e:
        print(e)
        exit()


#############
## METHODS ##
#############

tbits = pow(2, m)
rd = random.randint(int(tbits * 2 / 3), tbits) # generate a random amount of active nodes

def create_node(_time=False):
    if _time:
        time.sleep(random.randint(70, 500))
    subprocess.call(["python3", "utils/chord.py"])
    
    
def update_tables():
    subprocess.call(["python3", "utils/update_tables.py"])

def del_node_random():
    while True:
        rd = random.randint(0, tbits - 1)
        time.sleep(random.randint(60, 600))
        subprocess.call(["python3", "utils/delchord.py", str(rd)])
    

########################
## ADDING CHORD NODES ##
########################

total_amount = 0
for i in range(0, rd):
    t = threading.Thread(target=create_node)
    # t.setDaemon(True)
    t.start()
    total_amount += 1

print(f'Se agregaron {total_amount} nodos inicialmente en el sistema.')


####################
## UPDATING TABLE ##
####################

t1 = threading.Thread(target=update_tables)
# t1.setDaemon(True)
t1.start()

##########################
## DELETING RANDOM NODE ##
##########################

t2 = threading.Thread(target=del_node_random)
# t2.setDaemon(True)
t2.start()

##########################
## CREATING RANDOM NODE ##
##########################

t3 = threading.Thread(target=create_node, args=[True,])
# t3.setDaemon(True)
t3.start()
