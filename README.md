# Trabajo de Curso. Sistemas distribuidos

## Scrapper Distribuido
### Integrantes:
### Yasmin Cisneros Cimadevila C411
### Jessy Gigato Izquiedo C411
\
\
Las bibliotecas usadas fueron:
\
Pyro5==5.12
\
psutil==5.8.0

Para una previa instalación de la misma en caso de no tenerla:

> pip3 install -r requirements

\
\
Pasos para iniciar el servidor que implementa el algoritmo de chord

\
Para ejecutar el código inicialmente se debe de levantar el servidor y el router:

> python3 main.py

Debe de esperar hasta que la terminal le diga que el servicio esta listo. 

\
Para agregar nodos de forma aleatoria al sistema distribuido (cada uno de los nodos ejecutarlos en una termnal diferente):

> python3 server.py add-chord

\
Para realizar la búsqueda  de la URL se ejecuta:

> python3 server.py scrap URL

Donde dice URL debe ser sustituido por la URL a buscar (e.g. https://www.twitter.com)