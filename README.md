# Tarea de Sistemas distribuidos

#### Implementacion de Chord
##### Yasmin Cisneros Cimadevila C411

La biblioteca usada fue:
Pyro5==5.12

Para una previa instalación de la misma en caso de no tenerla:

> pip3 install -r requirements

Para ejecutar el código inicialmente se debe de levantar el servidor:

> python3 server.py

Para revisar que el servidor se encuentre en orden y las tablas esten en el estado correcto:

> python3 update.py

Para añadir un nodo nuevo al sistema chord se ejecuta:

> python3 chord.py

Para realizar la búsqueda de un cliente se ejecuta:

> python3 client.py

Para ver el estado de la finger-table ejecute:

> python3 check_finger_table.py