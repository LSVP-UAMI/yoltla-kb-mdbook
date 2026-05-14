# Requisitos previos

Para agregar un nuevo tutorial a Yoltla Knowledge Base

# Clonar el repositorio

Clone el repositorio en el que se encuentra la configuración de Antora:

```bash
$ git clone https://github.com/LSVP-UAMI/yoltla-kb.git
```

Navegue al directorio raíz del repositorio:

```bash
$ cd yoltla-kb/
```

y cambie a la rama `develop`:

```bash
$ git checkout develop
```

Navegue al directorio de tutoriales

``` bash
$ cd docs/modules/tutoriales/pages
```

Agregue un nuevo archivo adoc y suba los cambios.

``` bash
$ vim nuevo_tutorial.adoc
```

modifique el archivo de navegtación para agregar el nuevo archivo

``` bash
$vim ../nav.adoc
```

Suba los cambios

``` bash
$ git add nuevo_tutorial.adoc
$ git add ../nav.adoc
$ git commit -m "nuevo_tutorial"
$ git push
```

# Actualizar el sitio web

Para actualizar el sitio web es necesario conectarse al contenedor de Antora por 
medio de su ID. Para obtener el ID del contenedor, ejecute el comando:

```bash
$ docker ps
```

Debe obtener una salida similar a la siguiente:

```bash
CONTAINER ID   IMAGE           COMMAND                  CREATED              STATUS              PORTS                                   NAMES
f40410989c1e   antora/server   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3034->80/tcp, :::3034->80/tcp   yoltla_docs
382555c8ab71   antora/server   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3036->80/tcp, :::3036->80/tcp   yoltla_kb
```

Para conectarse al contenedor ejecute el comando:

```bash
$ docker exec <CONTAINER ID>  ash -c "antora antora-playbook.yml"
```

Debe obtener la siguiente salida:

```bash
[clone] git@github.com:LSVP-UAMI/yoltla-docs.git [#################################]
```

Para salir del contenedor ejecute el comando:

```bash
/antora # exit
```
