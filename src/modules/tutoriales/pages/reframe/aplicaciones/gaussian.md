# Descripción

[Gaussian](http://gaussian.com/) es un paquete de química computacional con varios métodos para calcular
propiedades de sistemas moleculares y periódicos, usando descripciones mecánico-cuánticas estándar para
las funciones de onda o la densidad electrónica.

- Esta trabajo se realizo con Gaussian 09-sse4.

- Benchmarks: test979 y test 1044

# Gaussian Execution Environment

Gaussian localiza ejecutables y crea archivos temporales en directorios especificados por varias
variables de entorno. El usuario es responsable de definir dos de ellos:

`g09root` : indica el directorio donde reside el subdirectorio g09.

`GAUSS_SCRDIR` :Indica el directorio que se debe utilizar para los archivos temporales.

# Parallel Gaussian

Hay dos niveles de paralelización en Gaussian: memoria compartida y distribuida. Tenga en cuenta que la
versión disponible en Yoltla no tiene el componente de paralelización de Linda para la ejecución
distribuida de Gaussian. Sin embargo, la ejecución paralela está disponible dentro de un solo nodo,
utilizando el parámetro `%NProcShared` en el archivo de entrada de Gaussian. Por ejemplo, para ejecutar
con nodos de 20 núcleos, agregue la siguiente línea en la parte superior de su archivo de entrada
gaussiana:

    %NProcShared=20

Algunos trabajos, pueden consumir grandes recursos de memoria. Para trabajos muy grandes, podría
considerar establecer el parámetro de Gaussian09, `%Mem` , que afecta la cantidad de memoria disponible
para producir un buen rendimiento general.

Al determinar un valor para la variable `%Mem`, permita al menos un valor de 500 MB de memoria total.
De lo contrario, el job tendrá problemas, posiblemente morirá y, en algunos casos, hará que el nodo se
caiga.

:::: note
::: title
:::

La versión de Gaussian instalada en Yoltla sólo permite utilizar paralelización de memoria
compartida, por lo que los trabajos que utilicen esta aplicación, deberán enviarse a particiones con un
sólo nodo.
::::

# Gaussian Performance

`Gaussian` no tiene una variable de performance como tal, en cambio muestra estadísticas de recursos
utilizados como el tiempo de cpu o memoria utilizada. Para este trabajo, para medir el performance y la
eficiencia paralela de `Gaussian`, usaremos el tiempo de cpu para calcular los tiempos de ejecución.

:::: formalpara
::: title
Ejemplo de salida exitosa de Gaussian
:::

     Job cpu time:       0 days  0 hours 48 minutes 26.9 seconds.
     File lengths (MBytes):  RWF=    182 Int=      0 D2E=      0 Chk=     13 Scr=      1
     Normal termination of Gaussian 09 at Mon Aug  1 19:00:15 2022.
::::

# Eficiencia Paralela

La única forma confiable de ver si un trabajo escala de manera eficiente es compararlo. Comparar un
trabajo significa ejecutar un trabajo de prueba breve y representativo varias veces en diferentes
números de CPU para encontrar un punto óptimo.

A partir de estos datos, se puede calcular la **eficiencia paralela**. Esto se define cómo:

E = (1/P) \* (T~1~/T~P~)

- P = Numero de procesadores

- T~1~ = tiempo óptimo para el algoritmo en un procesador

- T~P~ = tiempo para algoritmo paralelo en P procesadores

Como regla general, los trabajos que se ejecutan con una gran cantidad de núcleos deben tener
una eficiencia paralela superior o igual a 0,7.

# Test Jobs

Un extenso conjunto de test jobs es proporcionado por Gaussian, junto con sus correspondientes
archivos de salida. Los archivos de entrada se encuentran en el directorio `g09root/g09/tests/com`.

Los archivos de entrada de trabajos de prueba tienen nombres con el formato `test_nnnn_.com`.
El archivo `g09root/g09/tests/tests.idx` enumera lo que hace cada trabajo de prueba.

## test0979 (Junio 2022)

Test0979: NBO test with f functions

![](Reframe/Apps/Gaussian/Figure_0979.png){alt="Figure 0979"}

+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| **\#    | **CPU's Nodos nc\          | **CPU's Nodos              | **CPU's Nodos              |
| Cores** | 20 Cores x 2.50GHz Intel   | ttv1\[1-58\]\              | ttv2\[59-104\]\            |
|         | Xeón E5-2670v2\            | 20 Cores x 2.60GHz Intel   | 32 Cores x 2.10GHz Intel   |
|         | 64GB RAM\                  | Xeón E5-2660v3\            | Xeon E5-2683v4\            |
|         | Infiniband FDR10/FDR**     | 128GB RAM\                 | 256GB RAM\                 |
|         |                            | Infiniband FDR10/FDR**     | Infiniband FDR10/FDR**     |
|         +-------------+--------------+-------------+--------------+-------------+--------------+
|         | **time      | **Eficiencia | **time      | **Eficiencia | **time      | **Eficiencia |
|         | (seconds)** | Paralela %** | (seconds)** | Paralela %** | (seconds)** | Paralela %** |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 1       | 1895.314    | 100.0 %      | 2052.557    | 100.0 %      | 2480.583    | 100.0 %      |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 2       | 999.707     | 94.8 %       | 1041.206    | 98.6 %       | 1240.281    | 100.0 %      |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 4       | 533.439     | 88.8 %       | 546.997     | 93.8 %       | 651.619     | 95.2 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 8       | 310.036     | 76.4 %       | 294.713     | 87.1 %       | 361.331     | 85.8 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 16      | 173.288     | 68.4 %       | 228.473     | 56.1 %       | 202.973     | 76.4 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 20      | 152.121     | 62.3 %       | 152.093     | 67.5 %       |             |              |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 32      |             |              |             |              | 156.012     | 49.7 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+

: Performance Test 0979

Para este Benchmarks, observamos un uso eficiente de los recursos entre 8 y 16 cores de cada partición.

## test1044 (Junio 2022)

Test1044: TD 50-50 with PCM test

![](Reframe/Apps/Gaussian/Figure_1044.png){alt="Figure 1044"}

+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| **\#    | **CPU's Nodos nc\          | **CPU's Nodos              | **CPU's Nodos              |
| Cores** | 20 Cores x 2.50GHz Intel   | ttv1\[1-58\]\              | ttv2\[59-104\]\            |
|         | Xeón E5-2670v2\            | 20 Cores x 2.60GHz Intel   | 32 Cores x 2.10GHz Intel   |
|         | 64GB RAM\                  | Xeón E5-2660v3\            | Xeon E5-2683v4\            |
|         | Infiniband FDR10/FDR**     | 128GB RAM\                 | 256GB RAM\                 |
|         |                            | Infiniband FDR10/FDR**     | Infiniband FDR10/FDR**     |
|         +-------------+--------------+-------------+--------------+-------------+--------------+
|         | **time      | **Eficiencia | **time      | **Eficiencia | **time      | **Eficiencia |
|         | (seconds)** | Paralela %** | (seconds)** | Paralela %** | (seconds)** | Paralela %** |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 1       | 1868.443    | 100.0 %      | 2117.750    | 100.0 %      | 3104.160    | 100.0 %      |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 2       | 958.971     | 97.4 %       | 1068.356    | 99.1 %       | 1628.442    | 95.3 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 4       | 463.332     | 100.8 %      | 539.453     | 98.1 %       | 815.336     | 95.2 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 8       | 242.975     | 96.1 %       | 263.012     | 100.6 %      | 415.186     | 93.5 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 16      | 129.552     | 90.1 %       | 141.716     | 93.4 %       | 210.299     | 92.3 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 20      | 105.539     | 88.5 %       | 119.133     | 88.9 %       |             |              |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 32      |             |              |             |              | 116.476     | 83.3 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+

: Performance Test 1044

Para este Benchmarks, observamos que Gaussian hace un uso eficiente de los recursos disponibles
escalando apropiadamente.

# Referencias

[Gaussian Main Site](http://gaussian.com/)

[Link 0 Commands](https://gaussian.com/link0/)

[Running Gaussian](https://gaussian.com/running/)

[RUNNING GAUSSIAN 09 JOBS MORE EFFICIENTLY](https://nusit.nus.edu.sg/services/hpc-newsletter/running-gaussian-09-jobs-more-efficiently/)
