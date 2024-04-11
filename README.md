# common

Repo para incluir todo codigo comun entre nuestras apps.



## Instalacion local

Para realizar pruebas se puede instalar el paquete en nuestro local:

```bash
pip install .
```

y luego importarlo en nuestros archivos `.py`. Ej:

```python
from common.connection import Connection
```



## Uso en otros repos

Se puede instalar el paquete usando `pip` de la siguiente forma (TODO: Averiguar si nos sirve el flag `-e` en el install):

```bash
pip install git+https://github.com/Trabajo-profesional-grupo-21/common.git@0.0.1#egg=common
```

En este caso estamos instalando la version `0.0.1` del paquete. Para instalar otra version simplemente hay que modificar luego del `@`.



Para incluirlo en nustros proyectos que corren con docker es el mismo procedimiento que instalar cualquier otro paquete (debemos instalar git en el dockerfile). Ej de un Dockerfile que instala nuestro paquete:

```
FROM python:3.9.7-slim

RUN apt-get update && apt-get install -y git
RUN pip install --upgrade pip
RUN pip3 install git+https://github.com/Trabajo-profesional-grupo-21/common.git@0.0.1#egg=common

COPY / /
CMD ["python3", "./main.py"]
```



Luego para usar importar el modulo en el codigo:

```python
from common.connection import Connection
```



## Agregar cambios

TODO