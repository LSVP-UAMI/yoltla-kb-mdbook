# Descripción

Las pruebas de regresión en ReFrame son clases simples de Python que especifican los parámetros básicos de la prueba.

ReFrame cargará las pruebas y las enviará por un pipeline bien definido que las ejecutará en paralelo. Las etapas de esta canalización se encargan de todos los detalles de interacción del sistema, como el cambio de entorno de programación, la compilación, el envío de trabajos, la consulta del estado del trabajo, la verificación del estado y la evaluación del rendimiento.

# Estructura general

A continuación se presenta la estructura general de una prueba de ReFrame:

:::: formalpara
::: title
simple_test.py
:::

``` python
# Lista de imports necesarios para la prueba
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher
...

# Define una prueba de ReFrame
@rfm.simple_test
class Simple_Test(rfm.RegressionTest):
    # Descripción de la prueba
    descr = 'Simple Test'
    # Lista de sistemas y particiones en en que se ejecutará la prueba
    valid_systems = [
        'sistema_a:partición_1',
        'sistema_b:particion_3',
        'sistema_c:particion_5',
        ...
    ]
    # Lista de entornos de programación para la prueba
    # Un entorno de programación es esencialmente una
    # cadena de herramientas de compilación
    valid_prog_environs = [
        'entorno_1',
        'entorno_2',
        'entorno_3',
        .
        .
        .
    ]
    # Sistema que se utilizará para compilar el archivo fuente.
    # Algunas opciones son:
    #  * Make
    #  * SingleSource
    build_system = 'sistema_compilacion'
    # Archivo fuente a compilar
    sourcepath = 'archivo_fuente'

    # Número total de tareas para la prueba
    # Deben coincidir con la partición en que se ejecutará la prueba
    num_tasks = #
    # Número de tareas por nodo
    # Deben coincidir con los nodos en que se ejecutará la prueba
    num_tasks_per_node = #
    # Tiempo máximo de ejecución de la prueba
    # Sigue el formato días|horas|minutos|segundos, por ejemplo:
    #  * 1d12h
    #  * 6h45m
    #  * 15m30s
    time_limit = '#'

    # Lista de módulos a cargar para la prueba
    # Todos los módulos del cluster Yoltla pueden ser utilizados
    modules = [
        'moódulo_a',
        'módulo_b',
        'módulo_c',
        ...
    ]
    # Lista de comandos antes de ejecutar la prueba
    prerun_cmds = [
        'comando_1',
        'comando_2',
        'comando_3',
        ...
    ]
    # Lista de comandos despúes de ejecutar la prueba
    postrun_cmds = [
        'comando_1',
        'comando_2',
        'comando_3',
        ...
    ]
    # Comando para ejecutar la prueba, por ejemplo:
    #  * mpirun programa
    #  * ./programa
    executable = 'comando_ejecución'

    # Valores de referencia para determinar el rendimiento de la prueba
    reference = {
        'sistema_a:partición_1': {
            'variable_1': (#, -#, #, 'Unidades/x')
        },
        'sistema_b:particion_3': {
            'variable_2': (#, -#, #, 'Unidades/y')
        },
        'sistema_c:particion_5': {
            'variable_3': (#, -#, #, 'Unidades/z')
        },
        .
        .
        .
    }

    # Lista de nombres de los responsables del mantenimiento de la prueba
    maintainers = [
        'nombre_1',
        'nombre_2',
        'nombre_3',
        ...
    ]
    # Lista de etiquetas que identifican la prueba
    tags = {
        'etiqueta_1',
        'etiqueta_2',
        'etiqueta_3',
        ...
    }

    # Opciones de compilación
    @run_before('compile')
    def set_compilation_flags(self):
        # Lista de banderas que se utilizarán para compilar el archivo fuente
        self.build_system.cflags = [
            'opción_1',
            'opción_2',
            'opción_3',
            ...
        ]
        environ = self.current_environ.name

    # Opciones adicionales para el trabajo
    # El formato a seguir es el mismo que el de las directivas de SLURM,
    # por ejemplo:
    #   --nodelist=nc33
    @run_after('setup')
    def set_job_options(self):
        self.job.options = [
            '--opcion_1=valor_a',
            '--opcion_2=valor_b',
            '--opcion_3=valor_c',
            ...
        ]

    # Establece el lanzador para el trabajo
    @run_before('run')
    def set_launcher(self):
        self.job.launcher = getlauncher('lanzador')()

    # Prueba de sanidad
    @sanity_function
    def assert_tests_passed(self):
        return sn.assert_found(r'Test completed', self.stdout)

    # Variables de rendimiento
    @run_before('performance')
    def set_perf_vars(self):
        self.perf_variables = {
            'variable_1': sn.make_performance_function(
                sn.extractsingle(r'Variable 1:\s+(?P<variable_1>\S+)', self.stdout, 1, float),
                'Unidades/x'
            ),
            'variable_2': sn.make_performance_function(
                sn.extractsingle(r'Variable 2:\s+(?P<variable_2>\S+)', self.stdout, 1, float),
                'Unidades/y'
            ),
            'variable_3': sn.make_performance_function(
                sn.extractsingle(r'Variable 3:\s+(?P<variable_3>\S+)', self.stdout, 1, float),
                'Unidades/z'
            ),
            .
            .
            .
        }
```
::::

:::: note
::: title
:::

Como podrá haber observado, todas las funciones de la clase `Simple_Test` están decoradas. El [decorador](https://docs.python.org/3/glossary.html#term-decorator) de cada función le indica a ReFrame en que punto de su [pipeline](reframe/anexos/referencia_api.xml#pipeline) debe ejecutarla. Por ejemplo, en este fragmento de código:

        @run_before('performance')
        def set_perf_vars(self):
            self.perf_variables = {
                .
                .
                .
            }

el decorator `@run_before('performance')` indica a ReFrame que debe ejecutar la función `set_perf_vars` antes de la etapa de `performance`.

Para obtener más información de los decoradores, consulte la sección [Test Decorators](/reframe/anexos/referencia_api.xml#test_decorators).
::::

# Estructura de directorios

Además de nuestro script de ReFrame, debemos tener la estructura de directorios adecuada para nuestra prueba. A continuación se presenta la estructura general de directorios de una prueba de ReFrame:

    ├── simple_test         
    │   ├── simple_test.py  
    │   ├── logs            
    │   └── src             
    │       └── recurso_1
    │       └── recurso_2
    │       └── recurso_2
    │       └── ...

- Directorio de la prueba

- Prueba de ReFrame

- Directorio donde se guardarán los logs de la prueba

- En este directorio deben colocarse todos los recursos necesarios para la prueba:

  - Código fuente

  - Archivos de entrada

# Ejemplos

## Hello, World!

Dentro del directorio *reframe* cree la siguiente estructura de directorios:

    hello_world
    └── logs
    └── src

Posteriormente, cambie al directorio *reframe/hello_world*:

``` shell
[t.800@yoltla ~]$ cd reframe/hello_world/
[t.800@yoltla hello_world]$
```

y cree el archivo *hello_test.py*:

:::: formalpara
::: title
hello_test.py
:::

``` python
# Import necesario para definir pruebas de ReFrame
import reframe as rfm
# Import necesario para la función de sanidad
import reframe.utility.sanity as sn

# Decorador que define una prueba de ReFrame
@rfm.simple_test
class HelloTest(rfm.RegressionTest):
    # Descripción de la prueba
    descr = 'Hello, World!'
    # La prueba se ejecutará en el sistema yoltla, en la partición q1h-20p
    valid_systems = ['yoltla:q1h-20p']
    # ReFrame compilará el archivo fuente utilizando
    # el entorno de programación builtin-gcc-7.2.0
    valid_prog_environs = ['builtin-gcc-7.2.0']
    # Archivo fuente a compilar, por defecto,
    # el sourcepath es relativo al directorio src
    sourcepath = 'hello.c'

    # Número total de tareas
    num_tasks = 20
    # Número de tareas por nodo
    num_tasks_per_node = 20
    # Tiempo límite de ejecución
    time_limit = '1m'

    # Responsable del mantenimiento de la prueba
    maintainers = ['LSVP']
    # Etiquetas de la prueba
    tags = {'hello', 'world'}

    # Expresión regular que debe cumplir la prueba, en este caso el
    # output de la prueba debe contener la expresión:
    #  Hello, World!
    @sanity_function
    def assert_tests_passed(self):
        return sn.assert_found(r'Hello, World\!', self.stdout)
        # return sn.assert_found(r'Expresión regular de python', archivo)
        # archivo: Archivo donde buscará la expresión regular
        #   * self.stdout: Salida estándar de la prueba
```
::::

Dentro del directorio *src*, cree el archivo *hello.c*:

:::: formalpara
::: title
hello.c
:::

``` c
#include <stdio.h>

int main()
{
    printf("Hello, World!\n");
    return 0;
}
```
::::

El contenido del directorio *reframe* debe ser el siguiente:

    reframe
    ├── hello_world
    │   ├── hello_test.py
    │   ├── logs
    │   └── src
    │       └── hello.c
    └── settings.py

Para lanzar una prueba de ReFrame utilice el siguiente formato:

    reframe -c <directorio/archivo> -r

+-----------------------------------+-----------------------------------+
| Opción                            | Descripción                       |
+===================================+===================================+
| -c, \--checkpath=PATH             | Una ruta del sistema de archivos  |
|                                   | donde ReFrame debería buscar      |
|                                   | pruebas.\                         |
|                                   | PATH puede ser un directorio o un |
|                                   | solo archivo de prueba.           |
+-----------------------------------+-----------------------------------+
| -r, \--run                        | Ejecutar las pruebas              |
|                                   | seleccionadas.                    |
+-----------------------------------+-----------------------------------+

Para este ejemplo, utilice el comando:

``` shell
reframe -c hello_test.py -r
```

Al lanzar la prueba, se mostrará una salida como la siguiente:

``` shell
[t.800@yoltla hello_world]$ reframe -c hello_test.py -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c hello_test.py -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/hello_world'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/hello_world/hello_test.py'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/hello_world/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/hello_world/output'

[==========] Running 1 check(s)
[==========] Started on Tue Jun 21 11:53:54 2022

[----------] started processing HelloTest (Hello, World!)
[ RUN      ] HelloTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing HelloTest (Hello, World!)

[----------] waiting for spawned checks to finish
```

Está salida nos da información general de la prueba:

- version: Versión de ReFrame que se está utilizando

- command: Comando que se usó para lanzar la prueba

- launched by: Nombre del usuario que lanzó la prueba

- working directory: Directorio de trabajo de la prueba

- ...​

En este punto, la prueba se encuentra en el sistema de colas del cluster Yoltla esperando por los recursos necesarios para ser ejecutada.

Una vez que la prueba ha concluido, obtendremos la siguiente salida:

``` shell
[t.800@yoltla hello_world]$ reframe -c hello_test.py -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c hello_test.py -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/hello_world'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/hello_world/hello_test.py'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/hello_world/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/hello_world/output'

[==========] Running 1 check(s)
[==========] Started on Tue Jun 21 11:53:54 2022

[----------] started processing HelloTest (Hello, World!)
[ RUN      ] HelloTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing HelloTest (Hello, World!)

[----------] waiting for spawned checks to finish
[       OK ] (1/1) HelloTest on yoltla:q1h-20p using builtin-gcc-7.2.0 [compile: 1.697s run: 35.526s total: 37.283s]
[----------] all spawned checks have finished

[  PASSED  ] Ran 1/1 test case(s) from 1 check(s) (0 failure(s), 0 skipped)
[==========] Finished on Tue Jun 21 11:54:31 2022
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/.../t.800/reframe/hello_world/logs/rfm.out', '/LUSTRE/home/uam/.../t.800/reframe/hello_world/logs/rfm.log'
```

Esta salida nos indicá que la prueba fue exitosa.

:::: warning
::: title
:::

El criterio que utiliza ReFrame para determinar si una prueba concluyó con éxito, es la prueba de sanidad (*sanity check*). Por lo que todas las pruebas de ReFrame deben tener una función con el decorador `@sanity_function`.

Para obtener más información, consulte la sección [Pruebas de sanidad](reframe/scripts/pruebas_sanidad.xml).
::::

Al concluir la prueba, su árbol de directorios se verá como el siguiente:

    reframe
    ├── hello_world
    │   ├── hello_test.py
    │   ├── logs                                            
    │   │   ├── rfm.log
    │   │   ├── rfm.out
    │   │   └── run-report.json
    │   ├── output                                          
    │   │   └── yoltla
    │   │       └── q1h-20p
    │   │           └── builtin-gcc-7.2.0
    │   │               └── HelloTest
    │   │                   ├── rfm_HelloTest_build.sh      
    │   │                   ├── rfm_HelloTest_build.out     
    │   │                   ├── rfm_HelloTest_build.err     
    │   │                   └── rfm_HelloTest_job.sh        
    │   │                   ├── rfm_HelloTest_job.out       
    │   │                   ├── rfm_HelloTest_job.err       
    │   ├── __pycache__
    │   │   └── hello_test.cpython-38.pyc
    │   ├── src
    │   │   └── hello.c
    │   └── stage                                           
    │       └── yoltla
    │           └── q1h-20p
    │               └── builtin-gcc-7.2.0
    └── settings.py

- Directorio que almacena los logs de la prueba

- Directorio que almacena los scripts y archivos de salida/error de la prueba

- Script para compilar el archivo fuente

- Salida estándar de la compilación

- Error estándar de la compilación

- Script para ejecutar la prueba

- Salida estándar de la ejecución

- Error estándar de la ejecución

- Directorio que almacena temporalmente los recursos de la prueba

## Performance

Dentro del directorio *reframe* cree la siguiente estructura de directorios:

    prime_numbers
    ├── logs
    └── src

Posteriormente, cambie al directorio *reframe/prime_numbers*:

``` shell
[t.800@yoltla ~]$ cd reframe/prime_numbers/
[t.800@yoltla prime_numbers]$
```

y cree el archivo *prime_numbers_test.py*:

:::: formalpara
::: title
prime_numbers_test.py
:::

``` python
import reframe as rfm
import reframe.utility.sanity as sn
# Import necesario para la utilizar la función getlauncher
from reframe.core.backends import getlauncher

@rfm.simple_test
class PrimeNumbersTest(rfm.RegressionTest):
    # Descripción de la prueba
    descr = 'Prime numbers between 1 to 100000'
    # Sistemas y particiones en que se ejecutará la prueba
    valid_systems = ['yoltla:q1h-20p']
    # Entornos de programación para la prueba
    valid_prog_environs = ['builtin-gcc-7.2.0']
    # Archivo fuente a compilar
    sourcepath = 'prime_numbers.c'

    # Número total de tareas
    num_tasks = 20
    # Número de tareas por nodo
    num_tasks_per_node = 20
    # Tiempo límite de ejecución
    time_limit = '1m'

    # Comando para ejecutar la prueba
    # Por defecto, el entorno de programación utiliza el nombre de la clase
    # para nombrar al archivo compilado
    # En este ejemplo, ejecutaremos directamente el binario
    executable = './PrimeNumbersTest'

    # Valores de referencia
    # Se comparan con los valores obtenidos en la prueba
    reference = {
        'yoltla:q1h-20p': {
        # 'sistema:partición'
            'time': (0.65, -0.20, 0.20, 's')
            # 'id_rend': (var_esp, -umb_inf, umb_sup, 'unidad')
            #   * id_rend: Identificador de la variable de rendimiento
            #   * var_esp: Valor esperado
            #   * umb_inf: Umbral inferior (porcentaje)
            #   * umb_sup: Umbral superior (porcentaje)
            #   * unidad: Unidad de medida
        }
    }

    # Responsable del mantenimiento de la prueba
    maintainers = ['LSVP']
    # Etiquetas de la prueba
    tags = {'prime', 'numbers'}

    # Establece el lanzador como local, lo cual permite definir de manera
    # manual el comando para ejecutar la prueba
    @run_before('run')
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    # Prueba de sanidad
    @sanity_function
    def assert_tests_passed(self):
        return sn.assert_found(r'There are \d+ prime numbers between \d+ to \d+', self.stdout)

    # Variables de rendimiento
    # Se comparan con los valores de referencia
    @run_before('performance')
    def set_perf_vars(self):
        self.perf_variables = {
            'time': sn.make_performance_function(
                sn.extractsingle(r'The elapsed time is (?P<time>\S+) seconds', self.stdout, 1, float), 's'
            )
            # 'id_rend': sn.make_performance_function(
            #     sn.extractsingle(r'Expresión regular (?P<var_rend>\S+)', archivo, grupo, tipo), 'unidad'
            # )
            #   * id_rend: Identificador de la variable de rendimiento
            #   * var_rend: Valor de rendimiento a extraer
            #   * archivo: Archivo donde buscará la expresión regular
            #       ** self.stdout: Salida estándar de la prueba
            #   * grupo: Número del grupo de captura
            #       ** 1: Referencia al primer grupo de captura (var_rend)
            #   * tipo: Tipo de dato
            #   * unidad: Unidad de medida
        }
```
::::

Dentro del directorio *src*, cree el archivo *prime_numbers.c*:

:::: formalpara
::: title
prime_numbers.c
:::

``` c
#include <stdio.h>
#include <time.h>

int isPrime(int n) {
    if(n < 2)
        return 0;

    else {
        int lim = n/2;
        int i = 0;

        for(i = 2; i <= lim; i++) {
            if(n % i == 0)
                return 0;
        }
    }

    return 1;
}

int main() {
    double time_spent = 0.0;
    clock_t begin = clock();

    int i = 0;
    int count = 0;

    for(i = 1; i <= 100000; i++) {
        if(isPrime(i))
            count++;
    }

    i--;
    printf("There are %d prime numbers between 1 to %d\n", count, i);

    clock_t end = clock();
    time_spent += (double)(end - begin) / CLOCKS_PER_SEC;

    printf("\nThe elapsed time is %f seconds\n", time_spent);

    return 0;
}
```
::::

El contenido del directorio *prime_numbers* debe ser el siguiente:

``` shell
prime_numbers
├── logs
├── prime_numbers_test.py
└── src
    └── prime_numbers.c
```

Finalmente, lance la prueba con el comando:

``` shell
reframe -c prime_numbers_test.py -r
```

Al finalizar la prueba, debe obtener una salida como la siguiente:

``` shell
[t.800@yoltla prime_numbers]$ reframe -c prime_numbers_test.py -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c prime_numbers_test.py -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/prime_numbers_test.py'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/output'

[==========] Running 1 check(s)
[==========] Started on Tue Jun 21 23:25:51 2022

[----------] started processing PrimeNumbersTest (Prime numbers between 1 to 100000)
[ RUN      ] PrimeNumbersTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing PrimeNumbersTest (Prime numbers between 1 to 100000)

[----------] waiting for spawned checks to finish
[       OK ] (1/1) PrimeNumbersTest on yoltla:q1h-20p using builtin-gcc-7.2.0 [compile: 0.216s run: 123.626s total: 123.881s]
[----------] all spawned checks have finished

[  PASSED  ] Ran 1/1 test case(s) from 1 check(s) (0 failure(s), 0 skipped)
[==========] Finished on Tue Jun 21 23:27:55 2022
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/logs/rfm.out', '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/logs/rfm.log'
```

Como puede observar la salida de esta prueba es muy similar a la vista en el ejemplo anterior. La prueba terminó con éxito y no parece arrojarnos niguna información adicional, por lo que continuaremos con el análisis de su estructura de directorios.

Al concluir la prueba, su árbol de directorios se verá como el siguiente:

``` shell
prime_numbers/
├── logs
│   ├── rfm.log
│   ├── rfm.out
│   └── run-report.json
├── output
│   └── yoltla
│       └── q1h-20p
│           └── builtin-gcc-7.2.0
│               └── PrimeNumbersTest
│                   ├── rfm_PrimeNumbersTest_build.err
│                   ├── rfm_PrimeNumbersTest_build.out
│                   ├── rfm_PrimeNumbersTest_build.sh
│                   ├── rfm_PrimeNumbersTest_job.err
│                   ├── rfm_PrimeNumbersTest_job.out
│                   └── rfm_PrimeNumbersTest_job.sh
├── perflogs                                                
│   └── yoltla
│       └── q1h-20p
│           └── PrimeNumbersTest.log                        
├── prime_numbers_test.py
├── __pycache__
│   └── prime_numbers_test.cpython-38.pyc
├── src
│   └── prime_numbers.c
└── stage
    └── yoltla
        └── q1h-20p
            └── builtin-gcc-7.2.0
```

- Directorio en el que se almacenan los resultados de las pruebas de rendimiento

- Archivo con los resultados de la prueba de rendimiento

Es muy similar al visto en el ejemplo anterior, pero nos encontramos con un nuevo directorio, el directorio *perflogs*. En este directorio se almacenan los resultados del rendimiento de la prueba:

:::: formalpara
::: title
PrimeNumbersTest.log
:::

    2022-06-21T23:27:53|reframe 3.9.2|PrimeNumbersTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=926296|time=0.62|ref=0.65 (l=-0.2, u=0.2)|
::::

- \<año\>-\<mes\>-\<día\>T\<horas\>:\<minutos\>:\<segundos\> (Fecha y hora en que se completó la prueba)

- \<versión de ReFrame\>

- \<nombre de la prueba\> on \<sistema\>:\<partición\> using \<entorno de programación\>

- jobid=\<identificador del trabajo\>

- \<variable de rendimiento\>=\<valor obtenido\>

- ref=\<valor esperado\> (l=-\<umbral inferior\>, u=\<umbral superior\>)

Para obtener más información de las pruebas de rendimiento, consulte la sección [Pruebas de rendimiento](reframe/scripts/pruebas_rendimiento.xml).

## Tags

Hasta el momento hemos visto ejemplos de como lanzar pruebas de manera individual, sin embargo, cuando se tiene una gran cantidad de pruebas, probablemente deseemos lanzar múltiples pruebas con un solo comando. ReFrame implementa diferentes mecanismos que nos permiten realizar esta función, y uno de estos es el uso de etiquetas (`tags`). Las etiquetas nos permiten seleccionar y lanzar pruebas utilizando los valores declarados en la variable `tags`.

### **Ejemplo 1**

Dentro del directorio *reframe* cree la siguiente estructura de directorios y archivos:

    tags
    ├── hello_test.py
    ├── hola_test.py
    ├── logs
    └── src
        ├── hello.c
        └── hola.c

:::: formalpara
::: title
hello_test.py
:::

``` python
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class HelloTest(rfm.RegressionTest):
    # Descripción de la prueba
    descr = 'Hello!'
    # Sistemas y particiones en que se ejecutará la prueba
    valid_systems = ['yoltla:q1h-20p']
    # Entornos de programación para la prueba
    valid_prog_environs = ['builtin-gcc-7.2.0']
    # Archivo fuente a compilar
    sourcepath = 'hello.c'

    # Número total de tareas
    num_tasks = 20
    # Número de tareas por nodo
    num_tasks_per_node = 20
    # Tiempo límite de ejecución
    time_limit = '1m'

    # Comando para ejecutar la prueba
    executable = './hello'

    # Responsable del mantenimiento de la prueba
    maintainers = ['LSVP']
    # Etiquetas de la prueba
    tags = {'greetings', 'america', 'hello'}

    # Establece el lanzador para el trabajo
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    # Prueba de sanidad
    @sanity_function
    def assert_tests_passed(self):
        return sn.assert_found(r'Hello!', self.stdout)
```
::::

:::: formalpara
::: title
hello.c
:::

``` python
#include <stdio.h>

int main()
{
    printf("Hello!\n");
    return 0;
}
```
::::

:::: formalpara
::: title
hola_test.py
:::

``` python
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class HolaTest(rfm.RegressionTest):
    # Descripción de la prueba
    descr = '¡Hola!'
    # Sistemas y particiones en que se ejecutará la prueba
    valid_systems = ['yoltla:q1h-20p']
    # Entornos de programación para la prueba
    valid_prog_environs = ['builtin-gcc-7.2.0']
    # Archivo fuente a compilar
    sourcepath = 'hola.c'

    # Número total de tareas
    num_tasks = 20
    # Número de tareas por nodo
    num_tasks_per_node = 20
    # Tiempo límite de ejecución
    time_limit = '1m'

    # Comando para ejecutar la prueba
    executable = './hola'

    # Responsable del mantenimiento de la prueba
    maintainers = ['LSVP']
    # Etiquetas de la prueba
    tags = {'greetings', 'america', 'hola'}

    # Establece el lanzador para el trabajo
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    # Prueba de sanidad
    @sanity_function
    def assert_tests_passed(self):
        return sn.assert_found(r'Hola!', self.stdout)
```
::::

:::: formalpara
::: title
hola.c
:::

``` c
#include <stdio.h>

int main()
{
    printf("Hola!\n");
    return 0;
}
```
::::

Posteriormente, cambie al directorio *reframe/tags*:

``` shell
[t.800@yoltla ~]$ cd reframe/tags/
[t.800@yoltla tags]$
```

En este ejemplo tenemos dos pruebas de ReFrame, con sus respectivos recursos, en un mismo directorio, y nos interesa lanzar ambas pruebas. En primer instancia, podemos pensar en simplemente lanzar primero la prueba *hello_test.py* y posteriormente la prueba *hola_test.py*, lo cual es una solución válida, sin embargo, si nos encontraramos en un escenario donde fuera necesario lanzar 100 pruebas, esto puede volverse complicado. Una alternativa a lanzar las pruebas de forma individual es utilizar etiquetas (`tags`).

Para lanzar pruebas utilizando etiquetas, siga el formato:

    reframe -c <directorio/archivo> -t <etiqueta>  -r

+-----------------------------------+-----------------------------------+
| Opción                            | Descripción                       |
+===================================+===================================+
| -c, \--checkpath=PATH             | Una ruta del sistema de archivos  |
|                                   | donde ReFrame debería buscar      |
|                                   | pruebas.\                         |
|                                   | PATH puede ser un directorio o un |
|                                   | solo archivo de prueba.           |
+-----------------------------------+-----------------------------------+
| -t, \--tag=TAG                    | Filtrar pruebas por etiqueta.     |
+-----------------------------------+-----------------------------------+
| -r, \--run                        | Ejecutar las pruebas              |
|                                   | seleccionadas.                    |
+-----------------------------------+-----------------------------------+

:::: note
::: title
:::

TAG se interpreta como una [expresión regular](https://docs.python.org/3/library/re.html) de Python; se seleccionarán todas las pruebas que tengan al menos una etiqueta coincidente.

Esta opción se puede especificar varias veces, en cuyo caso solo se seleccionarán las pruebas que definan o coincidan con todas las etiquetas.
::::

Para este ejemplo, utilice el comando:

``` shell
reframe -c . -t greetings -r
```

Con el cual lanzará todas las pruebas que tengan la etiqueta \'greetings\':

``` shell
[t.800@yoltla tags]$ reframe -c . -t greetings  -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c . -t greetings -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/tags'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/tags'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/tags/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/tags/output'

[==========] Running 2 check(s)
[==========] Started on Fri Jul 22 07:25:04 2022

[----------] started processing HolaTest (¡Hola!)
[ RUN      ] HolaTest on yoltla:q1d-20p using builtin-gcc-7.2.0
[----------] finished processing HolaTest (¡Hola!)

[----------] started processing HelloTest (Hello!)
[ RUN      ] HelloTest on yoltla:q1d-20p using builtin-gcc-7.2.0
[----------] finished processing HelloTest (Hello!)

[----------] waiting for spawned checks to finish
```

Una vez que las pruebas hayan concluido, tendrá la siguiente salida:

``` shell
[t.800@yoltla tags]$ reframe -c . -t greetings -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c . -t greetings -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/tags'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/tags'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/tags/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/tags/output'

[==========] Running 2 check(s)
[==========] Started on Fri Jul 22 07:25:04 2022

[----------] started processing HolaTest (¡Hola!)
[ RUN      ] HolaTest on yoltla:q1d-20p using builtin-gcc-7.2.0
[----------] finished processing HolaTest (¡Hola!)

[----------] started processing HelloTest (Hello!)
[ RUN      ] HelloTest on yoltla:q1d-20p using builtin-gcc-7.2.0
[----------] finished processing HelloTest (Hello!)

[----------] waiting for spawned checks to finish
[       OK ] (1/2) HolaTest on yoltla:q1d-20p using builtin-gcc-7.2.0 [compile: 1.944s run: 7120.166s total: 7122.172s]
[       OK ] (2/2) HelloTest on yoltla:q1d-20p using builtin-gcc-7.2.0 [compile: 0.296s run: 7180.096s total: 7180.448s]
[----------] all spawned checks have finished

[  PASSED  ] Ran 2/2 test case(s) from 2 check(s) (0 failure(s), 0 skipped)
[==========] Finished on Fri Jul 22 09:24:46 2022
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/.../t.800/reframe/tags/logs/rfm.out', '/LUSTRE/home/uam/.../t.800/reframe/tags/logs/rfm.log'
```

### **Ejemplo 2**

Utilizando el mismo directorio *tags* del ejemplo anterior, cree la siguiente estructura de directorios y archivos:

    tags/
    ├── hello_test.py
    ├── hola_test.py
    ├── konnichiwa_test.py
    ├── namaste_test.py
    ├── logs
    └── src
        ├── hello.c
        ├── hola.c
        ├── konnichiwa.c
        └── namaste.c

:::: formalpara
::: title
konnichiwa_test.py
:::

``` python
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class KonnichiwaTest(rfm.RegressionTest):
    # Descripción de la prueba
    descr = 'Konnichiwa!'
    # Sistemas y particiones en que se ejecutará la prueba
    valid_systems = ['yoltla:q1h-20p']
    # Entornos de programación para la prueba
    valid_prog_environs = ['builtin-gcc-7.2.0']
    # Archivo fuente a compilar
    sourcepath = 'konnichiwa.c'

    # Número total de tareas
    num_tasks = 20
    # Número de tareas por nodo
    num_tasks_per_node = 20
    # Tiempo límite de ejecución
    time_limit = '1m'

    # Comando para ejecutar la prueba
    executable = './konnichiwa'

    # Responsable del mantenimiento de la prueba
    maintainers = ['LSVP']
    # Etiquetas de la prueba
    tags = {'greetings', 'asia', 'konnichiwa'}

    # Establece el lanzador para el trabajo
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    # Prueba de sanidad
    @sanity_function
    def assert_tests_passed(self):
        return sn.assert_found(r'Konnichiwa!', self.stdout)
```
::::

:::: formalpara
::: title
konnichiwa.c
:::

``` c
#include <stdio.h>

int main()
{
    printf("Konnichiwa!\n");
    return 0;
}
```
::::

:::: formalpara
::: title
namaste_test.py
:::

``` python
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class NamasteTest(rfm.RegressionTest):
    # Descripción de la prueba
    descr = 'Namaste!'
    # Sistemas y particiones en que se ejecutará la prueba
    valid_systems = ['yoltla:q1h-20p']
    # Entornos de programación para la prueba
    valid_prog_environs = ['builtin-gcc-7.2.0']
    # Archivo fuente a compilar
    sourcepath = 'namaste.c'

    # Número total de tareas
    num_tasks = 20
    # Número de tareas por nodo
    num_tasks_per_node = 20
    # Tiempo límite de ejecución
    time_limit = '1m'

    # Comando para ejecutar la prueba
    executable = './namaste'

    # Responsable del mantenimiento de la prueba
    maintainers = ['LSVP']
    # Etiquetas de la prueba
    tags = {'greetings', 'asia', 'namaste'}

    # Establece el lanzador para el trabajo
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    # Prueba de sanidad
    @sanity_function
    def assert_tests_passed(self):
        return sn.assert_found(r'Namaste!', self.stdout)
```
::::

:::: formalpara
::: title
namaste.c
:::

``` c
#include <stdio.h>

int main()
{
    printf("Namaste!\n");
    return 0;
}
```
::::

Ya hemos visto que gracias a las etiquetas podemos lanzar múltiples pruebas de manera simultánea, sin embargo, puede que por diversos motivos no nos interese lanzar las pruebas que contengan cierta etiqueta, es decir, queremos exlcuir pruebas.

Para lanzar pruebas excluyendo etiquetas, siga el formato:

    reframe -c <directorio/archivo> -T <etiqueta>  -r

+-----------------------------------+-----------------------------------+
| Opción                            | Descripción                       |
+===================================+===================================+
| -c, \--checkpath=PATH             | Una ruta del sistema de archivos  |
|                                   | donde ReFrame debería buscar      |
|                                   | pruebas.\                         |
|                                   | PATH puede ser un directorio o un |
|                                   | solo archivo de prueba.           |
+-----------------------------------+-----------------------------------+
| -T, \--exclude-tag=TAG            | Excluir pruebas por etiqueta.     |
+-----------------------------------+-----------------------------------+
| -r, \--run                        | Ejecutar las pruebas              |
|                                   | seleccionadas.                    |
+-----------------------------------+-----------------------------------+

:::: note
::: title
:::

TAG se interpreta como una [expresión regular](https://docs.python.org/3/library/re.html) de Python; se excluirá cualquier prueba con etiquetas que coincidan con TAG.

Esta opción se puede especificar varias veces, en cuyo caso se excluirán las pruebas con cualquiera de las etiquetas especificadas.
::::

Para este ejemplo, utilice el comando:

    reframe -c . -t greetings -T hello -r

Con el cual lanzará todas las pruebas que tengan la etiqueta \'greetings\', pero no la etiqueta \'hello\':

``` shell
[t.800@yoltla tags]$ reframe -c . -t greetings -T hello -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c . -t greetings -T hello -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/tags'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/tags'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/tags/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/tags/output'

[==========] Running 3 check(s)
[==========] Started on Fri Jul 22 07:25:22 2022

[----------] started processing NamasteTest (Namaste!)
[ RUN      ] NamasteTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing NamasteTest (Namaste!)

[----------] started processing KonnichiwaTest (Konnichiwa!)
[ RUN      ] KonnichiwaTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing KonnichiwaTest (Konnichiwa!)

[----------] started processing HolaTest (¡Hola!)
[ RUN      ] HolaTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing HolaTest (¡Hola!)

[----------] waiting for spawned checks to finish
```

Una vez que las pruebas hayan concluido, tendrá la siguiente salida:

``` shell
[t.800@yoltla tags]$ reframe -c . -t greetings -T hello -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c . -t greetings -T hello -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/tags'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/tags'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/tags/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/tags/output'

[==========] Running 3 check(s)
[==========] Started on Fri Jul 22 07:25:22 2022

[----------] started processing NamasteTest (Namaste!)
[ RUN      ] NamasteTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing NamasteTest (Namaste!)

[----------] started processing KonnichiwaTest (Konnichiwa!)
[ RUN      ] KonnichiwaTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing KonnichiwaTest (Konnichiwa!)

[----------] started processing HolaTest (¡Hola!)
[ RUN      ] HolaTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing HolaTest (¡Hola!)

[----------] waiting for spawned checks to finish
[       OK ] (1/3) NamasteTest on yoltla:q1h-20p using builtin-gcc-7.2.0 [compile: 0.318s run: 7225.883s total: 7226.263s]
[       OK ] (2/3) KonnichiwaTest on yoltla:q1h-20p using builtin-gcc-7.2.0 [compile: 0.298s run: 7286.627s total: 7286.981s]
[       OK ] (3/3) HolaTest on yoltla:q1h-20p using builtin-gcc-7.2.0 [compile: 0.311s run: 7341.376s total: 7341.741s]
[----------] all spawned checks have finished

[  PASSED  ] Ran 3/3 test case(s) from 3 check(s) (0 failure(s), 0 skipped)
[==========] Finished on Fri Jul 22 09:27:45 2022
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/.../t.800/reframe/tags/logs/rfm.out', '/LUSTRE/home/uam/.../t.800/reframe/tags/logs/rfm.log'
```

# Errores

Hasta el momento hemos escrito y ejecutado varias pruebas de ReFrame de manera exitosa, sin embargo, esto no siempre es así.

## Prueba de sanidad

``` shell
[t.800@yoltla hello_world]$ reframe -c hello_test.py -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c hello_test.py -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/hello_world'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/hello_world/hello_test.py'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/hello_world/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/hello_world/output'

[==========] Running 1 check(s)
[==========] Started on Tue Jun 21 11:59:45 2022

[----------] started processing HelloTest (Hello, World!)
[ RUN      ] HelloTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing HelloTest (Hello, World!)

[----------] waiting for spawned checks to finish
[     FAIL ] (1/1) HelloTest on yoltla:q1h-20p using builtin-gcc-7.2.0 [compile: 0.435s run: 31989.472s total: 31989.965s]
==> test failed during 'sanity': test staged in '/LUSTRE/home/uam/.../t.800/reframe/hello_world/stage/yoltla/q1h-20p/builtin-gcc-7.2.0/HelloTest'
[----------] all spawned checks have finished

[  FAILED  ] Ran 1/1 test case(s) from 1 check(s) (1 failure(s), 0 skipped)
[==========] Finished on Tue Jun 21 20:52:55 2022

==============================================================================
SUMMARY OF FAILURES
------------------------------------------------------------------------------
FAILURE INFO for HelloTest
  * Test Description: Hello, World!
  * System partition: yoltla:q1h-20p
  * Environment: builtin-gcc-7.2.0
  * Stage directory: /LUSTRE/home/uam/.../t.800/reframe/hello_world/stage/yoltla/q1h-20p/builtin-gcc-7.2.0/HelloTest
  * Node list: nc63
  * Job type: batch job (id=926064)
  * Dependencies (conceptual): []
  * Dependencies (actual): []
  * Maintainers: ['LSVP']
  * Failing phase: sanity
  * Rerun with '-n HelloTest -p builtin-gcc-7.2.0 --system yoltla:q1h-20p -r'
  * Reason: sanity error: pattern 'Hello, World\\!' not found in 'rfm_HelloTest_job.out'
------------------------------------------------------------------------------
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/.../t.800/reframe/hello_world/logs/rfm.out', '/LUSTRE/home/uam/.../t.800/reframe/hello_world/logs/rfm.log'
```

En este ejemplo, podemos observar que a diferencia de las salidas vistas anteriormente, esta salida nos da información más detallada sobre la ejecución de nuestra prueba, en particular nos interesa saber la razón del porque la prueba falló. En este caso, ReFrame nos indica que fue debido a un error en la función de sanidad:

      * Reason: sanity error: pattern 'Hello, World\\!' not found in 'rfm_HelloTest_job.out'

Existen dos razones principales para que falle la función de sanidad:

- La expresión regular para la prueba de sanidad es incorrecta

- La prueba alcanzó el tiempo límite de ejecución, y no terminó adecuadamente

En este ejemplo, la prueba falló porque el archivo fuente fue modificado:

:::: formalpara
::: title
hello.c
:::

``` c
#include <stdio.h>

int main()
{
    printf("Hola, Mundo!\n");
    return 0;
}
```
::::

pero la expresión regular de la función de sanidad no fue actualizada:

``` python
    @sanity_function
    def assert_tests_passed(self):
        return sn.assert_found(r'Hello, World\!', self.stdout)
```

:::: note
::: title
:::

Como ya se mencionó anteriormente, todos los recursos de la prueba se almacenan en el directorio *stage* de manera temporal, estos recursos incluyen los archivos fuente y compilados, y cualquier otro archivo que se haya generado durante la prueba. Cuando la prueba concluye con éxito, los scripts y archivos de salida/error son movidos al directorio *output*, el resto de archivos son eliminados. Sin embargo, cuando la prueba falla, todos los recursos permanecen en el directorio *stage*:

``` shell
hello_world
├── hello_test.py
├── logs
│   ├── rfm.log
│   ├── rfm.out
│   └── run-report.json
├── output
│   └── yoltla
│       └── q1h-20p
│           └── builtin-gcc-7.2.0
│               └── HelloTest
├── __pycache__
│   └── hello_test.cpython-38.pyc
├── src
│   └── hello.c
└── stage
    └── yoltla
        └── q1h-20p
            └── builtin-gcc-7.2.0
                └── HelloTest
                    ├── hello.c
                    ├── HelloTest
                    ├── rfm_HelloTest_build.err
                    ├── rfm_HelloTest_build.out
                    ├── rfm_HelloTest_build.sh
                    ├── rfm_HelloTest_job.err
                    ├── rfm_HelloTest_job.out
                    └── rfm_HelloTest_job.sh
```
::::

## Prueba de rendimiento

``` shell
[t.800@yoltla prime_numbers]$ reframe -c prime_numbers_test.py -r
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe -C /LUSTRE/home/uam/.../t.800/reframe/settings.py -c prime_numbers_test.py -r
'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers'
  settings file:     '/LUSTRE/home/uam/.../t.800/reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/prime_numbers_test.py'
  stage directory:   '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/output'

[==========] Running 1 check(s)
[==========] Started on Tue Jun 21 23:32:35 2022

[----------] started processing PrimeNumbersTest (Prime numbers between 1 to 100000)
[ RUN      ] PrimeNumbersTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing PrimeNumbersTest (Prime numbers between 1 to 100000)

[----------] waiting for spawned checks to finish
[     FAIL ] (1/1) PrimeNumbersTest on yoltla:q1h-20p using builtin-gcc-7.2.0 [compile: 0.279s run: 21.230s total: 21.563s]
==> test failed during 'performance': test staged in '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/stage/yoltla/q1
d-20p/builtin-gcc-7.2.0/PrimeNumbersTest'
[----------] all spawned checks have finished

[  FAILED  ] Ran 1/1 test case(s) from 1 check(s) (1 failure(s), 0 skipped)
[==========] Finished on Tue Jun 21 23:32:56 2022

==============================================================================
SUMMARY OF FAILURES
------------------------------------------------------------------------------
FAILURE INFO for PrimeNumbersTest
  * Test Description: Prime numbers between 1 to 100000
  * System partition: yoltla:q1h-20p
  * Environment: builtin-gcc-7.2.0
  * Stage directory: /LUSTRE/home/uam/.../t.800/reframe/prime_numbers/stage/yoltla/q1h-20p/builtin-gcc-7.2.0/PrimeNumb
ersTest
  * Node list: nc13
  * Job type: batch job (id=926299)
  * Dependencies (conceptual): []
  * Dependencies (actual): []
  * Maintainers: ['LSVP']
  * Failing phase: performance
  * Rerun with '-n PrimeNumbersTest -p builtin-gcc-7.2.0 --system yoltla:q1h-20p -r'
  * Reason: performance error: failed to meet reference: time=1.36, expected 0.65 (l=0.52, u=0.78)
------------------------------------------------------------------------------
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/logs/rfm.out', '/LUSTRE/home/uam/.../t.800/reframe/prime_numbers/logs/rfm.log'
```

De manera similar al ejemplo anterior, la salida nos da información detallada sobre la ejecución de nuestra prueba, en particular nos interesa saber la razón del porque la prueba falló. En este caso, ReFrame nos indica que fue debido a un error en la función de rendimiento:

      * Reason: performance error: failed to meet reference: time=1.36, expected 0.65 (l=0.52, u=0.78)

Existen tres razones principales para que falle la función de rendimiento:

- La expresión regular para extraer el valor de rendimiento es incorrecta

- El identificador de la variable de rendimiento no es el mismo en la función de rendimiento y en la variable `reference`

- La prueba no obtuvo el rendimiento esperado

En este ejemplo, la prueba no obtuvo el rendimiento que se esperaba:

:::: formalpara
::: title
PrimeNumbersTest.log
:::

    2022-06-21T23:32:54|reframe 3.9.2|PrimeNumbersTest on yoltla:q1h-20p using builtin-gcc-7.2.0|jobid=926299|time=1.36|ref=0.65 (l=-0.2, u=0.2)|s
::::
