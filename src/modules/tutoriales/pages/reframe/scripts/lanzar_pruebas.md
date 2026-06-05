# Descripción

ReFrame proporciona una interfaz de programación para escribir pruebas de regresión 
y una interfaz de línea de comandos para administrar y ejecutar las pruebas, algunas 
de estas opciones se presentan aquí.

El comando `reframe` es parte de la interfaz de ReFrame. Esta interfaz es responsable 
de cargar y ejecutar pruebas de regresión escritas en ReFrame. ReFrame ejecuta pruebas 
enviándolas a un pipeline bien definido. La implementación de las diferentes etapas de 
este pipeline es parte de la arquitectura central de ReFrame, pero la interfaz es 
responsable de impulsar esta canalización y ejecutar pruebas a través de ella.

Para obtener más información del pipeline y la aquitectura de Reframe, consulte la 
sección [How ReFrame Executes Tests](https://reframe-hpc.readthedocs.io/en/stable/pipeline.html) 
de la documentación oficial de ReFrame.

# Detección y carga de pruebas

- `-c, --checkpath=PATH`

    Opción para proporcionar la ruta donde ReFrame buscara pruebas.

    `PATH` puede ser un directorio o un solo archivo de prueba. Si es un directorio, ReFrame 
    buscará archivos de prueba dentro de este directorio y cargará todas las pruebas que se 
    encuentren en ellos. Esta opción se puede especificar varias veces, en cuyo caso cada 
    `PATH` se buscará en orden.

    Ejemplos:

    Teniendo el siguiente árbol de directorios en /home/:

    ```bash
    [t.800@yoltla ~]$ ls
    Ejemplos logs

    [t.800@yoltla ~]$ ls Ejemplos/
    HolaMundo  PipelineMpi  Slurm_check

    [t.800@yoltla ~]$ tree Ejemplos/
    Ejemplos/
    ├── HolaMundo
    │   ├── hello_test.py
    │   ├── hello_test_MPI.py
    │   ├── logs
    │   └── src
    │       ├── hello.c
    │       └── hello_MPI.c
    ├── PipelineMpi
    │   ├── pipeMpi.py
    │   ├── logs
    │   └── src
    │       ├── Makefile
    │       └── pipelineOrdenamiento.c
    └── Slurm_check
        ├── logs
        └── slurm_check.py
    ```

    Para [ejecutar](#ejecutar) el archivo `pipeMpi.py` pase la ruta del archivo a Reframe, ejemplo:

    ```bash
    reframe -c Ejemplos/PipelineMpi/pipeMpi.py -r
    ```

    ```admonish info title=" "
    Debe existir una carpeta `logs` desde el directorio donde se invoca a Reframe.

    Para más detalles, consulte la sección [Configuración de Logging](../anexos/archivo_configuracion.md#configuración-de-logging).
    ```

    Despues de ejecutar obtendremos las siguientes carpetas:

    ```bash
    [t.800@yoltla ~]$ ls

    Ejemplos  logs  output  stage
    ```

    Para [ejecutar](#ejecutar) los archivos dentro del directorio `HolaMundo` pase la ruta 
    del directorio a Reframe, por ejemplo:

    ```bash
    reframe -c Ejemplos/HolaMundo/ -r
    ```

    ```admonish info title=" "
    Tome en cuenta que se creara un solo archivo [`logs`](#lanzar_pruebas) y una sola 
    carpeta [`output`](#out) y [`stage`](#stage) para todas las pruebas que se encuentre.

    Para más detalles, consulte la sección [Archivo de configuración](../anexos/archivo_configuracion.md).
    ```


- ## --ignore-check-conflicts

    Ignora las pruebas con nombres en conflicto al cargar las pruebas.

    ReFrame requiere que los nombres de las pruebas sean únicos. Esta opción generalmente 
    debe evitarse a menos que haya una razón específica.

- ## -R, --recursive

    Busca archivos de prueba recursivamente en los directorios que se encuentran en la ruta 
    de búsqueda `--checkpath=PATH`.

    Para nuestro ejemplo anterior, si queremos [ejecutar](#ejecutar) todas las pruebas, ejecutamos:

    ```bash
    reframe -c Ejemplos/ -R -r
    ```

    ```admonish info title=" "
    Tome en cuenta que se creara un solo archivo [`logs`](#lanzar_pruebas) y una sola 
    carpeta [`output`](#out) y [`stage`](#stage) para todas las pruebas que se encuentre.

    Para más detalles, consulte la sección [Archivo de configuración](../anexos/archivo_configuracion.md).
    ```


# Filtrado de pruebas

Las pruebas se pueden filtrar por diferentes atributos y existen opciones de línea de 
comandos específicas para lograrlo. Una característica común de todas las opciones de 
filtrado de pruebas es que si se selecciona una prueba, también se seleccionarán todas 
sus dependencias, independientemente de si coinciden o no con los criterios de filtrado. 
Esto sucede de forma recursiva, de modo que si la prueba T1 depende de T2 y T2 depende 
de T3, la selección T1 también seleccionaría T2 y T3.

- ## --cpu-only

    Seleccione pruebas que no estén dirigidas a las GPU.

    Estas son todas las pruebas con `num_gpus_per_node` igual a cero. Esta opción y 
    `--gpu-only` son mutuamente excluyentes.

- ## --failed

    Selecciona solo los casos de prueba fallidos para una ejecución anterior.

    Esta opción solo se puede utilizar en combinación con `--restore-session`. Para volver a 
    ejecutar los casos fallidos de la última ejecución, puede usar `reframe --restore-session --failed -r`.

- ## -n, --name=NAME

    Filtra pruebas por nombre.

    NAME se interpreta como una [expresión regular](https://docs.python.org/3/library/re.html) 
    de Python; se seleccionará cualquier prueba cuyomnombre coincida con NAME.

- ## -T, --exclude-tag=TAG

    Excluir pruebas por etiquetas.

    Esta opción se puede especificar varias veces, en cuyo caso se seleccionarán las pruebas 
    con cualquiera de los nombres especificados: `-n NAME1 -n NAME2` esto equivale a 
    `-n 'NAME1|NAME2'`.

    Para más detalles, consulte la sección [Tags](../scripts/scripts.md#tags).

- ## -t, --tag=TAG

    Filtrar pruebas por etiqueta.

    Esta opción se puede especificar varias veces, en cuyo caso se seleccionarán las pruebas 
    con cualquiera de los nombres especificados: `-n NAME1 -n NAME2` esto equivale a `-n 'NAME1|NAME2'`.

    Para más detalles, consulte la sección [Tags](../scripts/scripts.md#tags).

- ## -x, --exclude=NAME

    Excluir pruebas por nombre. NAME se interpreta como una [expresión regular](https://docs.python.org/3/library/re.html) 
    de Python; se seleccionará cualquier prueba cuyo nombre coincida con NAME.

    Ejemplo:

    ```bash
    reframe -c hello_mpi.py -x HelloTest_8 -r
    ```

# Enlistar y ejecutar pruebas

- ## -L

    Lista las pruebas seleccionadas proporcionando más detalles de cada prueba.

    Ejemplo:

    ```python
    [t.800@yoltla ~]$ reframe -c hello_mpi.py -L

    [ReFrame Setup]
      version:           3.9.2
      command:           '/LUSTRE/home/uam/../../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2/bin/reframe -c hello_mpi.py -l'
      launched by:       t.800@yoltla.supercomputo.izt.uam.mx
      working directory: '/LUSTRE/home/uam/../../Pruebas/parametros'
      settings file:     '/LUSTRE/home/uam/../../t.800/.reframe/settings.py'
      check search path: '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/hello_mpi.py'
      stage directory:   '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/stage/'
      output directory:  '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/output/'

    [List of matched checks]
    - HelloTest_8:
        Description:
          HelloTest_8

        Environment modules:
          <none>

        Location:
          /LUSTRE/home/uam/../../t.800/Pruebas/parametros/hello_mpi.py

        Maintainers:
          <none>

        Node allocation:
          standard (1 task(s) -- may be set differently in hooks)

        Pipeline hooks:
          - pre_run: replace_launcher

        Tags:
          <none>

        Valid environments:
          builtin-openmpi-2.1.5

        Valid systems:
          yoltla:q1h-20p

        Dependencies (conceptual):
          <none>

        Dependencies (actual):
          <none>

    - HelloTest_20:
        Description:
        .
        .
        .
    ```

- ## -l

    Lista las pruebas seleccionadas.

    Ejemplo:

    ``` bash
    [t.800@yoltla ~]$ reframe -c hello_mpi.py -l

    [ReFrame Setup]
      version:           3.9.2
      command:           '/LUSTRE/home/uam/../../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2/bin/reframe -c hello_mpi.py -l'
      launched by:       t.800@yoltla.supercomputo.izt.uam.mx
      working directory: '/LUSTRE/home/uam/../../Pruebas/parametros'
      settings file:     '/LUSTRE/home/uam/../../t.800/.reframe/settings.py'
      check search path: '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/hello_mpi.py'
      stage directory:   '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/stage/'
      output directory:  '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/output/'

    [List of matched checks]
    - HelloTest_20 (found in '/LUSTRE/home/uam/../../c.800/Pruebas/parametros/hello_mpi.py')
    - HelloTest_16 (found in '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/hello_mpi.py')
    - HelloTest_2 (found in '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/hello_mpi.py')
    - HelloTest_8 (found in '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/hello_mpi.py')
    - HelloTest_4 (found in '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/hello_mpi.py')
    Found 5 check(s)

    Log file(s) saved in '/LUSTRE/home/uam/../../t.800/Pruebas/parametro/logs/rfm.out', '/LUSTRE/home/uam/../../t.800/Pruebas/parametro/logs/rfm.log'
    ```

- ## --list-tags

    Enumera las etiquetas únicas de las pruebas seleccionadas.

    Las etiquetas se imprimen en orden alfabético.

    Ejemplo

    ```bash
    [t.800@yoltla ~]$ reframe -c namd.py --list-tags

            .
            .
            .

    [List of unique tags]
    'test-cpu-nc-1-F1atpase', 'test-cpu-nc-1-Stmv', 'test-cpu-nc-16-F1atpase', 'test-cpu-nc-16-Stmv',
    'test-cpu-nc-2-F1atpase', 'test-cpu-nc-2-Stmv', 'test-cpu-nc-4-F1atpase', 'test-cpu-nc-4-Stmv',
    'test-cpu-nc-8-F1atpase', 'test-cpu-nc-8-Stmv', 'test-cpu-ttv1-16-F1atpase', 'test-cpu-ttv1-16-Stmv',
    'test-cpu-ttv1-4-F1atpase', 'test-cpu-ttv1-4-Stmv', 'test-cpu-ttv1-5-F1atpase', 'test-cpu-ttv1-5-Stmv',
    'test-cpu-ttv1-8-F1atpase', 'test-cpu-ttv1-8-Stmv', 'test-cpu-ttv2-16-F1atpase',
    'test-cpu-ttv2-16-Stmv', 'test-cpu-ttv2-2-F1atpase', 'test-cpu-ttv2-2-Stmv',
    'test-cpu-ttv2-4-F1atpase', 'test-cpu-ttv2-4-Stmv', 'test-cpu-ttv2-8-F1atpase', 'test-cpu-ttv2-8-Stmv'

    Found 26 tag(s)

            .
            .
    ```



- ## -r, --run

    Ejecutar las pruebas seleccionadas.

    Cuando una prueba se ejecuta se crean los directorios [`output`](#out) y 
    [`stage`](#stage). Estos directorios contienen las salidas de la pruebas y se 
    sobreescriben en cada ejecución.

    Para más detalles, consulte el siguiente [enlace](https://reframe-hpc.readthedocs.io/en/stable/manpage.html?#cmdoption-o).


# Opciones de control

## Salida

- ### --dont-restaging

    No vuelve a preparar una prueba si su directorio [`stage`](#stage) existe. 
    Normalmente, si existe el directorio de `stage` de una prueba, ReFrame lo 
    eliminará y lo volverá a crear. Esta opción deshabilita este comportamiento.

- ### --keep-stage-files

    Mantiene los directorios [`stage`](#stage) de prueba incluso para las pruebas que 
    finalicen con éxito.

    Esta opción también se puede configurar con la variable de ambiente `RFM_KEEP_STAGE_FILES` 
    o el parámetro `keep_stage_files` del archivo de configuración.

- ### -o, --output=DIR

    Directorio para archivos de salida de la prueba.

    Cuando una prueba finaliza con éxito, ReFrame copia los archivos de salida 
    importantes en un directorio específico de la prueba para referencia futura. Este 
    directorio específico de la prueba tiene el formato:
    
    ```bash
    {output_prefix}/{system}/{partition}/{environment}/{test_name}
    ```

    donde `output_prefix` está establecido por esta opción. Los archivos de prueba 
    guardados en este directorio son los siguientes:

    - El script de compilación generado por ReFrame, si no es una prueba de solo ejecución.

    - La salida estándar y el error estándar de la fase de compilación, si no es una prueba 
    de solo ejecución.

    - El script de trabajo generado por ReFrame, si no es una prueba de solo compilación.

    - La salida estándar y el error estándar de la fase de ejecución, si no es una prueba de 
    solo compilación.

    - Cualquier archivo adicional especificado por el atributo [`keep_files`](../anexos/referencia_api.md#keep_files) 
    de prueba de regresión.

    Esta opción también se puede configurar con la variable de ambiente `RFM_OUTPUT_DIR` o 
    el parámetro `outputdir` del archivo de configuración.

- ### -s, --stage=DIR

   Prefijo del directorio para la preparación de recursos de la prueba.

    ReFrame no ejecuta pruebas desde su directorio de origen original. En su lugar, crea 
    un directorio de estapas (stage) específico por prueba y copia todos los recursos de 
    la prueba allí. Luego cambia a ese directorio y ejecuta la prueba. Este directorio 
    específico de la prueba tiene el formato:

    ```bash
    {stage_prefix}/{system}/{partition}/{environment}/{test_name}
    ```

    donde `stage_prefix` está establecido por esta opción. Si una prueba finaliza con 
    éxito, se eliminará su directorio stage.

    Esta opción también se puede configurar con la variable de ambiente `RFM_STAGE_DIR` 
    o el parámetro `stagedir` del archivo de configuración.

## Envío de trabajos

- ### -J, --job-option=OPTION

   Pasa `OPTION` directamente al backend del programador de trabajos (en este caso Slurm).

    Ejemplo:

    ```bash
    reframe -c hola_mundo.py -J 'exclude=tt[81-88]' -r
    ```

    Esto agregara la siguiente linea al script de trabajo:

    ```bash
    #SBATCH --exclude=tt[81-88]
    ```

# Otras opciones

- ## -C --config-file=FILE

    Usa `FILE` cómo archivo de configuración para ReFrame.

    Esta opción también se puede configurar con la [variable de ambiente](../anexos/archivo_configuracion.md#variables-de-ambiente)
    `RFM_CONFIG_FILE`.

- ## --detect-host-topology=[FILE]

   Detecta la topología del procesador del host local y la guarda en el archivo `FILE`.

    Si no se especifica `FILE`, se utilizará la salida estándar.

- ## -h, --help 

    Imprime un breve mensaje de ayuda.

- ## --performance-report

    Muestra un informe de rendimiento para todas las pruebas de rendimiento que se han 
    ejecutado.

- ## -v, --verbose

    Aumenta el nivel de detalle de la salida. Esta opción se puede especificar varias veces.

- ## --show-config=[PARAM]

    Muestra el valor del parámetro de configuración `PARAM` tal como está definido para 
    el sistema seleccionado actualmente y sale.

    El valor del parámetro se imprime en formato JSON. Si no se especifica `PARAM` o si 
    se establece en `all`, se mostrará toda la configuración para el sistema actualmente 
    seleccionado.

# Más opciones

Puede consultar más opciones en la sección [Command Line Reference](https://reframe-hpc.readthedocs.io/en/stable/manpage.html) 
de la documentación oficial de ReFrame.
