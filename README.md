shouts-stats-t
==============

Jugando con la API de tardinga

Antes de que lo digan... ya lo sé: código feo
Quizás lo vaya mejorando


1 ) Utilizar primero shoutgraph.py

python shoutgraph.py archivodeacciones.csv [nickname]

Si no usan el parámetro "nickname", por defecto utilizará el mío, linces ibéricos del Himalaya
;)


2 ) ... y luego stats.py

python stats.py archivodeacciones.csv R L


Hace un conteo de likes y reshouts en cada shouts, y arma
- un TOP-R con los reshouts por usuario
- y un TOP-L con los likes por usuario
