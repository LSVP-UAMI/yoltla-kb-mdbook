# Descripción

Durante la fase sanidad, se verifica el estado de la salida de la prueba. ReFrame no hace
ninguna suposición de lo que es una prueba exitosa; ni siquiera busca por defecto algo en 
particular en la salida. Esto depende totalmente de la prueba por definir. ReFrame 
proporciona una forma flexible y expresiva de especificar patrones y operaciones 
complejas que se realizarán en la salida de la prueba para determinar la \"cordura\" de 
la prueba.

```admonish warning title=" "
Toda prueba de regresión siempre debe tener una función con el decorador `@sanity_function` 
como parte de la prueba. Esta función se convierte en una expresión de evaluación que 
afirma la salud de la prueba.
```

# Ejemplos

En el siguiente ejemplo, la función de sanidad especificada verifica que el ejecutable 
haya producido la frase deseada en la salida estándar de la prueba.

```admonish info title=" "
Tenga en cuenta que ReFrame no determina el éxito de una prueba por su código de salida.
En cambio, la evaluación del éxito es responsabilidad de la prueba misma.
```

<span style="color: red;">*hello.c*</span>

```c
#include <stdio.h>

int main()
{
    printf("Hello, World!\n");
    return 0;
}
```

<span style="color: red;">*HelloTest.py*</span>

```python
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class HelloTest(rfm.RegressionTest):
      valid_systems = ['yoltla:q1h-20p']
      valid_prog_environs = ['builtin-gcc-7.2.0']
      sourcepath = 'hello.c'

      num_tasks = 1
      num_tasks_per_node = 1
      time_limit = '1m'

      @sanity_function
      def assert_hello(self):
          return sn.assert_found(r'Hello, World\!', self.stdout)
```

Una prueba de ReFrame debe definir un ejecutable para ejecutar o un archivo fuente 
(o código fuente) para compilar. En este ejemplo, basta con definir el archivo fuente
de nuestro programa. ReFrame conoce el ejecutable que se produjo y lo usará para 
ejecutar la prueba.

Nuestra función de sanidad esta identificada por el decorador `@sanity_function`. Esta 
función se convierte en una expresión de evaluación perezosa que afirma la "cordura" 
de la prueba.

```admonish info title=" "
La expresion de evaluación es una [expresión regular](https://docs.python.org/3/library/re.html) 
de Python. Y se usa para buscar una cadena de caracteres en la salida.
```

Toda función de sanidad debe regresar un valor booleano (True). Esto se explicará más 
adelante, por el momento se destaca el uso de la [función diferible](#funciones-diferibles) 
[`sn.assert_found`](./pruebas_sanidad.md#reframeutilitysanityassert_foundpatt-filename-msgnone-encodingutf-8-¶) 
que afirma la existencia de una cadena. Esta función se hereda de la clase `sanity`:

```bash
import reframe.utility.sanity as sn
```

Antes de ejecutar la prueba, revise la estructura de directorios que debe tener:

```bash
hello
├── hello.py
├── src/
│    └── hello.c
└── logs/
```

Ahora es el momento de ejecutar nuestra prueba:

```bash
./bin/reframe -c hello.py -r
```

Lo que producirá la siguiente salida:

```bash
[ReFrame Setup]
  version:           3.9.2
  command:           '/LUSTRE/home/uam/../../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2/bin/reframe -c hello.py -r'
  launched by:       t.800@yoltla.supercomputo.izt.uam.mx
  working directory: '/LUSTRE/home/uam/../../t.800/Pruebas/HolaMundo'
  settings file:     '/LUSTRE/home/uam/../../t.800/.reframe/settings.py'
  check search path: '/LUSTRE/home/uam/../../t.800/Pruebas/HolaMundo/hello.py'
  stage directory:   '/LUSTRE/home/uam/../../t.800/Pruebas/HolaMundo/stage/'
  output directory:  '/LUSTRE/home/uam/../../t.800/Pruebas/HolaMundo/output/'

[==========] Running 1 check(s)
[==========] Started on Wed Jun 22 23:39:12 2022

[----------] started processing HelloTest (HelloTest)
[ RUN      ] HelloTest on yoltla:q1h-20p using builtin-gcc-7.2.0
[----------] finished processing HelloTest (HelloTest)

[----------] waiting for spawned checks to finish
[       OK ] (1/1) HelloTest on yoltla:q1h-20p using builtin-gcc-7.2.0 [compile: 3.780s run: 2.977s total: 6.843s]
[----------] all spawned checks have finished

[  PASSED  ] Ran 1/1 test case(s) from 1 check(s) (0 failure(s), 0 skipped)
[==========] Finished on Wed Jun 22 23:39:19 2022
Run report saved in 'logs/run-report.json'
Log file(s) saved in '/LUSTRE/home/uam/../../t.800/Pruebas/HolaMundo/logs/rfm.out', '/LUSTRE/home/uam/../../t.800/Pruebas/HolaMundo/logs/rfm.log'
```

La prueba ha verificado que se produjo la salida deseada y ha sido exitosa, hemos 
verificado que tenemos un compilador de C en funcionamiento en nuestro sistema. Si 
todo ha salido bien, puede verificar el resultado en la carpeta *output*.

# Comprobación avanzada

Hasta ahora, solo hemos visto una búsqueda similar a `grep`, pero las funcion de sanidad
son mucho más que esto. De hecho, uno podría prácticamente hacer casi cualquier 
operación en la salida y procesarla como quisiera antes de evaluar la \"cordura\" de la 
prueba. A continuación describiremos algunas operaciones de sanidad útiles.

## Funciones Diferibles

Las funciones de sanidad y sus operaciones entran en la categoría de funciones diferibles
de ReFrame.

Las funciones diferibles son las funciones cuya ejecución puede posponerse a un momento 
posterior después de su llamada. La característica clave de estas funciones es que 
almacenan sus argumentos cuando se les llama, y la ejecución en sí no ocurre hasta que 
la función se evalúa explícita o implícitamente.

Para obtener más información, consulte la sección 
[Deferrable Functions Reference](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html#deferrable-functions-reference) de la documentación oficial de ReFrame.

### **Lista de funciones y utilidades**

#### reframe.utility.sanity.abs(x) [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.abs)
- Calcula el valor absoluto de x

#### reframe.utility.sanity.all(iterable) [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.all)
- Lista de múltiples pruebas de sanidad

#### reframe.utility.sanity.assert_eq(a, b, msg=None) [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.assert_eq)
- Confirma que `a == b`.

    **Parámetros:**
    
    - **a y b** : Variables a comparar.

    - **msg** : El mensaje de error que se utilizará si la confirmación falla. Opcional.

    **Regresa:**

    `True` si tiene éxito.

    **Plantea:**

    `reframe.core.exceptions.SanityError` -- si falla.


#### reframe.utility.sanity.assert_found(patt, filename, msg=None, encoding=\'utf-8\') [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.assert_found)
- Comprueba que el patrón de expresiones regulares `patt` se encuentra en el archivo `filename`.

    **Parámetros:**

    - **patt** : El patrón de expresión regular para buscar.Se acepta cualquier 
    expresión regular estándar de Python.

    - **filename** : El nombre del archivo a examinar.

    - **msg** : El mensaje de error que se utilizará si la confirmación falla. Opcional

    - **encodig** : El nombre de la codificación utilizada para decodificar el archivo. 
    Opcional.

    **Regresa:**

    `True` si tiene éxito.

    **Plantea:**

    `reframe.core.exceptions.SanityError` -- si falla.


####  reframe.utility.sanity.assert_lt(a, b, msg=None)\] [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.assert_lt)
- Confirma que `a < b`.

    **Parámetros:**

    - **a y b** : Variables a comparar.

    - **msg** : El mensaje de error que se utilizará si la confirmación falla. Opcional.

    **Regresa:**

    `True` si tiene éxito.

    **Plantea:**

    `reframe.core.exceptions.SanityError` -- si falla.


#### reframe.utility.sanity.assert_ne(a, b, msg=None) [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.assert_ne)
- Confirma que `a != b`.

    **Parámetros:**

    - **a y b** : Variables a comparar.

    - **msg** : El mensaje de error que se utilizará si la confirmación falla. Opcional.

    **Regresa:**

    `True` si tiene éxito.

    **Plantea:**

    `reframe.core.exceptions.SanityError` -- si falla.


#### reframe.utility.sanity.assert_not_found(patt, filename, msg=None, encoding=\'utf-8\') [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.assert_not_found)
- Comprueba que el patrón de expresiones regulares `patt` no se encuentra en el archivo `filename`.

    **Parámetros:**

    - **patt** : El patrón de expresión regular para buscar.Se acepta cualquier 
    expresión regular estándar de Python.

    - **filename** : El nombre del archivo a examinar.

    - **msg** : El mensaje de error que se utilizará si la confirmación falla. Opcional

    - **encodig** : El nombre de la codificación utilizada para decodificar el archivo. 
    Opcional.

    **Regresa:**

    `True` si tiene éxito.

    **Plantea:**

    `reframe.core.exceptions.SanityError` -- si falla.


#### reframe.utility.sanity.avg(iterable) [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.avg)
- Devuelve el promedio de todos los elementos de `iterable`.

#### reframe.utility.sanity.count(iterable) [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.count)
- Devuelve el recuento de elementos de `iterable`.


#### reframe.utility.sanity.extractall(patt, filename, tag=0, conv=None, encoding=\'utf-8\') [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.extractall)
- Extrae todos los valores del grupo de captura `tag` de una expresión regular coincidente `patt` en el archivo filename\`.

    **Parámetros:**

    - **patt** : El patrón de expresión regular para buscar. Se acepta cualquier 
    expresión regular estándar de Python.

    - **filename** : El nombre del archivo a examinar.

    - **encodig** : El nombre de la codificación utilizada para decodificar el archivo. Opcional.

    - **tag** : El grupo de captura de expresiones regulares que se va a extraer.

    - **conv** : Función de conversión de los valores extraídos.

    **Regresa:**

    Una lista de valores convertidos extraídos de los grupos de captura especificados en `tag`.

    **Plantea:**

    `reframe.core.exceptions.SanityError` -- si falla.


#### reframe.utility.sanity.extractsingle(patt, filename, tag=0, conv=None, item=0, encoding=\'utf-8\') [¶](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#reframe.utility.sanity.extractsingle)
- Extrae un valor del grupo de captura `tag` de una expresión regular coincidente `patt` en el archivo `filename`.

    **Parámetros:**

    - **patt** : El patrón de expresión regular para buscar. Se acepta cualquier 
    expresión regular estándar de Python.

    - **filename** : El nombre del archivo a examinar.

    - **encodig** : El nombre de la codificación utilizada para decodificar el archivo. Opcional.

    - **tag** : El grupo de captura de expresiones regulares que se va a extraer.

    - **item** : El numero del elemento especifico a extraer. Valor -1 extrae el último.


ReFrame tiene muchas más funciones útiles, que puede consultar en la sección 
[List of deferrable functions and utilities](https://reframe-hpc.readthedocs.io/en/stable/deferrable_functions_reference.html?highlight=sanity.all#list-of-deferrable-functions-and-utilities) 
de la documentación oficial de ReFrame.

```admonish info title=" "
Una función de sanidad **verifica** la presencia de patrones y elementos, por lo tanto 
debe ser explícita en cuanto al valor que regresa (un booleano). Si la función de 
sanidad no se puede resolver debido a una sintaxis ambigua, se marcará el error 
[reframe.core.exceptions.ReframeSyntaxError](https://reframe-hpc.readthedocs.io/en/stable/exceptions.html#reframe.core.exceptions.ReframeSyntaxError).
```

# Ejemplos avanzados

Ahora que hemos visto operaciones avanzadas de las funciones de sanidad, podemos 
analizar ejemplos más complejos.

El siguiente ejemplo pertenece a una función de sanidad de una prueba de la aplicación 
Namd.

```python
@sanity_function
def assert_step_num(self):
    energy = sn.avg(sn.extractall(r'ENERGY:([ \t]+\S+){10}[ \t]+(?P<energy>\S+)',self.stdout,'energy',float))

    energy_reference = -725159.11
    energy_tolerance = 300

    energy_diff = sn.abs(energy - energy_reference)

    return sn.assert_lt(energy_diff,energy_tolerance)
```

Esta prueba analiza una salida Namd cómo la siguiente:

```bash
ETITLE:      TS           BOND          ANGLE          DIHED          IMPRP
          ELECT            VDW       BOUNDARY           MISC        KINETIC
          TOTAL           TEMP         TOTAL2         TOTAL3        TEMPAVG
       PRESSURE      GPRESSURE         VOLUME       PRESSAVG      GPRESSAVG
```

Salida:

```bash
ENERGY:    9996    108140.4062     81521.6814     16177.1220      1722.7921
  -1335678.7673    112536.7841         0.0000         0.0000    290425.4924
   -725154.4891       297.5011  -1015579.9816   -722577.7165       297.5011
       348.5550       163.1747   3104392.8098       348.5550       163.1747

ENERGY:    9997    108061.8062     81667.0452     16169.8824      1721.5431
  -1335791.0959    112556.9911         0.0000         0.0000    290465.6266
   -725148.2014       297.5422  -1015613.8280   -722543.2055       297.5422
       304.1737       161.3509   3104392.8098       304.1737       161.3509

ENERGY:    9998    108373.7883     81798.0534     16165.9493      1718.4754
  -1335967.4030    112577.6787         0.0000         0.0000    290204.5390
   -725128.9190       297.2748  -1015333.4580   -722544.8914       297.2748
       216.5664       160.7425   3104392.8098       216.5664       160.7425

ENERGY:    9999    108790.3699     81866.1842     16165.2348      1713.4982
  -1336153.5789    112590.8997         0.0000         0.0000    289924.9586
   -725102.4334       296.9884  -1015027.3920   -722547.1299       296.9884
       123.4770       159.9664   3104392.8098       123.4770       159.9664
```

La función de de sanidad busca obtener el promedio de energia de la variable `TOTAL`, 
después compara el resultado con un valor esperado y si el valor entra en un margen de 
tolerancia la prueba es existosa.

Para lograr lo anterior la función de sanidad realiza los siguientes pasos:

1.  Se define una expresión regular que filtre la variable deseada:
```bash
    r'ENERGY:([ \t]+\S+){10}[ \t]+(?P<energy>\S+)'
```

2.  Con la función `sn.extractall` se define que se buscará el patrón en la salida 
estándar y se guardará el valor en la variable \'energy\' que es de tipo `float`. 
La función creará una lista con los valores obtenidos.

3.  Con la función `sn.avg` se obtiene un promedio de los valores.

4.  Con la funcion `sn.abs` se obtiene el valor absoluto de la diferencia entre el 
promedio de la energía obtenida con la energía promedio esperada.

5.  Se regresa el valor de la función `sn.assert.lt`. La prueba es exitosa si la energía 
entra en el margen de tolerancia: `energy_diff < energy_tolerance`, en este caso 
`sn.assert.lt` regresa True, falla la prueba en caso contrario.

## Múltiples pruebas de sanidad

Con ayuda de la funcion `sn.all` se puede definir una lista de múltiples pruebas de 
sanidad a cumplir, usando el ejemplo anterior, modificamos el código de la siguiente forma:

```python
@sanity_function
def assert_step_num(self):
    energy = sn.avg(sn.extractall(r'ENERGY:([ \t]+\S+){10}[ \t]+(?P<energy>\S+)',self.stdout,'energy',float))

    energy_reference = -725159.11
    energy_tolerance = 300

    energy_diff = sn.abs(energy - energy_reference)

    return sn.all([
        sn.assert_eq(sn.count(sn.extractall(r'TIMING: (?P<step_num>\S+)  CPU:',self.stdout,'step_num')),500),
        sn.assert_lt(energy_diff,energy_tolerance)
    ])
```

Esta función de sanidad ahora evalua dos pruebas a cumplir, si cualquiera de estas falla
la prueba se marcará como fallida.
