import os, random, threading, subprocess, sys


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


########################
## ADDING CHORD NODES ##
########################

tbits = pow(2, m)
rd = random.randint(int(tbits * 2 / 3), tbits) # generate a random amount of active nodes

def create_node():
    subprocess.call(["python3", "chord.py"])

total_amount = 0
for i in range(0, rd):
    t = threading.Thread(target=create_node)
    t.start()
    total_amount += 1

print(f'Se agregaron {total_amount} nodos.')


####################
## UPDATING TABLE ##
####################

t = threading.Thread(target=os.system('python3 update_tables.py'))
t.start()

