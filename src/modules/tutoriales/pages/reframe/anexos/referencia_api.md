# Descripción

Esta sección proporciona una guía de referencia de la API ReFrame para escribir pruebas de regresión que
cubre detalles relevantes usados en los scripts para el cluster Yoltla. Se cubre solo en la medida en que esto pueda ser útil para el usuario final del cluster.

Para obtener más información, consulte la sección [Test API Reference](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html#test-api-reference) de la documentación oficial de ReFrame.

# Pipeline

Cada caso de prueba de ReFrame pasa por un Pipeline de etapas. Las pruebas de ReFrame pueden
personalizar su funcionamiento a medida que se ejecutan adjuntando [enlaces](#enlaces_pipeline) a las
etapas del Pipeline. La siguiente figura muestra las diferentes etapas del Pipeline.

+----------+----------+----------+----------+-------------+-----------+
| Setup    | Compile  | Run      | Sanity   | Performance | Cleanup   |
+----------+----------+----------+----------+-------------+-----------+

: Pipeline de una prueba de regresión

Todas las pruebas pasarán por cada etapa una tras otra. Sin embargo, algunos tipos de pruebas implementan algunas etapas como no operativas, mientras que las fases de verificación de sanidad o rendimiento pueden omitirse a pedido (ver las opciones `--skip-sanity-check` y `--skip-performance-check`).

Para obtener más información, consulte la sección [The Regression Test Pipeline](https://reframe-hpc.readthedocs.io/en/stable/pipeline.html#the-regression-test-pipeline) de la documentación oficial de ReFrame.

# Clases base de prueba

reframe.CompileOnlyRegressionTest

:   Base: [RegressionTest](#run_regression)

    Clase base para pruebas de regresión de solo compilación.

    Estas pruebas son locales de forma predeterminada y omitirán la fase de ejecución del pipeline
    de prueba de regresión.

<!-- -->

reframe.RegressionTest

:   Clase base para pruebas de regresión.

    Todas las pruebas de regresión eventualmente deben heredar de esta clase. Esta clase proporciona la implementación de las fases del pipeline por las que pasa la prueba de regresión durante su vida útil.

    **Propiedades**

    - `build_locally = True`

      Esta opción compila el codigo localmente. Si se establece en False, ReFrame generará un trabajo de compilación en la partición donde se ejecutará la prueba. Establecer esto en False es útil cuando la compilación no es compatible con el sistema donde se ejecuta ReFrame.

      - **Type**: booleano

      - **Default**: True

    - `build_system = None`

      El sistema de compilación que se usará para esta pruebai, ejemplo: `Make` para detectar Makefile's. Si no se especifica, Reframe intentará resolverlo automáticamente en función del valor de sourcepath.

      - **Type**: str o [reframe.core.buildsystems.BuildSystem](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html?highlight=api%20#reframe.core.buildsystems.BuildSystem)

      - **Default**: `None`

    - `build_time_limit = None`

      El límite de tiempo para el trabajo de compilación de la prueba de regresión. Se especifica de forma similar al atributo `time_limit`.

      - **Type**: str, float o int

      - **Default**: `None`

    - `property current_environ`

      Variable de consulta donde se guarda el entorno de programación con el que se está ejecutando actualmente la prueba de regresión. Esto se establece durante la fase `setup()`.

    - `property current_partition`

      Variable de consulta donde se guarda la partición del sistema en la que se está ejecutando actualmente la prueba de regresión. Esto se establece durante la fase `setup()`.

      Ejemplo de consulta:

      ``` python
          @run_before('run')
          def define_tasks(self):
              # Se definen opciones para cada partición
              if self.current_partition.fullname in ['yoltla:q1h-20p']:
                  self.num_tasks = 20
                  self.num_tasks_per_node=20
              elif self.current_partition.fullname in ['yoltla:q1h-40p']:
                  self.num_tasks = 20
                  self.num_tasks_per_node=10
      ```

    - `property current_system`

      Variable de consulta donde se guarda sistema en el que se está ejecutando actualmente la prueba de regresión.
      Esto se establece durante la fase de inicialización.

    - `descr`

      Una descripción detallada de la prueba.

    - `exclusive_access = False`

      Especifica si esta prueba necesita acceso exclusivo a los nodos.

      - **Type**: booleano

      - **Default**: False

    - `executable`

      El nombre del ejecutable que se lanzará durante la fase de ejecución.

      - **Type**: str

      - **Default**: Requerido

    - `executable_opts = []`

      Lista de opciones a pasar al executable.

      - **Type**: List\[str\]

      - **Default**: \[\]

- `extra_resources = {}`

  Este campo es para especificar los recursos personalizados que necesita esta prueba. Estos recursos se definen en el archivo de configuración de una partición del sistema. Por ejemplo:

  ``` python
  'resources': [
      {
          'name': 'gpu',
          'options': ['--gres=gpu:{num_gpus_per_node}']
      }
  ]
  ```

  Una prueba de regresión puede instanciar los recursos al establecer el atributo `extra_resources` de la siguiente manera:

  ``` python
  self.extra_resources = {
      'gpu': {'num_gpus_per_node': 2}
  }
  ```

  El script generado (para SLURM) contendrá las siguiente línea:

  ``` bash
  #SBATCH --gres=gpu:2
  ```

<!-- -->

- `keep_files = []`

  Lista de archivos que se guardarán después de que finalice la prueba.

  De forma predeterminada, Reframe guarda la salida estándar, el error estándar y el script generado que se usó para ejecutar esta prueba.

  Estos archivos se copiarán en el directorio de salida de la prueba durante la fase cleanup().

  También se aceptan directorios en este campo.

  Los nombres de ruta relativos se resuelven respecto al directorio stage.

  - **Type**: List\[str\]

  - **Default**: \[\]

- `maintainers = []`

  Lista de personas responsables de esta prueba. Cuando la prueba falla, se imprimirá esta lista de contactos.

  - **Type**: str

  - **Default**: None

- `modules = []`

  Lista de módulos que se cargarán antes de ejecutar esta prueba.
  Estos módulos se cargarán durante la fase `setup()`.

  - **Type**: List\[str\]

  - **Default**: \[\]

- `num_cpus_per_task = None`

  Número de CPU por tarea requeridas por esta prueba.
  Ignorado si es `None`.

  - **Type**: integer o `None`

  - **Default**: `None`

- `num_gpus_per_node = 0`

  Número de GPU por nodo requeridas por esta prueba. Este atributo se traduce internamente como recurso.
  Eche un vistazo al atributo [`extra_resources`](#extra_resources).

  El atributo `num_gpus_per_node` se traduce internamente al recurso `_rfm_gpu`, por lo que la
  configuración `self.num_gpus_per_node = 2` es equivalente a lo siguiente:

  ``` python
  self.extra_resources = {'_rfm_gpu': {'num_gpus_per_node': 2}}
  ```

  - **Type**: integer.

  - **Default**: 0.

- `num_tasks = 1`

  Número de tareas requeridas por esta prueba.

  - **Type**: integer

  - **Default**: 1

- `num_tasks_per_core = None`

  Número de tareas por núcleo requeridas por esta prueba.
  Ignorado si `None`.

  - **Type**: integer

  - **Default**: `None`

- `num_tasks_per_node = None`

  Número de tareas por nodo requeridas por esta prueba.
  Ignorado si `None`.

  - **Type**: integer

  - **Default**: `None`

- `num_tasks_per_socket = None`

  Número de tareas por socket requeridas por esta prueba.
  Ignorado si None.

  - **Type**: integer.

  - **Default**: None.

- `postbuild_cmds = []`

  Lista de comandos de shell que se ejecutarán después de una compilación exitosa.

  Estos comandos se emiten en el script después de los comandos de compilación generados por el sistema de compilación seleccionado.

  - **Type**: List\[str\]

  - **Default**: \[\]

- `postrun_cmds = []`

  Lista de comandos de shell para ejecutar después del comando de lanzamiento paralelo.

  - **Type**: List\[str\]

  - **Default**: \[\]

- `prebuild_cmds = []`

  Lista de comandos de shell que se ejecutarán antes de compilar.

  Estos comandos se emiten en el script antes de los comandos de compilación generados por el sistema de compilación seleccionado.

  - **Type**: List\[str\].

  - **Default**: \[\].

- `prerun_cmds = []`

  Lista de comandos de shell para ejecutar antes del comando de lanzamiento paralelo.

  - **Type**: List\[str\]

  - **Default**: \[\]

- `reference = {}`

  El conjunto de valores de referencia para esta prueba.

  Los valores de referencia se especifican como un diccionario de ámbito basado en las variables de
  rendimiento definidas en `perf_patterns` y en combinaciones de sistema/partición. Consulte la sección
  de pruebas de rendimiento.

- `skip(msg=None)`

  Skip test.

  - **Parámetros**:

    - **msg** - un mensaje que explica por qué se omitió la prueba.

- `skip_if(cond, msg=None)`

  Omite la prueba si la condición es verdadera.

  - **Parámetros**:

    - **cond** -- la condición para comprobar si se salta la prueba.

    - **msg** -- un mensaje que explica por qué se omitió la prueba.

- `skip_if_no_procinfo(msg=None)`

  Omite la prueba si no hay información disponible sobre la topología del procesador.

  Este método solo tiene efecto si se llama después de la estapa setup.

  - **Parámetros**:

    - **msg** - un mensaje que explica por qué se omitió la prueba. Si no se especifica, se utilizará un mensaje predeterminado.

- `sourcepath = ' '`

  La ruta al archivo de origen o al directorio de origen de la prueba.

  Debe ser una ruta relativa al `sourcesdir`, apuntando a una subcarpeta o un archivo contenido en `sourcesdir`. Esto se aplica también en el caso de que `sourcesdir` sea un repositorio de Git.

  Si se refiere a un archivo normal, este archivo se compilará utilizando el sistema de compilación elegido.

  - **Type**: str.

  - **Default**: \' \'

<!-- -->

- `sourcesdir = 'src'`

  El directorio que contiene los recursos de la prueba.

  Este directorio se puede especificar con una ruta absoluta o con una ruta relativa a la ubicación de la prueba. Su contenido siempre se copiará en el directorio de etapas de la prueba.

  Este atributo también puede aceptar una URL, en cuyo caso ReFrame lo tratará como un repositorio de Git e intentará clonar su contenido en el directorio de etapa de la prueba.

  Si se establece en `None`, la prueba no tiene recursos y no se realiza ninguna acción.

  - **Type**: str o `None`

  - **Default**: \'src\' si tal directorio existe en el nivel de prueba, de lo contrario `None`

- `tags = set()`

  Conjunto de etiquetas asociadas a esta prueba.

  Esta prueba se puede seleccionar desde la interfaz utilizando cualquiera de estas etiquetas.

  - **Type**: Set\[str\]

  - **Default**: Un conjunto vacío

- `time_limit = None`

  Límite de tiempo para esta prueba.

  El límite de tiempo se especifica como una cadena en el formulario `<days>d<hours>h<minutes>m<seconds>s` o como número de segundos. Si se establece en `None`, se utilizará el `time_limit` de la partición.

- `use_multithreading = None`

  Especifica si esta prueba necesita subprocesos múltiples simultáneos habilitados.
  Ignorado si None.

  - **Type**: booleano o `None`

  - **Default**: `None`

- `valid_prog_environs`

  Lista de entornos o características del entorno o propiedades del entorno requeridas por esta prueba.

  - **Type**: List\[str\]

  - **Default**: Requerido

- `valid_systems`

  Lista de sistemas o características del sistema o propiedades del sistema requeridas por esta prueba.

- `variables = {}`

  Las variables de entorno deben establecerse antes de ejecutar esta prueba.
  Estas variables se configurarán durante la fase setup().

  - **Type**: Dict\[str, str\]

  - **Default**: {}

    Ejemplo:

    ``` python
    variables = {
                'OMP_NUM_THREADS': '$SLURM_CPUS_PER_TASK'
                }
    ```

    El script generado (para SLURM) contendrá las siguiente línea:

    ``` bash
    export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASKS
    ```

reframe.RunOnlyRegressionTest

:   Base: [RegressionTest](#run_regression)

    Clase base para pruebas de regresión de solo ejecución.

    **Propiedades**

    - `run()`

      La fase de ejecución del pipeline de prueba de regresión.

      Los recursos de la prueba se copian en el directorio de stage y el resto de la ejecución se delega al `RegressionTest.run()`.

# Test Decorators

\@reframe.simple_test

:   Decorador de clases para registrar pruebas con ReFrame.

\@reframe.deferrable

:   Convierte la función decorada en una expresión diferida.

    Para obtener más información, consulte la sección de [Funciones Diferibles](reframe/scripts/pruebas_sanidad.xml#funciones_diferibles).

\@reframe.performance_function(unit, \*, perf_key=None)

:   Decora una función para marcarla como una función de rendimiento.

    Para obtener más información, consulte la sección de [Pruebas de rendimiento](reframe/scripts/pruebas_rendimiento.xml#funciones_diferibles).

    - **Parámetros:**

      - **unit**: Una cadena que representa la unidad de medida de esta métrica.

      - **pef_key**: Clave para identificar la variable de performance.

\@reframe.run_after(stage)

:   Adjunta la función decorada después de una determinada etapa del pipeline.

    La función decorada se ejecutará justo después de la etapa (stage) a la que se adjuntó. Este decorador también
    admite \'init\' como argumento válido, en este caso, la función se ejecutará justo después de que se
    inicialice la prueba (es decir, después de que se llame el método *init*()) y antes de ingresar al
    pipeline de la prueba.

    - **Parámetros:**

      - **stage**: La etapa del pipeline a la que se adjuntará esta función.

        Consulte la sección [Enlaces Pipeline](#enlaces_pipeline).

\@reframe.run_before(stage)

:   Adjunta la función decorada antes de una determinada etapa del pipeline.

    La función decorada se ejecutará justo antes de la etapa (stage) a la que se adjuntó.

    - **Parámetros:**

      - **stage** : La etapa del pipeline a la que se adjuntará esta función.

        Consulte la sección [Enlaces Pipeline](#enlaces_pipeline).

\@reframe.sanity_function

:   Decora una función para marcarla como una verificación de sanidad.

    Este decorador convertirá la función dada en una función `deferrable()` y la marcará para que se ejecute durante la etapa de sanidad de la prueba.

    Para obtener más información, consulte la sección de [Pruebas de sanidad](reframe/scripts/pruebas_sanidad.xml).

# Enlaces Pipeline

ReFrame proporciona un mecanismo que permite adjuntar funciones para que se ejecuten antes o después de una etapa determinada del pipeline de ejecución. Esto se logra a través de las funciones integradas `@run_before` y `@run_after`. Una vez adjuntadas a una etapa determinada, estas funciones se conocen como **enlaces de Pipeline**. Se puede unir un enlace a múltiples etapas del pipeline y también se pueden unir múltiples enlaces a la misma etapa del pipeline.

Los enlaces pipeline adjuntos a varias etapas se ejecutarán en cada etapa del pipeline a la que se adjuntó el enlace. Las etapas del pipeline con varios enlaces adjuntos ejecutarán estos enlaces en el orden en que se adjuntaron a la etapa del pipeline determinada.

Una función puede adjuntarse a cualquiera de las siguientes etapas (enumeradas en orden de ejecución): `init`, `setup`, `compile`, `run`, `sanity`, `performance` y `cleanup`.

La etapa `init` se refiere a la creación de instancias de la prueba y se ejecuta antes de ingresar al pipeline de ejecución. Por lo tanto, no se puede adjuntar una función para que se ejecute antes de esta etapa. Los enlaces adjuntos a cualquier otra etapa se ejecutarán exactamente antes o después de que se ejecute esta etapa. Por lo tanto, aunque se ejecutarán un enlace \"post-init\" y uno \"pre-setup\" después de que se haya inicializado una prueba y antes de que la prueba pase por la primera etapa del pipeline, se ejecutarán en momentos diferentes: el enlace \"post-init\" se ejecutará justo después de que la prueba se inicializa. Luego, el framework continuará con otras actividades y ejecutará el enlace \"pre-setup\" justo antes de ejecutar su etapa de setup.

Los *Enlaces Pipeline* son muy útiles ya que existen variables que solo se pueden consultar, definir o modificar
después o antes de que Reframe haya pasado por ciertas etapas del [`Pipeline`](#pipeline). Algunas de estas variables son:

## init

### **Parámetros**

Los parámetros nos ayudan a instanciar múltiples pruebas diferentes en una misma prueba. Consulte la
sección [Parámetros](reframe/scripts/parametros.xml) para más información. Estos se definen
dentro del cuerpo de la clase de la prueba sin embargo si queremos consultar o modificar el comportamiento
de una prueba usando los parámetros desde la clase de prueba, se nos presentara el siguiente error:

    reframe syntax error: accessing a test parameter from the class body is disallowed

Para solucionar esto utilizamos el decorador `@run_after('init')` para utilizar los parámetros **después**
de que se hayan instanciado. Ejemplo:

:::: formalpara
::: title
Ejemplo \@run_after(\'init\')
:::

``` python
@rfm.simple_test
class Namd_CPU_Benchmarks(rfm.RunOnlyRegressionTest):

      # Modulos a cargar
      modules = ['namd/2.13']

      valid_prog_environs = ['defecto']

      benchmark_info = parameter([
        ('Stmv','stmv.namd'),
        ('F1atpase','f1atpase.namd')
      ])

      # Parametros para el Yoltla
      num_nodes = parameter([1, 2, 4, 5, 8, 16])
      node_type = parameter(['nc','ttv1','ttv2'])

.
.
.


    @run_after('init')
    def setup_system(self):

        self.__bench, self.__name = self.benchmark_info

        self.descr = f'NAMD Benchmark: {self.node_type} con {self.num_nodes} nodo(s)'

        valid_systems = {
                           'nc': {
                                   1: ['yoltla:q1d-20p'],
                                   2: ['yoltla:q1d-40p'],
                           },
                           'ttv1': {
                                   4: ['yoltla:tt2d-80p'],
                                   5: ['yoltla:tt2d-100p'],
                           },
                           'ttv2': {
                                   2: ['yoltla:tt2d-64p'],
                                   4: ['yoltla:tt1d-128p'],
                           }
                        }

        try:
            self.valid_systems = valid_systems[self.node_type][self.num_nodes]
        except KeyError:
            self.valid_systems = []

        # Setup nombre del Benchmark a ejecutar
        self.sourcesdir= f'src/{self.bench_name}'

.
.
.
```
::::

En el ejemplo anterior , utilizamos los parámetros para definir las variables `descr`,`sourcedir` y `valid_systems`
en la función `setup_system` con del decorador `@run_after('init')`

## compile

En esta etapa El código fuente asociado con la prueba se compila utilizando el entorno de programación
actual. Si la prueba es \"solo de ejecución\", esta fase no es operativa.

Antes de construir la prueba, todos los recursos asociados con ella se copian en el directorio de etapa
del caso de prueba. ReFrame luego cambia temporalmente a ese directorio y crea la prueba.

Puede usar la opción \@run_before(\'compile\') para definir variables de ambiente antes de la compilación.
Ejemplo

:::: formalpara
::: title
Ejemplo \@run_before(\'compile\')
:::

``` python
    @run_before('compile')
    def set_compilation_flags(self):
        self.build_system.cxxflags = ['-std=c++11', '-Wall']
        environ = self.current_environ.name
        if environ in {'clang', 'gnu'}:
            self.build_system.cxxflags += ['-pthread']
```
::::

En el ejemplo anterior definimos cxxflags del entorno de compilación.

## run

Durante esta fase, se creará un script de trabajo asociado con el caso de prueba y se enviará para su
ejecución.

### **getlauncher**

En ocasiones, es posible que deba reemplazar por completo el comando launcher de la partición ,
ya que el software que está probando puede usar su propio launcher paralelo . El truco aquí es
reemplazar el lanzador paralelo con el local, que prácticamente no emite ningún comando de lanzamiento,
una vez reemplazado el launcher puede definir como ejecutar con la opción `executable`

Al reemplazar el launcher, debemos hacerlo antes de la fase `run` , por lo tanto usamos la opción `@run_before('run')`

Ejemplo:

:::: formalpara
::: title
Ejemplo \@run_before(\'run\')
:::

``` python
      @run_before('run')
      def setup_run(self):

          # Se reemplaza lanzador del job
          self.job.launcher = getlauncher('local')()

          self.num_tasks_per_node = 20
          self.num_tasks = self.num_nodes * self.num_tasks_per_node
          self.num_tasks_per_core = 1

          # Se define como ejecutar el job
          self.executable=f'mpiexec.hydra -bootstrap slurm -np {self.num_tasks} namd2 stmv.namd'
```
::::

### **current_partition**

`current_partition` es un variable de consulta donde se guarda la partición del sistema en la que se está
ejecutando la prueba de regresión. Esto se establece durante la fase `setup()`. Puede consultarla antes
de la fase de ejecución de la siguiente forma:

:::: formalpara
::: title
Ejemplo \@run_before(\'run\')
:::

``` python
    @run_before('run')
    def define_tasks(self):
        # Se definen opciones para cada partición
        if self.current_partition.fullname in ['yoltla:q1h-20p']:
            self.num_tasks = 20
            self.num_tasks_per_node=20
        elif self.current_partition.fullname in ['yoltla:q1h-40p']:
            self.num_tasks = 20
            self.num_tasks_per_node=10
```
::::

# Variantes de prueba

A través del componente `parameter`, una prueba de regresión puede almacenar múltiples versiones o variantes de una prueba de regresión. Durante la creación de la clase, los parámetros de la prueba se construyen y combinan, asignando un índice único a cada una de las variantes de prueba disponibles.

Para obtener más información, consulte la sección de [Parámetros](reframe/scripts/parametros.xml).

# Programadores de trabajos y lanzadores paralelos

- `exclusive_access = False`

  Solicite acceso exclusivo en los nodos para este trabajo.

  - **Type**: booleano

  - **Default**: false

- `launcher`

  El lanzador de programas (paralelo) que se usará para lanzar el ejecutable (paralelo) de este trabajo.

  Los usuarios pueden configurar explícitamente el iniciador de trabajos actual, esto es relevante en situaciones especificas.

  El siguiente ejemplo muestra cómo puede reemplazar el iniciador de la partición actual para esta prueba con el iniciador \"local\":

  ``` python
  from reframe.core.backends import getlauncher

  @run_before('run')
        def setup_run(self):

          # Se reemplaza lanzador del job
           self.job.launcher = getlauncher('local')()
  ```

- `num_cpus_per_task = None`

  Número de elementos de procesamiento asociados con cada tarea para este trabajo.

  - **Type**: integer o `None`

  - **Default**: `None`

- `num_tasks = 1`

  Número de tareas para este trabajo.

  - **Type**: integer o None

  - **Default**: 1

- `num_tasks_per_core = None`

  Número de tareas por núcleo para este trabajo.

  - **Type**: integer o `None`

  - **Default**: `None`

- `num_tasks_per_node = None`

  - **Type**: integer o `None`

  - **Default**: `None`

- `num_tasks_per_socket = None`

  Número de tareas por socket para este trabajo.

  - **Type**: integer o None

  - **Default**: None

- `options = []`

  Opciones que se pasarán al programador de trabajos de back-end.

  - **Type**: List\[str\]

  - **Default**: \[\]

    Ejemplo:

    ``` python
    self.job.options = ['--constraint=nc']
    ```

    El script generado (para SLURM) contendrá las siguiente línea:

    ``` bash
    SBATCH --constraint=nc
    ```

- `time_limit = None`

  Límite de tiempo para este trabajo.

# Asignación de atributos al backend del programador de trabajos (SLURM)

+-----------------------------------+-----------------------------------+
| Atributo de prueba                | Opción SLURM                      |
+===================================+===================================+
| `num_tasks`                       | `--ntasks`                        |
+-----------------------------------+-----------------------------------+
| `num_tasks_per_node`              | `--ntasks-per-node`               |
+-----------------------------------+-----------------------------------+
| `num_tasks_per_core`              | `--ntasks-per-core`               |
+-----------------------------------+-----------------------------------+
| `num_tasks_per_socket`            | `--ntasks-per-socket`             |
+-----------------------------------+-----------------------------------+
| `num_cpus_per_task`               | `--cpus-per-task`                 |
+-----------------------------------+-----------------------------------+
| `time_limit`                      | `--time=hh:mm:ss`                 |
+-----------------------------------+-----------------------------------+
| `exclusive_access`                | `--exclusive`                     |
+-----------------------------------+-----------------------------------+

Si se establece alguno de los atributos en `None`, no se emitirá en absoluto en el script del trabajo.

:::: note
::: title
:::

La opción `--nodes` también se puede emitir si se establece el parámetro `use_nodes_option` en la configuración del planificador de trabajos.

Para obtener más información, consulte la consulte la sección [Configuracion de schedulers](reframe/anexos/archivo_configuracion.xml#configuracion_schedulers).
::::
