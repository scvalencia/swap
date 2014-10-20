##################################################################
########################### SWAP #################################
##################################################################

A continuacion, se detallaran los pasos para poder iniciar el servidor:

PASO 1:
Instalar la version 2.7.X del interprete escrito en C para el 
lenguaje de programacion Python desde la pagina oficial 
(https://www.python.org/) para el respectivo sistema operativo.
NOTA: Tener cuidado de no descargar la version 3 del interperete,
pues la sintaxis cambia de tal manera que convierte la aplicación
en incompatible. NOTA2: En caso de usar Windows, debera realizar
el agregado respectivo al PATH para poder correr comandos del
interprete Python desde la consola (cmd).

PASO 2:
Instalar Oracle Instant Client versiones Basic y SDK desde la
pagina oficial de Oracle (http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html)
para el respectivo sistema operativo.

PASO 3:
Instalar el gestor de paquetes pip desde la pagina oficial
https://pypi.python.org/pypi/pip, el instalador adicionara
automaticamente las lineas de comando respectivas por lo que usted
no tendra que preocuparse por agregar el PATH respectivo.

PASO 4:
Instalar desde el gestor de paquetes para Python pip, el driver
oficial de Oracle llamado cx_Oracle corriendo desde el terminal
(o cmd en caso de usar Windows), el comando "pip install cx_Oracle",
el gestor realizara de manera automatizada la instalacion, por lo
cual, si ha tenido exito en los pasos anteriores, no deberia de
llegar a tener problema alguno.

PASO 5:
Instalar los paquetes adicionales requeridos para el funcionamiento
de la aplicación los cuales se encuentran alojados en el archivo
requirements.txt, tenga alta precaucion al momento de instalar cada
libreria, pues es de estricta necesidad que las versiones a instalar
sean las mismas que plantea el archivo, de lo contario, sera 
imposible que logre correr Swap en su maquina. AYUDA: Para instalar
las librerias, puede usar el gestor de paquetes pip junto a los
comandos install, mayor informacion en la documentacion de pip
ubicada en https://pypi.python.org/pypi/pip.

PASO 6:
Ejecutar desde el terminal (cmd en caso de usar Windows), los comandos
apropiados para llegar a la carpeta de swap (que se deduce ya 
descomprimida previamente) en donde se encuentra el archivo manage.py.

PASO 7:
Ejecutar desde el terminal (cmd en caso de usar Windows), el comando
que inicializa el servidor integrado del framework de desarrollo web
Django, "python manage.py runserver". Si todo es correcto debera
poder correr desde el servidor local en el puerto por default 8000
(localhost:8000).