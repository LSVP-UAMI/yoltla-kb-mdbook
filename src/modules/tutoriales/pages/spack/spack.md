# Descripción

Spack es una herramienta de administración de paquetes diseñada para soportar múltiples versiones y configuraciones de software en una amplia variedad de plataformas y entornos.

Para obtener más información, consulte la documentación oficial de [Spack](https://spack.readthedocs.io/en/latest/).

# Descarga

Cargue el módulo de Git:

    [t.800@yoltla ~]$ module load git/2.22

y clone el repositorio de github de [Spack](https://github.com/spack/spack):

    [t.800@yoltla ~]$ git clone -c feature.manyFiles=true https://github.com/spack/spack.git

Esto creará un nuevo directorio llamado *spack*:

    [t.800@yoltla ~]$ ls
     spack

:::: warning
::: title
:::

Si no carga el módulo de Git, obtendrá el siguiente mensaje:

    [t.800@yoltla ~]$ git clone -c feature.manyFiles=true https://github.com/spack/spack.git
    error: unknown switch `c'
    usage: git clone [options] [--] <repo> [<dir>]
    .
    .
    .
::::

# Configuración del shell

Cargue el módulo de Python:

    [t.800@yoltla ~]$ module load python/conda/3.6

y ejecute el comando:

    [t.800@yoltla ~]$ . spack/share/spack/setup-env.sh

Esto configurará su *PATH* para poder utilizar el comando `spack`.

:::: warning
::: title
:::

Si no carga el módulo de Python, obtendrá el siguiente mensaje:

    [t.800@yoltla ~]$ . spack/share/spack/setup-env.sh
    Spack requires Python 2.7 or 3.5 or higher You are running spack with Python 2.6.6.
::::

Para obtener más información, consulte la sección [Shell support](https://spack.readthedocs.io/en/latest/getting_started.html#shell-support) de la documentación oficial de Spack.

# Spack scope

Por defecto, Spack cuenta sus propios archivos de configuración, sin embargo, nosotros queremos proveerle de una configuración personalizada. Todos los archivos de nuestra configuración los colocaremos en un nuevo directorio llamado *spack_scope*.

Primero, cree la siguiente estructura de directorios:

    spack_scope
    ├── deps
    ├── lmod
    ├── module
    └── stage

Posteriormente, dentro del directorio *spack_scope*, cree los archivos *config.yaml*:

:::: formalpara
::: title
config.yaml
:::

    config:
      install_tree:
        root: /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope/deps
      module_roots:
        tcl:  /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope/module
        lmod: /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope/lmod
      build_stage: /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope/stage
::::

y *bootstrap.yaml*:

:::: formalpara
::: title
bootstrap.yaml
:::

    bootstrap:
      root: /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/.spack/bootstrap
::::

Finalmente, copie los archivos *compilers.yaml* y *packages.yaml*, ubicados en el directorio:

    ~spack/spack/spack-0.17.0/etc/spack/

al directorio *spack_scope*:

    [t.800@yoltla ~]$ cp ~spack/spack/spack-0.17.0/etc/spack/compilers.yaml spack_scope
    [t.800@yoltla ~]$ cp ~spack/spack/spack-0.17.0/etc/spack/packages.yaml spack_scope

El contenido del directorio *spack_scope* debe ser el siguiente:

    spack_scope
    ├── bootstrap.yaml
    ├── compilers.yaml
    ├── config.yaml
    ├── deps
    ├── lmod
    ├── module
    ├── packages.yaml
    └── stage

    4 directories, 4 files

Para indicarle a Spack que utilice esta nueva configuración debe usar el comando `spack` siguiendo el formato:

    spack -C spack_scope [OPCIONES] COMANDO

De forma alternativa, puede crear un `alias` para el comando `spack`:

    alias spack="spack -C /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope"

y trabajar del modo usual:

    spack [OPCIONES] COMANDO

Para obtener más información, consulte la sección [Configuration Scopes](https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes) de la documentación oficial de Spack.

# Clingo

Spack usa *clingo* para encontrar las versiones óptimas y variantes de dependencias al instalar un paquete. Dado que *clingo* en sí es un binario, Spack debe instalarlo la primera vez que se utilice, lo que se denomina bootstrapping.

Para instalar *clingo*, cargue el módulo de GCC:

    [t.800@yoltla ~]$ module load gcc/7.2.0

y concretice (*concretize*) una especificación (*spec*):

    [t.800@yoltla ~]$ spack spec zlib
    Input spec
    --------------------------------
    zlib

    Concretized
    --------------------------------
    ==> Bootstrapping clingo from pre-built binaries
    ==> buildcache spec(s) matching /vcipwnf57slgoo7busvvkzjkk7vydeb5

    ==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.1/build_cache/linux-rhel5-x86_64/gcc-9.3.0/clingo-bootstrap-spack/linux-rhel5-x86_64-gcc-9.3.0-clingo-bootstrap-spack-vcipwnf57slgoo7busvvkzjkk7vydeb5.spack
    ==> Installing buildcache for spec clingo-bootstrap@spack%gcc@9.3.0~docs~ipo+python build_type=Release arch=linux-rhel5-x86_64
    ==> Bootstrapping patchelf from pre-built binaries
    ==> Installing patchelf-0.13.1-ekx3bivpcwktizxe5jfsnppm52t2kkc2
    ==> No binary for patchelf-0.13.1-ekx3bivpcwktizxe5jfsnppm52t2kkc2 found: installing from source
    ==> Fetching https://github.com/NixOS/patchelf/releases/download/0.13.1/patchelf-0.13.1.tar.gz
    ==> No patches needed for patchelf
    ==> patchelf: Executing phase: 'autoreconf'
    ==> patchelf: Executing phase: 'configure'
    ==> patchelf: Executing phase: 'build'
    ==> patchelf: Executing phase: 'install'
    ==> patchelf: Successfully installed patchelf-0.13.1-ekx3bivpcwktizxe5jfsnppm52t2kkc2
      Fetch: 1.98s.  Build: 29.94s.  Total: 31.92s.
    [+] /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/.spack/bootstrap/store/linux-centos6-x86_64/gcc-7.2.0/patchelf-0.13.1-ekx3bivpcwktizxe5jfsnppm52t2kkc2
    zlib@1.2.11%gcc@7.2.0+optimize+pic+shared arch=linux-centos6-ivybridge

Puede verificar la instalación de *clingo* con el comando:

    [t.800@yoltla ~]$ spack find -b
    ==> Showing internal bootstrap store at "/LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/.spack/bootstrap/store"
    ==> 3 installed packages
    -- linux-centos6-x86_64 / gcc@7.2.0 -----------------------------
    patchelf@0.13.1

    -- linux-rhel5-x86_64 / gcc@9.3.0 -------------------------------
    clingo-bootstrap@spack  python@3.6

:::: warning
::: title
:::

Si no carga el módulo de GCC, obtendrá el siguiente mensaje:

    [t.800@yoltla ~]$ spack spec zlib
    Input spec
    --------------------------------
    zlib

    Concretized
    --------------------------------
    ==> Bootstrapping clingo from pre-built binaries
    ==> buildcache spec(s) matching /vcipwnf57slgoo7busvvkzjkk7vydeb5

    ==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.1/build_cache/linux-rhel5-x86_64/gcc-9.3.0/clingo-bootstrap-spack/linux-rhel5-x86_64-gcc-9.3.0-clingo-bootstrap-spack-vcipwnf57slgoo7busvvkzjkk7vydeb5.spack
    ==> Installing buildcache for spec clingo-bootstrap@spack%gcc@9.3.0~docs~ipo+python build_type=Release arch=linux-rhel5-x86_64
    ==> Bootstrapping patchelf from pre-built binaries
    ==> Bootstrapping clingo from sources
    ==> Error: cannot bootstrap the "clingo" Python module from spec "clingo-bootstrap@spack+python %gcc target=x86_64" due to the following failures:
        'github-actions' raised RuntimeError: cannot bootstrap any of the patchelf executables from spec "patchelf@0.13.1:0.13.99 %gcc target=x86_64"
        'spack-install' raised ConflictsInSpecError: Conflicts in concretized spec "clingo-bootstrap@spack%gcc@4.4.7~docs~ipo+python~static_libstdcpp build_type=Release arch=linux-centos6-x86_64/4vex76p"
    .
    .
    .
::::

Para obtener más información, consulte la sección [Bootstrapping clingo](https://spack.readthedocs.io/en/latest/getting_started.html#bootstrapping-clingo) de la documentación oficial de Spack.

# MODULEPATH

Agregue el directorio *spack_scope/module/linux-centos6-ivybridge* al *MODULEPATH*:

    [t.800@yoltla ~]$ export MODULEPATH="/LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope/module/linux-centos6-ivybridge/:$MODULEPATH"

Esto le permitirá cargar los módulos que se instalen en el directorio *spack_scope* con el comando `module load`.
