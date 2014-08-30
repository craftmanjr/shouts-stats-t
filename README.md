shouts-stats-t
==============

Jugando con la API de tardinga

Antes de que lo digan... ya lo sé: código feo
Quizás lo vaya mejorando


1 ) Utilizar primero shoutgraph.py

python shoutgraph.py archivodeacciones.csv

IMPORTANTE: Cambiar el valor de la variable USERID_CRAFTMANJR (en shoutgraph.py) por el userid que quieras.


2 ) ... y luego stats.py

python stats.py archivodeacciones.csv R L


Hace un conteo de likes y reshouts en cada shouts, y arma
- un TOP-R con los reshouts por usuario
- y un TOP-L con los likes por usuario
