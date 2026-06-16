# Taller de administración de Slurm

## Introducción

Notas para curso de instalación y configuración de slurm dado el 28 de diciembre de 2020.

## Objetivos

- Instalar y configurar un cluster slurm básico de tres nodos.

- Realizar pruebas de funcionamiento.

## Antecedentes de Slurm

slurm es un sistema manejador de clusters linux y planificador de jobs:

- Código abierto.

- Tolerante a fallas.

- Escalable.

Sus principales funciones:

- Asigna recursos de cómputo a usuarios por cierto tiempo.

- Proporciona mecanismos para iniciar y monitorear trabajos.

- Lidia con la contención de recursos al manejar una cola de trabajos pendientes.

## Arquitectura

Los componentes de slurm:

- Un demonio central (slurmctld)

- Un demonio para la base de datos (slurmdbd)

- Varios demonios para autenticación (munged)

- Varios demonio ejecutándose en cada nodo de cómputo (slurmd)

## Instalación de slurm

- Requisitos previos

- Instalación de munge

- Compilación de slurm

- Configuración de slurm

### Requisitos previos

- Instalar todos los nodos

- Deshabilitar SElinux

- Configuración del nodo maestro como gateway

- Configuración de llaves

- Sincronizar hora

- Sincronización de usuarios

<span style="color: #990819;">*Para instalar todos los nodos*</span> 

Se deja como ejercicio

<span style="color: #990819;">*Para deshabilitar Selinux*</span> 
```bahs
sed -i 's/^SELINUX=. /SELINUX=disabled/' /etc/sysconfig/selinux
setenforce 0
getenforce
```

```admonish tip title=" "
También se puede deshabilitar desde la instalación de los nodos pasando la
opción al kernel

    selinux=0
```

<span style="color: #990819;">*Example 1. Para configurar el nodo maestro como gateway*</span> 

Asumiendo que el nodo maestro tiene dos interfaces de red

- **eth0** : Salida a los nodos de cómputo

- **eth1** : salida a internet

Se ejecutan los siguientes comandos
```bash
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
```

<span style="color: #990819;">*para crear configurar las llaves*</span> 

```bash
ssh-keygen
ssh-copy-id localhost
```

```admonish important title=" "
Las llaves se deben copiar a todos los nodos del cluster
```

<span style="color: #990819;">*Para sincronizar la hora*</span> 

Se debe iniciar y habilitar el servicio chrony
```bash
systemctl start  chronyd
systemctl enable chronyd
```

```admonish important title=" "
El servicio chrony se debe habilitar en todos los nodos
```

<span style="color: #990819;">*Para sincronizar de cuentas*</span> 

Se deben copiar los archivos /etc/passwd, /etc/shadow, /etc/group
```bash
clush -v -w z[1-2] --copy --dest=/etc /etc/{passwd,shadow,group}
```


### Instalación de munge

Munge es el mecanismo predeterminado para la autenticación
utilizado por Slurm para la ejecución de los trabajos
en los nodos de cómputo.

Las credenciales Munge generadas por Slurm son encriptadas por una
llave estas credenciales son validas por un
periodo de tiempo dado **TTL** (default 300 seg, máximo 1hr)

Munge debe instalarse y habilitarse en todos los nodos del cluster.

```admonish note title=" "
El periodo TTL es la principal razón para sincronizar los relojes de
los nodos del cluster.
```

```admonish important title=" "
La llave munge debe ser la misma en todos los nodos del cluster.
```

<span style="color: #990819;">*Para instalar munge*</span> 

```bash
dnf -y install munge
```

```admonish note title=" "
Para las distribuciones CentOS munge está en el repositorio **epel**
```

```admonish note title=" "
Durante la instalación se crea automáticamente el usuario y grupo munge.
```

```admonish important title=" "
Durante la instalación **NO** se genera la **llave**, esta debe ser generada manualmente.
```

<span style="color: #990819;">*Para generar la llave munge*</span> 

La llave munge es un archivo regular que se puede crear como uno quiera pero se recomienda
usar el comando

```bash
create-munge-key
```

```admonish important title=" "
Este archivo debe tener permisos 0600, propietario y grupo munge
```

```admonish note title=" "
Una vez creada se debe propagar la llave
```

<span style="color: #990819;">*Para probar munge*</span> 

```bash
#generar credencial encriptada a STDOUT
munge --no-input

#encriptar / des-encriptar credencial
munge --no-input | unmunge

#encriptar con tiempo de vida de la credencial 5 segundos
munge --ttl=5 --no-input --output=file.cred ; sleep 10 ; unmunge --input=file.cred

#encriptar en un nodo, des-encriptar en otro
munge --no-input | ssh z1 unmunge
munge --no-input | clush -b -w z[1-2] unmunge
```


### Compilación de Slurm

Compilaremos los componentes
\* slurmd
\* slurmctld
\* slurmdbd

<span style="color: #990819;">*Paquetes requeridos y recomendados*</span> 

- \"Development tools\"

- rpm-build

- perl

- perl-Switch

- munge-devel

- mysql-devel

- pam-devel

- freeipmi-devel

- libibmad-devel

- libibumad-devel

- rrdtool-devel

- ncurses-devel

- numactl-devel

- libssh2-devel

- readline-devel

- libssh2-devel

<span style="color: #990819;">*Para instalar los paquetes*</span> 

```bash
dnf group install "Development tools"
dnf -y install rpm-build perl perl-Switch \
        munge-devel mysql-devel pam-devel freeipmi-devel \
        libibmad-devel libibumad-devel rrdtool-devel ncurses-devel \
        numactl-devel libssh2-devel readline-devel
```

```admonish note title=" "
Se deben habilitar los repositorios **powertools** y **epel** para
estas instalaciones
```

<span style="color: #990819;">*Para descargar y compilar el código fuente*</span> 

```bash
wget https://download.schedmd.com/slurm/slurm-20.11.2.tar.bz2
rpmbuild -ta slurm*.tar.bz2
```

Este comando genera paquetes rpm dentro de la carpeta

```bash
/root/rpmbuild/RPMS/x86_64
```

```admonish note title=" "
Para hacer una compilación más cuidadosa y seleccionar manualmente
los plugins y sus dependencias se requiere compilar mediante autotools
como se explica en <https://slurm.schedmd.com/quickstart_admin.html>
```


### Instalación de Slurm

<span style="color: #990819;">*Para instalar archivos del nodo maestro*</span> 

```bash
rpm -ivh \
slurm-*.rpm
```

<span style="color: #990819;">*Para instalar los paquetes en nodos de computo*</span> 

```bash
rpm -ivh \
slurm-20*.rpm \
slurm-slurmd-20*.rpm \
slurm-pam_slurm-20*.rpm
```

Es recomendable que los demonios slurm se ejecute con su propio usuario

```bash
useradd slurm
```

Slurm requiere varios archivos y directorios auxiliares que deben crearse manualmente

<span style="color: #990819;">*Para crear los directorios y archivos que requiere slurm*</span> 

```bash
mkdir -p \
    /var/run/slurm \
    /var/spool/slurm/slurm \
    /var/spool/slurm/log \
    /var/lib/slurmd

touch   /var/lib/slurmd/node_state \
        /var/lib/slurmd/front_end_state \
        /var/lib/slurmd/job_state \
        /var/lib/slurmd/resv_state \
        /var/lib/slurmd/trigger_state \
        /var/lib/slurmd/assoc_mgr_state \
        /var/lib/slurmd/assoc_usage \
        /var/lib/slurmd/qos_usage \
        /var/lib/slurmd/fed_mgr_state
```

<span style="color: #990819;">*Para darle los permisos correctos*</span> 

```bash
chown -R slurm:slurm /var/*/slurm*
```


## Configuración de slurm

Utilizaremos el configurador básico en linea de slurm
<https://slurm.schedmd.com/configurator.easy.html>

El resultado sin opciones comentadas para el cluster zulu es

```bash
SlurmctldHost=zulu
SlurmUser=slurm
MpiDefault=pmi2
ReturnToService=1
SwitchType=switch/none
TaskPlugin=task/affinity
ProctrackType=proctrack/linuxproc
SlurmctldPidFile=/var/run/slurmctld.pid
SlurmdPidFile=/var/run/slurmd.pid
SlurmdSpoolDir=/var/spool/slurm
StateSaveLocation=/var/spool/slurm

# LOGGING AND ACCOUNTING
SlurmctldLogFile=/var/spool/slurm/log/slurmctld.log
SlurmdLogFile=/var/spool/slurm/log/slurmd.log
JobAcctGatherType=jobacct_gather/linux
#AccountingStorageType=accounting_storage/slurmdbd
ClusterName=zulu

# SCHEDULING
SchedulerType=sched/backfill
SelectType=select/cons_tres
SelectTypeParameters=CR_Core

# COMPUTE NODES
NodeName=z[1-2] CPUs=1 RealMemory=100 Sockets=1 CoresPerSocket=1 ThreadsPerCore=1 State=UNKNOWN
PartitionName=zulu-shaka Nodes=z[1-2] Default=YES MaxTime=01-00:00:00 State=UP
```

Este archivo debe guardarse en /etc/slurm/slurm.conf
y debe compartirse con el resto de los nodos

```bash
clush -v -w z[1-2] --copy --dest=/etc /etc/slurm/slurm.conf
```

<span style="color: #990819;">*Para probar las configuraciones en el nodo maestro*</span> 

```bash
slurmctld -Dvvv
```

<span style="color: #990819;">*Para probar las configuraciones en un nodo de cómputo*</span> 

```bash
slurmd -Dvvv
```


## Para configurar slurmdbd

Se instala una base de datos mysql

```bash
dnf install -y mysql-server
```

Se inicia el servicio

```bash
systemctl start mysqld
```

Se crea una base de datos, un usuario y un password

```bash
mysql> CREATE DATABASE slurm_acct_db;
mysql> CREATE USER 'slurm'@'localhost' IDENTIFIED BY 'slurm.password';
```

se edita el archivo de ejmplo slurmdbd.conf.example para agregar los datos de acceso


## Comandos de usuario slurm

- sinfo

- squeue

- srun

- sbatch

<span style="color: #990819;">*Para lanzar un job*</span> 

```bash
srun -n  2 hostname
sbatch job.slrm
```


## Comandos de administrador slurm

- scontrol

- sacctmgr

<span style="color: #990819;">*Para crear un usuario*</span> 

Se debe crear una cuenta y luego un usuario

```bash
sacctmgr -i create account name="CN_USER" description="CN_DESC" organization="ORG" parent="CP_USER"
sacctmgr -i create user name="CN_USER" defaultaccount="CN_USER" Fairshare=parent
```

<span style="color: #990819;">*Para dar de baja un nodo*</span> 

```bash
scontro update nodename=z1 state down reason="prueba"
```

<span style="color: #990819;">*Para crear una reservación*</span> 

```bash
scontrol create reservation=pruebas duration=1-0 partitionname=zulu-shaka accounts=edra starttime=now nodes=
```


## Lugares de interés

Toda la documentación de la versión de SLURM instalada puede consultarse
en:

**/usr/share/doc/slurm-17.11.4/html/slurm.html**

Documentación slurm
<https://slurm.schedmd.com/documentation.html>
