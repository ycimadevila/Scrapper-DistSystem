# Trabajo de Curso. Sistemas distribuidos

## Scrapper Distribuido
### Integrantes:
### Yasmin Cisneros Cimadevila C411
### Jessy Gigato Izquiedo C411
\
\
Las bibliotecas usadas fueron:
Pyro5==5.12
psutil==5.8.0

Para una previa instalación de la misma en caso de no tenerla:

> pip3 install -r requirements


\
\
Pasos para iniciar el servidor que implementa el algoritmo de chord

\
Para ejecutar el código inicialmente se debe de levantar el servidor:

> python3 server.py m

donde 'm' representa la contidad de bits para el sistema chord

\
Para agregar una cantidad aleatoria de nodos al sistema distribuido:

> python3 main.py m

\
Para realizar la búsqueda de un cliente se ejecuta:

> python3 client.py 

\
Para ver el estado de la finger-table ejecute:

> python3 check_finger_table.py