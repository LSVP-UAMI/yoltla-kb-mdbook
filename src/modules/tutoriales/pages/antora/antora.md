# Antora

## Requisitos previos

Antes de comenzar, es indispensable instalar y configurar las siguientes aplicaciones:

- [Docker](https://docs.docker.com/engine/install/)

- [Docker Compose](https://docs.docker.com/compose/install/)

## Clonar el repositorio

Clone el repositorio en el que se encuentra la configuración de Antora:

```bash 
$ git clone git@github.com:LSVP-UAMI/yoltla-antora.git
```

Navegue al directorio raíz del repositorio:

```bash
$ cd yoltla-antora/
```

y cambie a la rama `develop`:

```bash
$ git checkout develop
```

## Token y UI

```bash
yoltla-antora
├── docker-compose.yml
├── images
│   ├── build_antora.sh
│   └── Dockerfile.antora
├── README.md
├── token           (1)
└── volumes
    ├── yoltla_docs
    │   ├── antora-playbook.yml
    │   └── ui      (2) 
    └── yoltla_kb
        ├── antora-playbook.yml
        └── ui      (2) 
```

1. En este directorio debe colocar el archivo *.git-credentials*. [Private Repository Authentication](https://docs.antora.org/antora/2.3/playbook/private-repository-auth/).

2. En cada directorio debe colocar el archivo *ui-bundle.zip* correspondiente. [Build a UI Project for Local Preview](https://docs.antora.org/antora-ui-default/build-preview-ui//).

## Construir la imágen

Desde el directorio raíz del repositorio, navegue al directorio *images*:

```bash
$ cd images/
```

y ejecute el comando:

```bash
$ bash build_antora.sh
```

Debe obtener una salida como la siguiente:

```bash
Sending build context to Docker daemon  3.072kB
Step 1/3 : FROM antora/antora:2.3.4
2.3.4: Pulling from antora/antora
cbdbe7a5bc2a: Pull complete
338e24a1fcf8: Pull complete
68c2b1f63a50: Pull complete
70840f95d8e3: Pull complete
dd2944a52c09: Pull complete
d7f25dad5955: Pull complete
b6a6a8ad6971: Pull complete
Digest: sha256:8386785d53ef6307eb704cd6d20f5663207dd9151c3bb69837b0f87be6c15e72
Status: Downloaded newer image for antora/antora:2.3.4
 ---> 137a5b66917b
Step 2/3 : WORKDIR /antora
 ---> Running in f0d7708f164c
Removing intermediate container f0d7708f164c
 ---> f43b00fae5c8
Step 3/3 : RUN yarn global add http-server
 ---> Running in e748b5f3af38
yarn global v1.22.4
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Installed "http-server@0.12.3" with binaries:
      - http-server
      - hs
Done in 10.45s.
Removing intermediate container e748b5f3af38
 ---> 6b932c8ee038
Successfully built 6b932c8ee038
Successfully tagged antora/server:latest
```

## Iniciar servidor web

Desde el directorio raíz, ejecute el comando:

```bash
$ docker-compose up -d
```

Debe obtener una salida como la siguiente:

```bash
Creating network "yoltlaantora_default" with the default driver
Creating yoltla_docs ... done
Creating yoltla_kb   ... done
```

## Construir el sitio web

Para construir el sitio web es necesario conectarse al contenedor de Antora por medio 
de su ID. Para obtener el ID del contenedor, ejecute el comando:

```bash
$ docker ps | grep antora
```

Debe obtener una salida similar a la siguiente:

```bash
CONTAINER ID   IMAGE           COMMAND                  CREATED              STATUS              PORTS                                   NAMES
f40410989c1e   antora/server   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3034->80/tcp, :::3034->80/tcp   yoltla_docs
382555c8ab71   antora/server   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3036->80/tcp, :::3036->80/tcp   yoltla_kb
```

Para conectarse al contenedor ejecute el comando:

```bash
$ docker exec -it <CONTAINER ID> ash
```

Una vez que se ha accedido al contenedor ejecute el comando:

```bash
/antora # antora antora-playbook.yml
```

Debe obtener la siguiente salida:

```bash
[clone] git@github.com:LSVP-UAMI/yoltla-docs.git [#################################]
```

Para salir del contenedor ejecute el comando:

```bash
/antora # exit
```

## Ingresar al sitio

Para acceder a Yoltla Documentación, ingrese a la URL:

```bash
http://localhost:3034/
```

Para acceder a Yoltla Knowledge Base, ingrese a la URL:

```bash
http://localhost:3036/
```

## Detener el servidor web

Desde el directorio raíz, ejecute el comando:

```bash
$ docker-compose down
```

Debe obtener la siguiente salida:

```bash
Stopping yoltla_docs ... done
Stopping yoltla_kb   ... done
Removing yoltla_docs ... done
Removing yoltla_kb   ... done
Removing network yoltlaantora_default
```