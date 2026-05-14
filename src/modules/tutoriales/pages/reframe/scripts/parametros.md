# Descripción

Cualquier prueba ReFrame se convierte en una parametrizada si el usuario define parámetros dentro del cuerpo de la clase de la prueba. Esto se hace usando la función [`parameter()`](https://reframe-hpc.readthedocs.io/en/stable/regression_test_api.html?highlight=parameter#reframe.core.builtins.parameter) integrada en ReFrame, que acepta una la lista de valores de parámetros.

Para cada valor de parámetro, ReFrame instanciará una prueba de regresión **diferente** al asignar el valor correspondiente a un atributo con el nombre del parámetro.

Para obtener más información, consulte la sección [Parameterizing a Regression Test](https://reframe-hpc.readthedocs.io/en/stable/tutorial_advanced.html#parameterizing-a-regression-test) de la documentación oficial de ReFrame.

# Ejemplos

Vamos a ejecutar el siguiente codigo en C de MPI:

:::: formalpara
::: title
hola_mpi.c
:::

``` c
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

typedef char cadena[256];

int id,size,lenc;
cadena maquina;

void help(int id){
     printf("Hola Mundo, soy %d de %d en maq:%s \n",id,size,maquina);
}

int main(int argc,char *argv[]){
    MPI_Init(&argc,&argv);

    MPI_Comm_rank(MPI_COMM_WORLD,&id);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Get_processor_name(maquina,&lenc);

    help(id);

    MPI_Finalize();

    return 0;
}
```
::::

Utilizamos el siguiente script de ReFrame para lanzar las pruebas:

:::: formalpara
::: title
hello_mpi.py
:::

``` python
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher

@rfm.simple_test
class HelloTest(rfm.RegressionTest):
    valid_systems = ['yoltla:q1h-20p']

    valid_prog_environs = ['builtin-openmpi-2.1.5']

    tareas = parameter([2, 4, 8, 16, 20])

    sourcepath = 'hola_mpi.c'

    nodes = 1

    time = '2m'

    @run_before('run')
    def replace_launcher(self):
        self.job.launcher = getlauncher('mpirun')()

        # Se define número de tareas mpi
        self.num_tasks = self.tareas
        self.num_tasks_per_node = self.tareas

    @sanity_function
    def assert_hello(self):
        return sn.assert_found(r'Hola Mundo, soy \d+ de \d+ en maq:\S+ ', self.stdout)
```
::::

En este ejemplo, ReFrame generará automáticamente 5 pruebas con diferentes valores para el atributo tareas, el cual se utiliza para inicializar las variables `num_tasks` y `num_tasks_per_node`. Esto permite adaptar la prueba en función de los valores del parámetro, como lo hacemos en este caso, donde ejecutamos un mismo codigo MPI con diferentes cantidad de procesos en un nodo.

Antes de ejecutar, enumeremos las pruebas generadas:

    reframe -c hello_mpi.py -l

    Opciones:
      -l lista las pruebas presentes en un script

Salida:

``` bash
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

Confirmamos que ReFrame genera 5 pruebas a partir de una única prueba parametrizada. Al enumerar las pruebas parametrizadas, ReFrame agrega la lista de parámetros después del nombre de la prueba base, así cada prueba generada
también recibe un nombre único.

Para obtener más detalles sobre cómo se generan los nombres de las pruebas para varios tipos de pruebas, consulte la sección [Test Naming Scheme](https://reframe-hpc.readthedocs.io/en/stable/manpage.html#test-naming-scheme) de la la documentación oficial de ReFrame.

:::: note
::: title
:::

El nombre único está formado por el nombre de la clase de prueba seguido de un `_` y el valor del parámetro. Por cada elemento en los parámetros de la prueba se obtendra un nombre único.
::::

Ejecutemos la prueba:

    reframe -c hello_mpi.py -r

Salida:

``` bash
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/../../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2/bin/reframe -c hello_mpi.py -l'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/../../Pruebas/parametros'
  settings file:     '/LUSTRE/home/uam/../../t.800/.reframe/settings.py'
  check search path: '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/hello_mpi.py'
  stage directory:   '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/stage/'
  output directory:  '/LUSTRE/home/uam/../../t.800/Pruebas/parametros/output/'

[==========] Running 5 check(s)
[==========] Started on Sat Jun 25 00:01:52 2022

[----------] started processing HelloTest_20 (HelloTest_20)
[ RUN      ] HelloTest_20 on yoltla:q1h-20p using builtin-openmpi-2.1.5
[----------] finished processing HelloTest_20 (HelloTest_20)

[----------] started processing HelloTest_16 (HelloTest_16)
[ RUN      ] HelloTest_16 on yoltla:q1h-20p using builtin-openmpi-2.1.5
[----------] finished processing HelloTest_16 (HelloTest_16)

[----------] started processing HelloTest_8 (HelloTest_8)
[ RUN      ] HelloTest_8 on yoltla:q1h-20p using builtin-openmpi-2.1.5
[----------] finished processing HelloTest_8 (HelloTest_8)

[----------] started processing HelloTest_4 (HelloTest_4)
[ RUN      ] HelloTest_4 on yoltla:q1h-20p using builtin-openmpi-2.1.5
[----------] finished processing HelloTest_4 (HelloTest_4)

[----------] started processing HelloTest_2 (HelloTest_2)
[ RUN      ] HelloTest_2 on yoltla:q1h-20p using builtin-openmpi-2.1.5
[----------] finished processing HelloTest_2 (HelloTest_2)

[----------] waiting for spawned checks to finish
[       OK ] (1/5) HelloTest_8 on yoltla:q1h-20p using builtin-openmpi-2.1.5 [compile: 21.582s run: 42.816s total: 64.477s]
[       OK ] (2/5) HelloTest_20 on yoltla:q1h-20p using builtin-openmpi-2.1.5 [compile: 21.658s run: 84.787s total: 106.531s]
[       OK ] (3/5) HelloTest_16 on yoltla:q1h-20p using builtin-openmpi-2.1.5 [compile: 19.584s run: 65.351s total: 85.021s]
[       OK ] (4/5) HelloTest_4 on yoltla:q1h-20p using builtin-openmpi-2.1.5 [compile: 19.683s run: 23.787s total: 43.549s]
[       OK ] (5/5) HelloTest_2 on yoltla:q1h-20p using builtin-openmpi-2.1.5 [compile: 21.603s run: 57.855s total: 79.537s]
[----------] all spawned checks have finished

[  PASSED  ] Ran 5/5 test case(s) from 5 check(s) (0 failure(s), 0 skipped)
[==========] Finished on Sat Jun 25 00:04:35 2022
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/../../t.800/Pruebas/parametro/logs/rfm.out', '/LUSTRE/home/uam/../../t.800/Pruebas/parametro/logs/rfm.log'
```

Confirmamos que ReFrame ejecutó 5 pruebas distintas a partir de una única prueba. La parametrización de pruebas en ReFrame es muy poderosa ya que puede parametrizar sus pruebas en cualquier cosa y puede crear espacios de parametrización complejos.

## Ejecución por parámetro

ReFrame permite filtrar las pruebas por diferentes atributos y existen opciones de línea de comandos específicas para lograrlo. Como vimos, ReFrame asigna un nombre único por parámetro que identifica la prueba, de modo que podemos escoger que parámetro queremos ejecutar.

Para el ejemplo anterior, tenemos 5 pruebas posibles:

``` bash
- HelloTest_20
- HelloTest_16
- HelloTest_2
- HelloTest_8
- HelloTest_4
```

Suponiendo que queremos ejecutar solo 4 procesos MPI. Utilizamos la opción `-n, --name=NAME`:

    reframe -c hello_mpi.py -n HelloTest_4 -r

Esto ejecutara solo una prueba especifica.

:::: note
::: title
:::

La opción `-n, --name` filtra las pruebas por nombre. NAME se interpreta como una expresión regular de Python; se seleccionará cualquier prueba cuyo nombre coincida con NOMBRE.
::::

ReFrame al interpretar [expresiónes regulares](https://docs.python.org/3/library/re.html) de Python nos permite escoger múltiples pruebas especificas. Por ejemplo, si queremos ejecutar 2 y 20 procesos en el ejemplo anterior, ejecutamos:

    reframe -c hello_mpi.py -n HelloTest_2.*? -r

## Múltiples parámetros

En el siguiente ejemplo, utilizamos una combinación de parámetros para definir el número de nodos y número de tareas por nodo para el ejemplo Hola Mundo MPI.

:::: formalpara
::: title
hello_mpi.py
:::

``` python
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher

@rfm.simple_test
class HelloTest(rfm.RegressionTest):
    valid_prog_environs = ['builtin-openmpi-2.1.5']

    tareas = parameter([8, 16, 20])

    sourcepath = 'hola_mpi.c'

    num_nodes = parameter([1,2])

    time = '2m'

    @run_after('init')
    def setup_system(self):
      valid_systems = {
        1: ['yoltla:q1d-20p'],
        2: ['yoltla:q1d-40p']
      }

      try:
        self.valid_systems = valid_systems[self.num_nodes]
      except KeyError:
        self.valid_systems = []

    @run_before('run')
    def replace_launcher(self):
      self.job.launcher = getlauncher('mpirun')()

      # Se define número de tareas mpi
      self.num_tasks_per_node = self.tareas
      self.num_tasks = self.num_nodes*self.tareas

    @sanity_function
    def assert_hello(self):
      return sn.assert_found(r'Hola Mundo, soy \d+ de \d+ en maq:\S+ ', self.stdout)
```
::::

Esto lanza una combinación de pruebas, que se ilustra en la siguiente tabla:

+----------------------+----------------------+-----------------------+
| Número de Nodos      | No. tareas total     | No. tareas por nodo   |
+======================+======================+=======================+
| 1                    | 8                    | 8                     |
+----------------------+----------------------+-----------------------+
| 1                    | 16                   | 16                    |
+----------------------+----------------------+-----------------------+
| 1                    | 20                   | 20                    |
+----------------------+----------------------+-----------------------+
| 2                    | 16                   | 8                     |
+----------------------+----------------------+-----------------------+
| 2                    | 32                   | 16                    |
+----------------------+----------------------+-----------------------+
| 2                    | 40                   | 20                    |
+----------------------+----------------------+-----------------------+

Así puede crear y administrar multiples pruebas.

## Etiquetas

Es posible combinar parámetros y etiquetas en una misma prueba, como se puede ver en el siguiente ejemplo:

:::: formalpara
::: title
hello_mpi.py
:::

``` python
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher

@rfm.simple_test
class HelloTest(rfm.RegressionTest):
    valid_prog_environs = ['builtin-openmpi-2.1.5']

    tareas = parameter([8, 16, 20])

    sourcepath = 'hola_mpi.c'

    num_nodes = parameter([1,2])

    time = '2m'

    @run_after('init')
    def setup_system(self):
      valid_systems = {
          1: ['yoltla:q1d-20p'],
          2: ['yoltla:q1d-40p']
      }

      try:
          self.valid_systems = valid_systems[self.num_nodes]
      except KeyError:
          self.valid_systems = []

      # Se definen las etiquetas de la prueba
      self.tags = {f'HelloTest-{self.num_nodes}-{self.tareas}'}

    @run_before('run')
    def replace_launcher(self):
      self.job.launcher = getlauncher('mpirun')()

      # Se define número de tareas mpi
      self.num_tasks_per_node = self.tareas
      self.num_tasks = self.num_nodes*self.tareas

    @sanity_function
    def assert_hello(self):
      return sn.assert_found(r'Hola Mundo, soy \d+ de \d+ en maq:\S+ ', self.stdout)
```
::::

Para enumerar la lista de etiquetas de la prueba, ejecute el comando:

``` shell
reframe -c hello_mpi.py --list-tags

Opciones:
  --list-tags Enumera las etiquetas únicas de las pruebas seleccionadas
```

Salida:

``` shell
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/../../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2/bin/reframe -c hello_mpi.py --list-tags'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/.../t.800/Pruebas/etiquetas'
  settings file:     '/LUSTRE/home/uam/../../t.800/.reframe/settings.py'
  check search path: '/LUSTRE/home/uam/.../t.800/Pruebas/etiquetas/hello_mpi.py'
  stage directory:   '/LUSTRE/home/uam/.../t.800/Pruebas/etiquetas/stage'
  output directory:  '/LUSTRE/home/uam/.../t.800/Pruebas/etiquetas/output'

[List of unique tags]
'HelloTest-1-16', 'HelloTest-1-20', 'HelloTest-1-8', 'HelloTest-2-16', 'HelloTest-2-20', 'HelloTest-2-8'
Found 6 tag(s)

Log file(s) saved in '/LUSTRE/home/uam/.../t.800/Pruebas/etiquetas/logs/rfm.out', '/LUSTRE/home/uam/.../t.800/Pruebas/etiquetas/logs/rfm.log'
```

Para obtener más información sobre el uso de las etiquetas, consulte la sección [Tags](reframe/scripts/scripts.xml#tags).
