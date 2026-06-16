# Pruebas de rendimiento


## Descripción

Un aspecto importante de las pruebas de regresión es verificar el rendimiento.

Lo que hace que una prueba ReFrame sea una prueba de rendimiento es la definición de al 
menos una función de rendimiento. De manera similar a una prueba de sanidad 
(`@sanity_function`), una función de rendimiento es una función decorada con el decorador 
`@performance_function`, que vincula la función decorada a una unidad determinada.

Estas funciones pueden ser utilizadas por la prueba de regresión para extraer, medir o 
calcular una determinada cantidad de interés. Los valores devueltos por una función de 
rendimiento se denominan variables de rendimiento.

Las funciones de rendimiento pueden pensarse como herramientas disponibles en las pruebas
de regresión para la extracción de variables de rendimiento. De forma predeterminada, 
ReFrame intentará ejecutar todas las funciones de rendimiento disponibles durante la 
estapa de `performance` de la prueba, produciendo una sola variable de rendimiento por 
cada una de las funciones de rendimiento disponibles.

Para obtener más información, consulte la sección [Writing A Performance Test](https://reframe-hpc.readthedocs.io/en/stable/tutorial_basics.html#writing-a-performance-test) 
de la documentación oficial de ReFrame.

## Ejemplos

El siguiente script de reframe ejecuta una prueba del microbenchmark 
[STREAM](https://www.cs.virginia.edu/stream/ref.html):

```python
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher

@rfm.simple_test
class StreamTest(rfm.RegressionTest):
      # Se define sistema:particion donde se ejecuta
      valid_systems = ['yoltla:q1h-20p']

      # Se define archivo fuente presente en src
      sourcepath = 'stream.c'

      # Se define compilador a usar
      valid_prog_environs = ['builtin-gcc-7.2.0']

      # Se define tiempo límite de la prueba
      time_limit = '3m'

      # Se define el número de nodos, tareas, tareas por nodo, tareas por core
      num_nodes=1
      num_tasks_per_node = 1
      num_tasks = 1
      num_tasks_per_core = 1

      # Se define el comando para ejecutar la prueba
      executable = './stream'

      # Se establece el lanzador del job de forma local
      @run_before('run')
      def set_launcher(self):
          self.job.launcher = getlauncher('local')()

      # Función de sanidad
      @sanity_function
      def validate_solution(self):
          return sn.assert_found(r'Solution Validates', self.stdout)

      # Función de rendimiento
      @performance_function('MB/s')
      def Copy(self):
          return sn.extractsingle(r'Copy:\s+(\S+)\s+.*', self.stdout, 1, float)

      # Función de rendimiento
      @performance_function('MB/s')
      def Scale(self):
          return sn.extractsingle(r'Scale:\s+(\S+)\s+.*', self.stdout, 1, float)

      # Función de rendimiento
      @performance_function('MB/s')
      def Add(self):
          return sn.extractsingle(r'Add:\s+(\S+)\s+.*', self.stdout, 1, float)

      # Función de rendimiento
      @performance_function('MB/s')
      def Triad(self):
          return sn.extractsingle(r'Triad:\s+(\S+)\s+.*', self.stdout, 1, float)
```

En este ejemplo, extraemos cuatro variables de rendimiento, que son los valores de 
ancho de banda de la memoria para cada uno de los subpuntos de referencia: `Copy`, 
`Scale`, `Add` y `Tríad` de STREAM, donde cada una de las funciones de rendimiento 
utiliza la función de utilidad [`extractsingle()`](./pruebas_sanidad.md#sanity-extractsingle). 
Para cada uno de los subpuntos de referencia, se define una [expresión regular](https://docs.python.org/3/library/re.html) 
de Python para extraer la columna \"Best Rate MB/s\" de la salida (ver más abajo) y la convertimos en un valor flotante.

Ejemplo de salida de STREAM:

```bash
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:           24939.4     0.021905     0.021527     0.022382
Scale:          16956.3     0.031957     0.031662     0.032379
Add:            18648.2     0.044277     0.043184     0.046349
Triad:          19133.4     0.042935     0.042089     0.044283
```

Antes de ejecutar, observe el árbol de directorios que debe tener:

```bash
stream/
├── logs
├── src
│   └── stream.c
└── stream.py
```

Hagamos la prueba ahora:

``` bash
./bin/reframe -c stream.py -r --performance-report
```

La opción `--performance-report` generará un breve informe al final para cada prueba de 
rendimiento que se haya ejecutado.

```bash
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/../../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2/bin/reframe -c hello.py -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/../../t.800/Pruebas/stream'
  settings file:     '/LUSTRE/home/uam/../../t.800/.reframe/settings.py'
  check search path: '/LUSTRE/home/uam/../../t.800/Pruebas/stream/stream.py'
  stage directory:   '/LUSTRE/home/uam/../../t.800/Pruebas/stream/stage/'
  output directory:  '/LUSTRE/home/uam/../../t.800/Pruebas/stream/output/'

[==========] Running 1 check(s)
[==========] Started on Thu Jun 23 20:18:16 2022

[----------] started processing StreamTest (StreamTest)
[ RUN      ] StreamTest on yoltla:q1 using builtin-gcc-7.2.0
[----------] finished processing StreamTest (StreamTest)

[----------] waiting for spawned checks to finish
[       OK ] (1/1) StreamTest on yoltla:q1 using builtin-gcc-7.2.0 [compile: 0.595s run: 3.421s total: 4.104s]
[----------] all spawned checks have finished

[  PASSED  ] Ran 1/1 test case(s) from 1 check(s) (0 failure(s), 0 skipped)
[==========] Finished on Thu Jun 23 20:18:20 2022
==============================================================================
PERFORMANCE REPORT
------------------------------------------------------------------------------
StreamTest
- yoltla:q1
   - builtin-gcc-7.2.0
      * num_tasks: 1
      * Copy: 6606.1 MB/s
      * Scale: 6447.7 MB/s
      * Add: 9377.2 MB/s
      * Triad: 8648.0 MB/s
------------------------------------------------------------------------------
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/../../t.800/Pruebas/stream/logs/rfm.out', '/LUSTRE/home/uam/../../Pruebas/stream/logs/rfm.log'
```

## Valores de referencia

En su estado actual, la prueba de rendimiento STREAM anterior simplemente extraerá e 
informará las variables de rendimiento independientemente de los valores. Sin embargo, 
en algunas situaciones puede ser útil verificar que los valores de rendimiento extraídos 
estén dentro de un rango esperado e informar una falla cada vez que una prueba se 
desempeñe por debajo de las expectativas. Para ello, las pruebas ReFrame incluyen la variable 
[`reference`](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html#reframe.core.pipeline.RegressionTest.reference), 
que permite establecer referencias para cada una de las variables de rendimiento 
definidas en una prueba y también establecer diferentes referencias para diferentes 
sistemas o particiones. En el siguiente ejemplo establecemos los valores de referencia 
para todos los subpuntos de referencia de STREAM.

```admonish note title=" "
La optimización del rendimiento de las pruebas comparativas de STREAM está fuera del 
alcance de este tutorial.
```

```python
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher

@rfm.simple_test
class StreamTest(rfm.RegressionTest):
      # Se define sistema:particion donde se ejecuta
      valid_systems = ['yoltla:q1h-20p']

      # Se define archivo fuente presente en src
      sourcepath = 'stream.c'

      # Se define compilador a usar
      valid_prog_environs = ['builtin-gcc-7.2.0']

      # Se define tiempo límite de la prueba
      time_limit = '3m'

      # Se define el número de nodos, tareas, tareas por nodo, tareas por core
      num_nodes=1
      num_tasks_per_node = 1
      num_tasks = 1
      num_tasks_per_core = 1

      # Se define el comando para ejecutar la prueba
      executable = './stream'

      reference = {
        'yoltla:q1h-20p': {
            'Copy':  (6606.1, -0.05, 0.05, 'MB/s'),
            'Scale': (6447.7, -0.05, 0.05, 'MB/s'),
            'Add':   (9377.2, -0.05, 0.05, 'MB/s'),
            'Triad': (10648.0, -0.05, 0.05, 'MB/s')
        }
      }

      # Se establece el lanzador del job de forma local
      @run_before('run')
      def set_launcher(self):
          self.job.launcher = getlauncher('local')()

      # Función de sanidad
      @sanity_function
      def validate_solution(self):
          return sn.assert_found(r'Solution Validates', self.stdout)

      # Función de rendimiento
      @performance_function('MB/s')
      def Copy(self):
          return sn.extractsingle(r'Copy:\s+(\S+)\s+.*', self.stdout, 1, float)

      # Función de rendimiento
      @performance_function('MB/s')
      def Scale(self):
          return sn.extractsingle(r'Scale:\s+(\S+)\s+.*', self.stdout, 1, float)

      # Función de rendimiento
      @performance_function('MB/s')
      def Add(self):
          return sn.extractsingle(r'Add:\s+(\S+)\s+.*', self.stdout, 1, float)

      # Función de rendimiento
      @performance_function('MB/s', perf_key='Triad')
      def extract_triad_perf(self):
          return sn.extractsingle(r'Triad:\s+(\S+)\s+.*', self.stdout, 1, float)
```

Los valores de referencia se especifican como un diccionario basado en las variables de 
rendimiento definidas y en el ámbito de las combinaciones de sistema/partición. Los 
valores de referencia de rendimiento consta del valor deseado de referencia, los umbrales 
inferior y superior expresados como porcentajes en formato decimal relativos al valor de 
referencia y la unidad de medida.

``` admonish note title=" "
Si alguno de los umbrales no es relevante, `None` se puede utilizar en su lugar.
```

Para comprender mejor cómo configurar los valores de referencia de rendimiento, aquí hay 
algunos ejemplos con valores de referencia positivos y negativos:

| Valores de Rendimiento | Esperado | Más bajo | Más alto |
|------------------------|----------|----------|----------|
| `(100, -0.01, 0.02, 'MB/s')` | 100 MB/s        | 99 MB/s         | 102 MB/s        |
| `(100, -0.01, None, 'MB/s')` | 100 MB/s        | 99 MB/s         | inf MB/s        |
| `(100, None, 0.02, 'MB/s')`  | 100 MB/s        | -inf MB/s       | 102 MB/s        |
| `(-100, -0.01, 0.02, 'C')`   | -100C           | -101C           | -98C            |
| `(-100, -0.01, None, 'C')`   | -100C           | -101C           | Inf C           |
| `(-100, None, 0.02, 'C')`    | -100C           | -inf C          | -98C            |

Durante la etapa de rendimiento, los elementos de `reference`, excepto la unidad, se 
pasan a la función [`assert_reference()`](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html#reframe.utility.sanity.assert_reference) 
junto con el valor de rendimiento obtenido para evaluar realmente si la prueba pasa 
la verificación de rendimiento o no.

```admonish note title=" "
El nombre de los valores de referencia debe coincidir con el nombre de su función de 
rendimiento asociada. Sin embargo, se puede personalizar el nombre de la variable de 
rendimiento generada por `@performance_function` con el argumento `perf_key` como se 
muestra en el ejemplo anterior en la última función de performance.
```

Si cualquier valor de rendimiento obtenido está más allá de sus respectivos umbrales, 
la prueba fallará con un resumen como se muestra a continuación:

```bash
./bin/reframe -c stream.py -r --performance-report
```

```bash
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/../../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2/bin/reframe -c hello.py -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/../../t.800/Pruebas/stream'
  settings file:     '/LUSTRE/home/uam/../../t.800/.reframe/settings.py'
  check search path: '/LUSTRE/home/uam/../../t.800/Pruebas/stream/stream.py'
  stage directory:   '/LUSTRE/home/uam/../../t.800/Pruebas/stream/stage/'
  output directory:  '/LUSTRE/home/uam/../../t.800/Pruebas/stream/output/'

[==========] Running 1 check(s)
[==========] Started on Thu Jun 23 23:08:50 2022

[----------] started processing StreamTest (StreamTest)
[ RUN      ] StreamTest on yoltla:q1 using builtin-gcc-7.2.0
[----------] finished processing StreamTest (StreamTest)

[----------] waiting for spawned checks to finish
[     FAIL ] (1/1) StreamTest on yoltla:q1 using builtin-gcc-7.2.0 [compile: 0.613s run: 3.417s total: 4.117s]
==> test failed during 'performance': test staged in '/LUSTRE/home/uam/../../t.800/Pruebas/stream/stage/yoltla/q1h-20p/builtin-gcc-7.2.0/StreamTest'
[----------] all spawned checks have finished

[  FAILED  ] Ran 1/1 test case(s) from 1 check(s) (1 failure(s), 0 skipped)
[==========] Finished on Thu Jun 23 23:08:55 2022

==============================================================================
SUMMARY OF FAILURES
------------------------------------------------------------------------------
FAILURE INFO for StreamTest
  * Test Description: StreamTest
  * System partition: yoltla:q1
  * Environment: builtin-gcc-7.2.0
  * Stage directory: /LUSTRE/home/uam/../../t.800/Pruebas/stream/stage/23-06-2022/23-08-50/yoltla/q1h-20p/builtin-gcc-7.2.0/StreamTest
  * Node list: nc13
  * Job type: batch job (id=927000)
  * Dependencies (conceptual): []
  * Dependencies (actual): []
  * Maintainers: []
  * Failing phase: performance
  * Rerun with '-n StreamTest -p builtin-gcc-7.2.0 --system yoltla:q1h-20p -r'
  * Reason: performance error: failed to meet reference: Triad=8674.9, expected 10648.0 (l=10115.6, u=11180.4)
------------------------------------------------------------------------------
==============================================================================
PERFORMANCE REPORT
------------------------------------------------------------------------------
StreamTest
- yoltla:q1
   - builtin-gcc-7.2.0
      * num_tasks: 1
      * Copy: 6687.9 MB/s
      * Scale: 6511.4 MB/s
      * Add: 9462.3 MB/s
      * Triad: 8674.9 MB/s
------------------------------------------------------------------------------
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/../../t.800/Pruebas/stream/logs/rfm.out', '/LUSTRE/home/uam/../../Pruebas/stream/logs/rfm.log'
```

En este ejemplo, la prueba falla porque se esperaba otro valor para la variable Triad. 
Los demas valores entraron en el marguen esperado.

## Registros de rendimiento

ReFrame tiene un poderoso mecanismo para registrar sus actividades, así como los datos
de rendimiento. Admite diferentes tipos de canales de registro y puede enviar datos 
simultáneamente en cualquier de ellos. Por ejemplo, los datos de rendimiento pueden 
registrarse en archivos y, al mismo tiempo, enviarse a un log o a un servidor de 
administración de registros.

De forma predeterminada, es decir, a partir del archivo de configuración integrado, 
ReFrame envía datos de rendimiento a los archivos por prueba en el directorio `perflogs/`:

```bash
perflogs/
└── yoltla
    └── q1h-20p
        └── StreamTest.log
```

ReFrame crea un archivo de registro por prueba, por sistema y por partición y agrega los
registros cada vez que se ejecuta la prueba en esa combinación de sistema/partición. 
Inspeccionemos el archivo de registro de nuestras últimas pruebas:

```bash
2022-06-23T20:18:19|reframe 3.9.2|StreamTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=926963|Copy=6606.1|ref=0 (l=null, u=null)|MB/s
2022-06-23T20:18:19|reframe 3.9.2|StreamTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=926963|Scale=6447.7|ref=0 (l=null, u=null)|MB/s
2022-06-23T20:18:19|reframe 3.9.2|StreamTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=926963|Add=9377.2|ref=0 (l=null, u=null)|MB/s
2022-06-23T20:18:19|reframe 3.9.2|StreamTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=926963|Triad=8648.0|ref=0 (l=null, u=null)|MB/s
2022-06-23T23:08:53|reframe 3.9.2|StreamTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=927000|Copy=6687.9|ref=6606.1 (l=-0.05, u=0.05)|MB/s
2022-06-23T23:08:53|reframe 3.9.2|StreamTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=927000|Scale=6511.4|ref=6447.7 (l=-0.05, u=0.05)|MB/s
2022-06-23T23:08:53|reframe 3.9.2|StreamTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=927000|Add=9462.3|ref=9377.2 (l=-0.05, u=0.05)|MB/s
2022-06-23T23:08:53|reframe 3.9.2|StreamTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=927000|Triad=8674.9|ref=10648.0 (l=-0.05, u=0.05)|MB/s
```

Se imprime información diversa para cada ejecución, como las variables de rendimiento, 
su valor, sus referencias y umbrales, etc. El formato predeterminado está en una forma 
adecuada para un fácil análisis, pero puede controlar completamente no solo el formato, 
sino también lo que se está registrando desde el archivo de configuración.

Para obtener más información, consulte la sección [Configuración de Logging](../../reframe/anexos/archivo_configuracion.md#configuración-de-logging).


## Ejemplos avanzados

ReFrame ofrece operaciones complejas para definir, evaluar y administrar las funciones 
y variables de rendimiento de una forma más eficiente. Algunos ejemplos son:

## perf_variables = {} [¶](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html?highlight=performance#reframe.core.pipeline.RegressionTest.perf_variables)

- Las variables de rendimiento asociadas a la prueba.

En este contexto, una variable de rendimiento es una dupla de clave-valor, donde la 
clave es el nombre de la variable deseada y el valor es la expresión de rendimiento 
diferido, es decir, el resultado de una función de rendimiento diferible, que calcula 
o extrae el valor de la variable de rendimiento.

De forma predeterminada, ReFrame completa este campo durante la instanciación de la 
prueba con todas las funciones decoradas con el decorador `@performance_function`.

El siguiente ejemplo es una parcialidad de código donde se muestra el uso de `perf_variables`:

```python
    @performance_function('MB/s')
    def extract_bw(self, kind='Copy'):
        '''Funcion de extración de variables'''

        if kind not in ('Copy', 'Scale', 'Add', 'Triad'):
            raise ValueError(f'illegal value in argument kind ({kind!r})')

        return sn.extractsingle(rf'{kind}:\s+(\S+)\s+.*',self.stdout, 1, float)

    @run_before('performance')
    def set_perf_variables(self):
        '''Construye diccionario con todas las variables de performance.'''

        self.perf_variables = {
            'Copy': self.extract_bw(),
            'Scale': self.extract_bw('Scale'),
            'Add': self.extract_bw('Add'),
            'Triad': self.extract_bw('Triad'),
        }
```

El ejemplo anterior retoma las variables de performance de STREAM. Se destaca el uso de 
una sola función performance para extraer las variables en vez de usar múltiples funciones.

## reference = {} [¶](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html#reframe.core.pipeline.RegressionTest.reference)

- Comó se explico anteriormente, `reference` es el conjunto de valores de referencia 
para la prueba.

Los valores de referencia se especifican como un diccionario de ámbito basado en las 
variables de rendimiento definidas y en el ámbito de las combinaciones de `sistema/partición`.

Un ejemplo de uso en un sistema con múltiples particiones y arquitecturas diferentes 
es el siguiente:

```python
@rfm.simple_test
class Namd_CPU_Benchmarks(rfm.RunOnlyRegressionTest):

      ......

      allref = {
                1: {
                    'ivybridge':        {
                                         'Stmv':        (5.471,-0.50,0.15,'days/ns'),
                                         'F1atpase':    (1.487,-0.50,0.15,'days/ns')
                                        }
                   },
                4: {
                    'ivybridge':        {
                                         'Stmv':        (1.375,-0.50,0.15,'days/ns'),
                                         'F1atpase':    (0.374,-0.50,0.15,'days/ns')
                                        },
                    'haswell':          {
                                         'Stmv':        (1.486,-0.50,0.15,'days/ns'),
                                         'F1atpase':    (0.403,-0.50,0.15,'days/ns')
                                        },
                    'broadwell':        {
                                         'Stmv':        (1.531,-0.50,0.15,'days/ns'),
                                         'F1atpase':    (0.381,-0.50,0.15,'days/ns')
                                        }
                   }
               }
      ......

      @performance_function('days/ns')
      def Days_ns(self):
          return sn.avg(sn.extractall('Info: Benchmark time: \S+ CPUs \S+ ''s/step (?P<days_ns>\S+) days/ns \S+ MB memory',self.stdout,'days_ns', float))

      @run_before('run')
      def setup_run(self):

          ......

          # Setup performance
          self.reference = {
                            '*': {
                                  'Days_ns': self.allref[self.num_nodes][arch][self.bench_name]
                                 }
          }

          ......
```

El ejemplo anterior es una parcialidad de código de una prueba de la aplicación NAMD. 
En donde para todo sistema-partición (\*), `reference` busca los valores de referencia 
a partir de tres parametros: \[Número de nodos\]\[Arquitectura del nodo(s)\]\[Nombre 
del Benchmark usado\] en una lista (allref) previamente definida.

Este ejemplo usa otros elementos de ReFrame, sugerimos consultar la sección 
[Parámetros](../scripts/parametros.md) y [Topología](../anexos/topologia.md).

