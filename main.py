import os, random, threading, subprocess

while True:
    try:
        m = int(input())
        if m < 1:
            raise TypeError()
        break
    except TypeError:
        print("La entrada debe ser un entero positivo mayor que 1")

tbits = pow(2, m)
rd = random.randint(int(tbits * 2 / 3), tbits) # generate a random amount of active nodes

def create_node():
    subprocess.call(["python3", "chord.py"])

total_amount = 0
for i in range(0, rd):
    t = threading.Thread(target=create_node)
    t.start()
    print("hello bitch")
    total_amount += 1

print(f'Se agregaron {total_amount} nodos.')

# t = threading.Thread(target=os.system('python3 update_tables.py'))
# t.start()

