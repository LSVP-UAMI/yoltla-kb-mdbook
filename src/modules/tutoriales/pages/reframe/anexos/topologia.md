# Descripción

ReFrame puede detectar automáticamente la topología del procesador de las particiones locales y remotas. La información del procesador se pone a disposición de las pruebas a través de los atributos correspondientes de `current_partition` y permite que una prueba modifique su comportamiento.

Actualmente, ReFrame solo admite la detección automática de la información del procesador local o remota.

Para obtener más información, consulte la sección [Auto-detecting processor information](https://reframe-hpc.readthedocs.io/en/stable/configure.html#auto-detecting-processor-information) de la documentación oficial de ReFrame.

# Detección automática

La detección automática de información del procesador funciona de la siguiente manera:

1.  Si se define la opción `processor` en el archivo de configuración, no se intenta la detección automática.

2.  Si la opción de configuración `processor` no está definida, ReFrame buscará un archivo de metadatos de configuración del procesador en:

        ~/.reframe/topology/{system}-{part}/processor.json

    Si se encuentra el archivo, la información de topología se carga desde allí. Estos archivos son generados automáticamente por ReFrame a partir de ejecuciones anteriores.

3.  Si no se encuentran los archivos de metadatos correspondientes, la información del procesador se detectará automáticamente. Si la partición del sistema es local (es decir: `local` scheduler + `local` launcher), la información del procesador se detecta automáticamente de forma incondicional y se almacena en el archivo de metadatos correspondiente para esta partición. Si la partición es remota, ReFrame no intentará detectarla automáticamente a menos que las opciones de configuración `RFM_REMOTE_DETECT` ó `detect_remote_system_topology` se establezcan. En ese caso, los pasos para autodetectar la información del procesador
    remoto son los siguientes:

    a.  ReFrame crea un clon nuevo de sí mismo en un directorio temporal creado de forma predeterminada. Este prefijo de directorio temporal se puede cambiar configurando la variable ambiental `RFM_REMOTE_WORKDIR`.

    b.  ReFrame cambia a ese directorio e inicia un trabajo que primero iniciará el clon nuevo y luego ejecutará ese clon con:

            {launcher} ./bin/reframe –detect-host-topology=topo.json

        La opción hace que ReFrame detecte la topología del host actual, que en este caso serían los nodos de cómputo remotos.

En caso de errores durante la detección automática, ReFrame simplemente emitirá una advertencia y continuará.

## Cluster Yoltla

Hay dos formas de iniciar el proceso de detección de la topología, en ambas formas ReFrame se ejecutara localmente en las particiones. Revise la variable [`hostnames`](reframe/anexos/archivo_configuracion.xml#configuración_systems) del archivo de configuración.

### **Forma automática**

Para detectar la topología en el cluster de forma automática, se requiere el uso de un archivo de configuración `settings.py` que haga uso de la opción [remote_detect](https://reframe-hpc.readthedocs.io/en/stable/manpage.html#envvar-RFM_REMOTE_DETECT) el cual debe estar presente en `~/.reframe/`. El archivo de
configuración necesario lo puede encontrar [*aquí*](attachment$reframe/topologia/settings.py).

Puede pasar el archivo de configuración con la opción [`-C`](/reframe/scripts/lanzar_pruebas.xml#config)

:::: note
::: title
:::

La opción `remote_detect` tiene conflictos con algunos parámetros de configuración como `use_nodes_option`. Para evitar estos conflictos y que ReFrame busque detectar la topología cada vez que se ejecuta, se recomienda solo usar esta opción cuando sea necesario detectar nuevas topologias.
::::

Despues se lanza una prueba sencilla para que Reframe inicie la detección automática. Este proceso crea las carpetas y archivos de metadatos correspondiente en:

    ~/.reframe/topology/{system}-{part}/processor.json

Para detectar la topología del sistema, Reframe manda un trabajo en cada partición presente en el [archivo de configuración](reframe/anexos/archivo_configuracion.xml#configuración_systems) de la siguiente forma:

``` bash
#!/bin/bash
#SBATCH --job-name="rfm-detect-job"
#SBATCH --ntasks=1
#SBATCH --output=rfm-detect-job.out
#SBATCH --error=rfm-detect-job.err
#SBATCH --partition=q1h-20p

_onerror()
{
  exitcode=$?
  echo "-reframe: command \`$BASH_COMMAND' failed (exit code: $exitcode)"
  exit $exitcode
}

trap _onerror ERR

./bootstrap.sh
srun -np 1 ./bin/reframe --detect-host-topology=topo.json
```

:::: note
::: title
:::

Al lanzar la prueba para la detección automática, se recomienda usar la opción
[`-v`,`–verbose`](/reframe/scripts/lanzar_pruebas.xml#verbose) de la siguiente forma:

    reframe -c hello.py -r -vv
::::

### **Forma manual**

Puede lanzar un trabajo para detectar la topología cargando los entornos necesarios de ReFrame. Un ejemplo del script de SLURM necesario se puede ver en el siguiente ejemplo:

``` bash
#!/bin/bash
#SBATCH --job-name="rfm-detect-job"
#SBATCH --ntasks=1
#SBATCH --output=rfm-detect-job.out
#SBATCH --error=rfm-detect-job.err
#SBATCH --partition=q1h-20p
#SBATCH --time=0:5:0

_onerror()
{
    exitcode=$?
    echo "-reframe: command \`$BASH_COMMAND' failed (exit code: $exitcode)"
    exit $exitcode
}

trap _onerror ERR

export MODULEPATH=$HOME/spack_scope/modules/linux-centos6-ivybridge:"$MODULEPATH"

module purge
module load python-3.8.12-gcc-7.2.0-2m4osxg
module load reframe-3.9.2-gcc-7.2.0-gqmjpwb

srun reframe --detect-host-topology=processor.json -vv
```

El script hace uso de la opción [`--detect-host-topology`](/reframe/scripts/lanzar_pruebas.xml#detect-host-topology) de Reframe para detectar la información.
La topología resultante de la particion `q1h-20p` la puede consultar en el archivo resultante: `processor.json`

:::: note
::: title
:::

Se tiene que crear las carpetas:

    ~/.reframe/topology/{system}-{part}/

manualmente y mover los archivos correspondientes.
::::

# Ejemplos

La siguiente parcialidad de código es un ejemplo del uso de la topología en pruebas de regresión:

``` bash
      @run_before('run')
      def setup_run(self):
          # Se cancela la ejecución si no hay información de la topología en .reframe/topology/[valid_systems]
          self.skip_if_no_procinfo()

          # Se guarda información de la topología en proc
          proc = self.current_partition.processor

          # Se obtiene la arquitectura en arch
          arch = proc.arch

          # Setup parallel run
          self.num_tasks_per_node = proc.num_cores
          self.num_tasks = self.num_nodes * self.num_tasks_per_node
          self.num_tasks_per_core = 1

          # Se redefine como ejecutar el job
          self.executable=f'mpiexec.hydra -bootstrap slurm -np {self.num_tasks} namd2 {self.in_name}'
```

Donde:

`self.current_partition.processor` [¶](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html?highlight=current_partition.processor#reframe.core.systems.SystemPartition.processor)

:   Función que obtiene información del procesador para la partición actual. Esta información la obtiene de
    los archivos presentes de la carpeta `topology`.

`self.skip_if_no_procinfo(msg)` [¶](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html?highlight=skip_if_no_procinfo()#reframe.core.pipeline.RegressionTest.skip_if_no_procinfo)

:   Omite la prueba si no hay información disponible sobre la topología del procesador.

    Este método solo tiene efecto si se llama después de la etapa de `setup()`.

    **Parámetros**

    - **msg**: un mensaje que explica por qué se omitió la prueba. Si no se especifica, se utilizará un mensaje predeterminado.

proc.arch

:   Variable de consulta donde se obtiene información de la arquitectura donde se ejecutara la prueba, las arquitecturas disponibles son:

    - ivybridge: nodos nc

    - haswell: nodos ttv1

    - broadwell: nodos ttv2

    Esto puede ser usado para referirse a las particiones en otros contextos.

proc.num_cores

:   Variable de consulta donde se obtiene la cantidad de cores disponibles en la partición.

Puede ver más opciones en el siguiente [enlace](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html?highlight=num_cores#reframe.core.systems.ProcessorInfo).
