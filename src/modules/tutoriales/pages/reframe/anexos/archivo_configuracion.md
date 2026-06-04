# Descripción

ReFrame viene preconfigurado con una configuración genérica mínima que le permitirá 
ejecutar ReFrame en cualquier sistema. Esto le permitirá ejecutar pruebas locales 
simples utilizando el compilador predeterminado del sistema. Por supuesto, ReFrame 
es mucho más poderoso que eso. Esta sección lo guiará a través de la configuración 
de ReFrame para el cluster Yoltla.

El archivo de configuración de ReFrame puede ser un archivo JSON o un archivo de 
Python que almacene la configuración del sitio en una cadena con formato JSON.


# Localización

ReFrame por de defecto busca un archivo de configuración en las siguientes ubicaciones 
en ese orden:

1.  \${HOME}/.reframe/settings.{py,json}

2.  \${RFM_INSTALL_PREFIX}/settings.{py,json}

3.  /etc/reframe.d/settings.{py,json}

La variable `RFM_INSTALL_PREFIX` hace referencia al directorio de instalación de ReFrame.

Si se desea pasar una configuración fuera de estas ubicaciones, hay dos formas de 
proporcionar un archivo de configuración personalizado a ReFrame:

1.  Pasarlo por la opción [`-C`, `--config-file`](/reframe/scripts/lanzar_pruebas.xml#config) 
desde la linea de comando.

2.  Utilizando la variable de entorno `RFM_CONFIG_FILE`.

```admonish info title=" "
Las opciones de la línea de comandos siempre tienen prioridad sobre sus respectivas 
variables de entorno.
```


# Estructura

Toda la configuración de ReFrame es un único objeto JSON cuyas propiedades se encargan 
de configurar los aspectos básicos del framework. Nos referiremos a estas propiedades 
de nivel superior como `secciones`. Estas secciones contienen otros objetos que definen 
aún más en detalle el comportamiento del framework. Si está utilizando un archivo Python 
para configurar ReFrame, este gran objeto de configuración JSON se almacena en una variable 
especial llamada `site_configuration`.

Hay tres secciones obligatorias que debe proporcionar cada archivo de configuración:
[systems](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#system-configuration),
[environments](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#environment-configuration)
y [logging](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#logging-configuration). 
Primero cubriremos estas y luego pasaremos a las [secciones opcionales](#otras-opciones).

Para obtener una lista completa y una descripción de todas las opciones de configuración, consulte 
la sección [Configuration Reference](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html) 
de la documentación oficial de ReFrame.


## Configuración de Systems

ReFrame le permite configurar múltiples sistemas en el mismo archivo de configuración. 
Cada sistema es un objeto diferente dentro de la sección `systems`. En nuestro ejemplo 
definimos solo un sistema para el cluster Yoltla.

```python
'systems': [
        {
            'name': 'yoltla',
            'descr': 'settings para el cluster yoltla',
            'hostnames': ['yoltla.supercomputo.izt.uam.mx','nc','tt'],
            'modules_system': 'tmod32',
            'partitions': [
                {
                    'name': 'q1h-20p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1'],
                    'environs': ['default','builtin-gcc-5.5.0'],
                    'descr': 'particion q1',
                    'launcher': 'srun'
                },
                {
                    'name': 'tt2d-80p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt2d-80p'],
                    'environs': ['defecto','builtin-gcc-5.5.0'],
                    'descr': 'particion tt2d-80p',
                    'launcher': 'srun'
                }
            ]
        }
    ]
```

Cada sistema tiene asociado un conjunto de propiedades, que en este caso son las siguientes:

- `name`: El nombre del sistema. Debe ser una cadena alfanumérica (se permiten `-` 
guiones) y se usará para referirse a este sistema en otros contextos.

- `descr`: Una descripción detallada del sistema.

- `hostnames`: Esta es una lista de patrones de nombres de host que siguen la sintaxis 
de expresiones regulares de Python, que utilizará ReFrame cuando intente seleccionar 
automáticamente una entrada de configuración para el sistema actual.

- `modules_system`: Esto se refiere al backend de administración de módulos que debe 
usarse para cargar módulos de entorno en este sistema. Se admiten múltiples backends.

  Para obtener la lista completa de los sistemas de módulos admitidos, consulte el 
  siguiente [enlace](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#systems-.modules_system).

- `partitions`: La lista de particiones que están definidas para este sistema. Cada 
partición se define como un objeto separado. Dedicamos el resto de esta sección a las 
particiones del sistema, ya que son una parte esencial de la configuración de ReFrame.

Una partición del sistema en ReFrame es una partición virtual o separación del sistema. 
En el ejemplo que se muestra aquí, definimos dos particiones que corresponden a particiones 
del planificador de trabajos (SLURM), aunque tambien puede definir particiones que no 
correspondan a una partición del planificador, como los nodos de login.

Las particiones \'q1h-20p\' y \'tt2d-80p\' se refieren a dos conjuntos diferentes de 
nodos en el mismo cluster que están efectivamente separados mediante restricciones de 
SLURM. Elijamos la partición \'q1h-20p\' y examinémosla con más detalle:

```python
{
    'name': 'q1d-20p',
    'scheduler': 'slurm',
    'resources':[],
    'modules': [],
    'access': ['--partition=q1d-20p'],
    'environs': ['defecto','builtin-gcc-5.5.0'],
    'descr': 'particion q1d-20p',
    'launcher': 'srun'
}
```

Las propiedades básicas de una partición son las siguientes:

- `name`: El nombre de la partición. Debe ser una cadena alfanumérica (se permiten `-` 
guiones) y se usará para hacer referencia a esta partición en otros contextos.

- `descr`: Una descripción detallada de la partición del sistema.

- `scheduler`: El administrador o planificador de trabajos utilizado en esta partición 
para iniciar trabajos paralelos. En este ejemplo particular, se utiliza el planificador 
SLURM.

  Para obtener una lista completa de los planificadores de trabajos admitidos, consulte el siguiente
  [enlace](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#systems-.partitions-.scheduler).

- `launcher`: El iniciador de trabajos paralelos utilizado en esta partición. En este 
caso, se utilizará el comando `srun`.

  Para obtener una lista completa de los lanzadores de trabajos paralelos admitidos, consulte el siguiente
  [enlace](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#systems-.partitions-.launcher).

- `access`: Una lista de opciones del planificador que se pasarán al script del trabajo 
generado para obtener acceso a esa partición lógica. Observe cómo, en este caso, los 
nodos se seleccionan a través una partición del planificador real, pero es posible de 
otras formas.

- `environs`: La lista de entornos que utilizará ReFrame para ejecutar pruebas de regresión 
en esta partición. Estos son solo nombres simbólicos que se refieren a entornos definidos 
en la sección environments que se describe en la siguiente sección.

- `max_jobs`: El número máximo de pruebas de regresión que se pueden lanzar a esta partición.

- `resources`: Este es un conjunto de recursos adicionales opcionales a los que las 
pruebas pueden acceder de forma transparente.

  Puede ver un ejemplo de uso en la sección [`extra_resources`](/reframe/anexos/referencia_api.xml#extra_resources).
  Para obtener más información de esta propiedad, consulte el siguiente
  [enlace](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#systems-.partitions-.resources-.options).


## Configuración de Environments

Ya hemos visto entornos a los que se hace referencia por la propiedad `environs` de 
una partición. Un entorno en ReFrame es simplemente una colección de módulos de entorno, 
variables de entorno, compiladores y banderas de compilación. Ninguno de estos atributos 
es obligatorio. Un entorno puede simplemente estar vacío.

Los entornos en ReFrame se configuran en la seccón `environments`. Para cada entorno 
al que se hace referencia dentro de una partición, debe estar presente su respectiva 
definición en esta sección. En nuestro ejemplo, definimos entornos para compiladores 
básicos, así como uno por defecto, que se usa como configuración genérica.

```python
'environments': [
        {
            'name': 'defecto',
            'modules': [],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'builtin-gcc-7.2.0',
            'modules': ['gcc/7.2.0'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'builtin-openmpi-2.1.5',
            'modules': ['openmpi/2.1.5'],
            'cc': 'mpicc',
            'cxx': 'mpic++',
            'ftn': 'mpifort'
        }
    ]
```

Cada entorno está asociado a un nombre. Este nombre se utilizará para hacer referencia 
a este entorno en diferentes contextos.


## Configuración de Logging

ReFrame tiene un poderoso mecanismo de registro que brinda un control detallado sobre 
qué información se registra, dónde se registra y cómo se formatea esta información. 
Además, permite registrar datos de rendimiento de las pruebas de rendimiento. Veamos 
cómo se define el logging en nuestra configuración usada en el cluster Yoltla:

```python
'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'name': 'logs/rfm.out',
                    'level': 'info',
                    'format': '%(message)s',
                    'append': False,
                    #'timestamp': '%d-%m-%Y_%H-%M-%S'
                },
                {
                    'type': 'file',
                    'name': 'logs/rfm.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',
                    'append': False,
                    #'timestamp': '%d-%m-%Y_%H-%M-%S'
                },
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True
                },
            ]
        }
    ],
```

El Logging se configura en la sección `logging` del archivo de configuración, que es 
una lista de objetos registradores. A menos que desee configurar el Logging de manera 
diferente para diferentes sistemas, un solo objeto `logging` es suficiente.

Cada objeto logging está asociado con un nivel de logs almacenado en la propiedad 
`level` y tiene un conjunto de controladores de logs que son realmente responsables 
de manejar los logs de logs reales.

La salida de ReFrame se realiza a través del mecanismo de registro, lo que significa 
que si no especifica ningún controlador de logs, ¡no obtendrá ninguna salida de ReFrame!

La propiedad `handlers` del objeto `logging` contiene los controladores. Tenga en 
cuenta que puede usar varios controladores al mismo tiempo, lo que le permite enviar 
la salida de ReFrame a diferentes receptores y en diferentes niveles de detalle. 
Todos los objetos de controlador comparten un conjunto de propiedades comunes. Estas 
son los siguientes:

- `type`: Este es el tipo de controlador, que determina su funcionalidad. Dependiendo 
del tipo de controlador, las propiedades específicas del controlador pueden estar 
permitidas o requeridas.

  Para obtener una listacompleta de los tipos de controladores de registro disponibles, consulte el siguiente
  [enlace](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#logging-.handlers-.type).

- `level`: El nivel de corte para los mensajes que llegan a este controlador. 
Cualquier mensaje con un número de nivel inferior se filtrará.

- `name`: El nombre de la salida a donde se enviará el log. Observe el uso de la 
carpeta y archivo `logs/rfm.out` y `logs/rfm.log`, esto implica que en cada prueba 
realizada debe crearse la carpeta *logs* para enviar las salidas de ReFrame, si no 
Reframe fallará!!

- `format`: Una cadena de formato para formatear el log emitido. ReFrame usa los especificadores de formato de
  [Python Logging](https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes), 
  pero también define sus propios especificadores.

No entraremos en los detalles de los controladores individuales aquí. En este ejemplo 
particular, usamos tres controladores de dos tipos distintos:

1.  `stream`: Este controlador sirve para imprimir cualquier mensaje informativo 
(y advertencias y errores) de ReFrame a la salida estándar. Esto maneja esencialmente 
la salida real de ReFrame. Solo hay dos opciones para stream:

    - `stdout`

    - `stderr`

2.  `file`: Un controlador de archivos para imprimir la salida del framework en el archivo `rfm.out`

3.  `file`: Un controlador de archivos para imprimir mensajes de depuración en el archivo `rfm.log` 
usando un formato de mensaje más extenso que contiene una marca de tiempo, el nombre del nivel, etc.

```admonish info title=" "
En la configuración, se encuentra comentado el uso de `timestamp`. Esto agrega una 
marca de tiempo a los prefijos de los archivos log de ReFrame. Los formatos válidos 
son los aceptados por la función [time.strftime()](https://docs.python.org/3.8/library/time.html#time.strftime).
```

``` admonish warning title=" "
Para esta configuración, si no se crea la carpeta *logs*, se presentara el siguiente error:

    `/LUSTRE/home/../../../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/ reframe-3.9.2/bin/reframe:
    failed to load configuration: [Errno 2] No such file or directory: '/LUSTRE/home/../../../t.800/Pruebas/logs/rfm.out'`
```

Finalmente, hay un conjunto especial de controladores para manejar los mensajes de 
registro de rendimiento (performance log messages).

Los mensajes de registro de rendimiento se generan solo para [pruebas de rendimiento](../scripts/pruebas_rendimiento.md), 
es decir, pruebas que definen los atributos `perf_variables` o `perf_patterns`. Los 
controladores de registro de rendimiento se almacenan en la propiedad `handlers_perflog`.

El controlador `filelog` utilizado en este ejemplo creará un archivo por prueba y por 
combinación de sistema/partición de la siguiente forma:

    perflogs/<system>/<partition>/<testname>.log`

y agregará los datos de rendimiento obtenidos cada vez que se ejecute una prueba de rendimiento.

Observe cómo se estructura el mensaje que se va a registrar en la propiedad `format`, 
de modo que se pueda analizar fácilmente. Un ejemplo del mensaje de rendimiento obtenido 
es el siguiente:

    2022-06-19T19:57:04|reframe 3.9.2|Namd_CPU_Benchmarks___Stmv____stmv_namd___1_cpu_nc on yoltla:q1d-20p using defecto|jobid=925569|Days_ns=5.435009999999999| ref=5.471 (l=-0.5, u=0.15)|days/ns

Para obtener una referencia completa de los parámetros de configuración de Logging, 
consulte la sección [Logging Configuration](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#logging-configuration) 
de la documentación oficial de ReFrame.


# Otras opciones

Finalmente, hay secciones de configuración que son opcionales pero explicaremos a 
continuación ya que son utilizados en nuestro archivo de configuracion para el cluster Yoltla.

1.  La sección `general`, contiene opciones generales del comportamiento del framework

2.  La sección `schedulers`, contiene variables de configuración específicas para los 
diferentes planificadores de trabajos como SLURM.


## Configuración de General

Las configuración `General` utilizada es la siguiente:

```python
'general': [
        {
            'purge_environment': True,
            'report_file': 'logs/run-report.json'
            #'timestamp_dirs': '%d-%m-%Y/%H-%M-%S'
        }
    ],
```

Donde:

- `purge_environment`: Purga todos los módulos de entorno cargados antes de ejecutar 
cualquier prueba.

- `report_file`: El archivo donde ReFrame almacenará su informe, en este caso dentro 
de la carpeta *logs*.

```admonish info title=" "
En la configuración, se encuentra comentado el uso de `timestamp_dirs`. Esto agrega 
una marca de tiempo a los prefijos de directorio de ReFrame. Los formatos válidos 
son los aceptados por la función [time.strftime()](https://docs.python.org/3.8/library/time.html#time.strftime). 
Si se especifica desde la línea de comandos sin ningún argumento, \"%FT%T\" se utilizará 
como formato de hora.
```


## Configuración de Schedulers

Un objeto de configuración `Scheculers` contiene opciones de configuración específicas 
para el comportamiento del programador de trabajo. En el caso del Yoltla: [SLURM](https://slurm.schedmd.com/).

Las configuración `schedulers` utilizada es la siguiente:

```python
'schedulers': [
        {
            'name': 'slurm',
            'ignore_reqnodenotavail': True,
            'use_nodes_option': True
        }
    ]
```

Donde:

- `name`: El nombre del planificador al que hacen referencia estas opciones. Puede ser cualquiera de los
  [backends](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#systems-.partitions-.scheduler)
  de programador de trabajos compatibles.

- `ignore_reqnodenotavail`: Esta opción es relevante solo para los backends de SLURM. 
Si un trabajo asociado a una prueba está en estado pendiente con el motivo `ReqNodeNotAvail` 
de SLURM, ReFrame verificará el estado de los nodos y, si todos están caídos, cancelará 
el trabajo. A veces, sin embargo, el algoritmo de Slurm establecerá el motivo pendiente 
como `ReqNodeNotAvail` y marcará todos los nodos del sistema como no disponibles, lo 
que hará que ReFrame elimine el trabajo. En tales casos, puede configurar este parámetro 
`true` para evitar esto.

- `use_nodes_option`: Esta opción siempre emite la opción `--nodes` de Slurm en el 
script de trabajo. Esta opción solo es relevante para los backends de SLURM.

```admonish info title=" "
El uso de la opción `use_node_option` hace obligatorio usar las opciones `num_nodes` 
y `num_tasks_per_node` de ReFrame, que agrega las opciones `--nodes` y `--ntasks-per-node` 
respectivamente en el script de trabajo.
```

Para ver otras opciones útiles, consulte la sección
[Scheduler Configuration](https://reframe-hpc.readthedocs.io/en/stable/config_reference.html#scheduler-configuration) 
de la documentación oficial de ReFrame.


# Configuración del sistema

Como se discutió anteriormente, el archivo de configuración de ReFrame puede almacenar 
las configuraciones para múltiples sistemas. Cuando se inicie, ReFrame elegirá la primera 
configuración coincidente y la cargará.

ReFrame usa un mecanismo de detección automática para obtener información sobre el host 
en el que se está ejecutando y usa esa información para elegir la configuración correcta 
del sistema. Actualmente, solo se admite un método de detección automática que recupera 
el nombre de host. En base a esto, ReFrame pasa por todos los sistemas en su configuración 
e intenta hacer coincidir el nombre de host con cualquiera de los patrones definidos en la
propiedad `hostnames` de cada sistema. El proceso de detección se detiene en la primera 
coincidencia encontrada y se selecciona la configuración de ese sistema.


# Variables de ambiente

Varios aspectos de ReFrame se pueden controlar a través de variables de ambiente. Por 
lo general , las variables de ambiente tienen contrapartes en las opciones de la línea 
de comandos o los parámetros de configuración. Las opciones de la línea de comandos y 
los parámetros de configuración tienen prioridad sobre las variables de ambiente, las 
opciones de la línea de comando preceden a los parámetros de configuración.

Para ver una lista de variables de ambiente aceptadas por Reframe, revise la sección
[Environment](https://reframe-hpc.readthedocs.io/en/stable/manpage.html?#environment) 
de la documentación oficial de ReFrame.

Tambien puede consultar y modificar las variables de ambiente directamente en el archivo 
`config.json` presente en su directorio de instalación de Reframe: `reframe/schemas/config.json`

```admonish info title=" " 
Recomendamos modificar las variables de ambiente por línea de comandos o parámetros de 
configuración en lugar de modificar el archivo config.json.
```


# Detección automática

ReFrame puede detectar automáticamente la topología del procesador de las particiones 
locales y remotas. La información del procesador y del dispositivo se pone a disposición 
de las pruebas a través de los atributos correspondientes.

Para obtener más información, consulte la sección [Topologia](./topologia.md).
