# Descripción

ReFrame es un poderoso framework que permite escribir pruebas de regresión, específicamente dirigido a sistemas HPC. El objetivo de este framework es abstraer la complejidad de las interacciones con el sistema, separando la lógica de una prueba de los detalles de bajo nivel.

Para obtener más información, consulte la documentación oficial de [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/).

# Instalación

Para instalar ReFrame, ejecute el comando:

    [t.800@yoltla ~]$ spack install reframe +docs +gelf

:::: note
::: title
:::

La instalación de ReFrame puede tomar varios minutos.
::::

Puede verificar la instalación de ReFrame utilizando el comando:

    [t.800@yoltla ~]$ spack find reframe
    ==> 1 installed package
    -- linux-centos6-ivybridge / gcc@7.2.0 --------------------------
    reframe@3.9.2

Para obtener más información, consulte la sección [Getting the Framework](https://reframe-hpc.readthedocs.io/en/stable/started.html#getting-the-framework) de la documentación oficial de ReFrame.

# Configuración

ReFrame viene con una configuración genérica mínima que le permite ejecutarse en cualquier sistema, sin embargo, con el fin de que ReFrame funcione de manera correcta y en conjunto con el sistema de colas del clúster Yoltla, crearemos nuestra propia configuración.

Primero, cree el directorio *reframe*:

    [t.800@yoltla ~]$ mkdir reframe

y dentro de este directorio cree el archivo [*settings.py*](attachment$reframe/settings.py):

:::: formalpara
::: title
settings.py
:::

``` python
# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# Configuration Reference:  https://reframe-hpc.readthedocs.io/en/stable/config_reference.html?highlight=logging#configuration-reference
#
# SPDX-License-Identifier: BSD-3-Clause
#
# Yoltla settings
#
# rfmdocstart: site-configuration
site_configuration = {
.
.
.
}
```
::::

Para indicarle a ReFrame que utilice esta nueva configuración debe usar el comando `reframe` siguiendo el formato:

    reframe -C reframe/settings.py [OPCIONES] COMANDO

De forma alternativa, puede crear un `alias` para el comando `reframe`:

    alias reframe="reframe -C /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/reframe/settings.py"

y trabajar del modo usual:

    reframe [OPCIONES] COMANDO

Para obtener más información, consulte la sección [Configuring ReFrame for Your Site](https://reframe-hpc.readthedocs.io/en/stable/configure.html#configuring-reframe-for-your-site) de la documentación oficial de ReFrame.

# Cargar módulo

Para utilizar ReFrame, primero cargue el módulo de Python:

    [t.800@yoltla ~]$ module load python-3.8.12-gcc-7.2.0-2m4osxg

y posteriormente el módulo de ReFrame:

    [t.800@yoltla ~]$ module load reframe-3.9.2-gcc-7.2.0-zejkyvw

# Autocompletado

Para habilitar el autocompletado de ReFrame en el shell, ejecute el comando:

    . spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-zejkyvwz2r3jxv7fsbtialrt5ncdnyib/share/completions/reframe.bash

Para obtener más información, consulte la sección [Enabling auto-completion](https://reframe-hpc.readthedocs.io/en/stable/started.html#enabling-auto-completion) de la documentación oficial de ReFrame.

# Repositorio

El cluster Yoltla cuenta con un repositorio dedicado a ReFrame. En este repositorio se encuentran los archivos de configuración de ReFrame, así como scripts de benchmarks y aplicaciones. Para acceder al repositorio, ingrese a la URL:

    https://github.com/LSVP-UAMI/reframe/

## Descargar

Cargue el módulo de Git:

    [t.800@yoltla git]$ module load git/2.22

y clone el repositorio :

    [t.800@yoltla git]$ git clone git@github.com:LSVP-UAMI/reframe.git

Esto creará un nuevo directorio llamado *reframe*:

    [t.800@yoltla git]$ ls
    reframe

:::: warning
::: title
:::

Asegurese de tener configuradas y actualizadas sus llaves ssh, de lo contrario recibirá el siguiente error:

    [t.800@yoltla git]$  git clone git@github.com:LSVP-UAMI/reframe.git
    Clonando en 'reframe'...
    git@github.com: Permission denied (publickey).
    fatal: No se pudo leer del repositorio remoto.

    Por favor asegúrese que tiene los permisos de acceso correctos
    y que el repositorio existe.
::::

## Estructura

A continuación se presenta la estructura general del repositorio reframe:

    reframe
    ├── conf
    │   ├── settings.py
    │   └── topology
    ├── examples
    └── scripts
        ├── apps
        │   ├── Gaussian
        │   ├── Gromacs
        │   ├── Lammps
        │   ├── Namd
        │   ├── NWChem
        │   └── QuantumEspresso
        ├── benchmarks
        │   ├── hpcg
        │   └── hpl
        └── microbenchmarks
            ├── disk
            │   ├── diskread
            │   └── diskwrite
            ├── memory
            │   ├── memtester
            │   └── stream
            ├── nas
            │   └── ft
            └── osu
                ├── bandwidth
                └── latency

Para obtener más información del contenido de estos directorios, consulte la sección correspondiente.
