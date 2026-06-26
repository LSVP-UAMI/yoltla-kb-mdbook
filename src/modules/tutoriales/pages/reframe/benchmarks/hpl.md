# HPL


## Descripción

HPL es un paquete de software que resuelve un sistema lineal denso (aleatorio)
en aritmética de doble precisión (64 bits) en computadoras con memoria distribuida. 
Por lo tanto, se puede considerar como una implementación portátil y de libre 
acceso de High Performance Computing Linpack Benchmark.

El paquete HPL proporciona un programa de prueba y cronometraje para cuantificar 
la precisión de la solución obtenida, así como el tiempo necesario para calcularla.

Para obtener más información, visite el sitio oficial de [HPL](https://netlib.org/benchmark/hpl/).


## Archivo de entrada

HPL necesita un archivo de entrada para poder ejecutarse, por defecto HPL buscará
este archivo con el nombre *HPL.dat*. A continuación se presenta un ejemplo de este archivo:

<span style="color: #990819;">*HPL.dat*</span>

```bash

HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out     output file name (if any)
6           device out (6=stdout,7=stderr,file)
2           # of problems sizes (N)
3000 6000   Ns
3           # of NBs
80 100 120  NBs
0           MAP process mapping (0=Row-,1=Column-major)
2           # of process grids (P x Q)
1 2         Ps
6 8         Qs
16.0        threshold
1           # of panel fact<
2           PFACTs (0=left, 1=Crout, 2=Right)
1           # of recursive stopping criterium
4           NBMINs (>= 1)
1           # of panels in recursion
2           NDIVs
1           # of recursive panel fact.
1           RFACTs (0=left, 1=Crout, 2=Right)
1           # of broadcast
1           BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1           # of lookahead depth
1           DEPTHs (>=0)
2           SWAP (0=bin-exch,1=long,2=mix)
64          swapping threshold
0           L1 in (0=transposed,1=no-transposed) form
0           U in (0=transposed,1=no-transposed) form
1           Equilibration (0=no,1=yes)
8           memory alignment in double (> 0)
```

Este archivo consta de 31 líneas y contiene información sobre los tamaños de los 
problemas, la configuración del sistema y las características del algoritmo que 
utilizará el ejecutable. A continuación se explican algunos de los parámetros 
más relevantes de este archivo:

- **Línea 5:** Esta línea especifica el número de tamaños de problema a utilizar. 
Este número debe ser menor o igual a 20. El primer entero es significativo, el 
resto se ignora. Si la línea dice:
    
    ```bash
    2        # of problems sizes (N)
    ```
  esto significa que se utilizarán 2 tamaños de problema que se especificarán en 
  la siguiente línea.

- **Línea 6:** Esta línea especifica los tamaños de problema a utilizar. Suponiendo 
que la línea anterior comenzó con 2, los 2 primeros números enteros positivos son 
significativos, el resto se ignora. Por ejemplo:
    
    ```bash
    3000 6000   Ns
    ```

  Para obtener más información de este parámetro, consulte el siguiente 
  [enlace](https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/#hpl-main-parameters).

- **Línea 7:** Esta línea especifica el número de tamaños de bloque a utilizar. 
Este número debe ser menor o igual a 20. El primer entero es significativo, el 
resto se ignora. Si la línea dice:

    ```bash
    3        # of NBs
    ```

  esto significa que se utilizarán 3 tamaños de bloque que se especificarán en la 
  siguiente línea.

- **Línea 8:** Esta línea especifica los tamaños de bloque a utilizar. Suponiendo 
que la línea anterior comenzó con 3, los 3 primeros números enteros positivos son 
significativos, el resto se ignora. Por ejemplo:

    ```
    80 100 120  NBs
    ```

- **Línea 10:** Esta línea especifica el número de cuadrículas de procesos a utilizar. 
Este número debe ser menor o igual a 20. El primer entero es significativo, el resto 
se ignora. Si la línea dice:
    ```bash
    2        # of process grids (P x Q)
    ```
  Esto significa que se utilizarán 2 tamaños de cuadrícula de procesos que se especificarán 
  en la siguiente línea.

- **Línea 11-12:** Estas dos líneas especifican la cantidad de procesos correspondientes 
a cada fila y a cada columna de cada cuadrícula a utilizar. Suponiendo que la línea anterior 
comenzó con 2, los 2 primeros números enteros positivos de esas dos líneas son significativos, 
el resto se ignora. Por ejemplo:

    ```
    2 4          Ps
    5 8          Qs
    ```

```admonish warning title=""
En este ejemplo, se requiere ejecutar HPL en un nodo con al menos 32 cores:

Ps<sub>1</sub> x Qs<sub>1</sub> = 2 x 5 = 10 cores\
Ps<sub>2</sub> x Qs<sub>2</sub> = 4 x 8 = 32 cores
```

Para escribir el archivo de entrada de HPL debe considerar los recursos de su sistema: 
el número de nodos, el número de CPUs por nodo, y la cantidad de memoria por nodo. 
Puede utilizar el sitio web [How do I tune my HPL.dat file?](https://www.advancedclustering.com/act_kb/tune-hpl-dat-file/) 
para generar su archivo de entrada.

Para obtener más información, consulte la sección 
[HPL Tuning](https://netlib.org/benchmark/hpl/tuning.html) del sitio oficial de HPL.


## Archivo de salida

A continuación se presenta el archivo de entrada:

<span style="color: #990819;">*HPL.dat*</span>

```bash
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out     output file name (if any)
6           device out (6=stdout,7=stderr,file)
2           # of problems sizes (N)
82432 285600 Ns
1           # of NBs
224         # of problems sizes (N)
0           MAP process mapping (0=Row-,1=Column-major)
1           # of process grids (P x Q)
15          Ps
16          Qs
16.0        threshold
1           # of panel fact<
2           PFACTs (0=left, 1=Crout, 2=Right)
1           # of recursive stopping criterium
4           NBMINs (>= 1)
1           # of panels in recursion
2           NDIVs
1           # of recursive panel fact.
1           RFACTs (0=left, 1=Crout, 2=Right)
1           # of broadcast
1           BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1           # of lookahead depth
1           DEPTHs (>=0)
2           SWAP (0=bin-exch,1=long,2=mix)
64          swapping threshold
0           L1 in (0=transposed,1=no-transposed) form
0           U in (0=transposed,1=no-transposed) form
1           Equilibration (0=no,1=yes)
8           memory alignment in double (> 0)
```

y la salida de una ejecución de HPL:

<span style="color: #990819;">*HPL.out*</span>

```bash

(1)

================================================================================
HPLinpack 2.3  --  High-Performance Linpack benchmark  --   December 2, 2018
Written by A. Petitet and R. Clint Whaley,  Innovative Computing Laboratory, UTK
Modified by Piotr Luszczek, Innovative Computing Laboratory, UTK
Modified by Julien Langou, University of Colorado Denver
================================================================================

(2)

An explanation of the input/output parameters follows:
T/V    : Wall time / encoded variant.
N      : The order of the coefficient matrix A.
NB     : The partitioning blocking factor.
P      : The number of process rows.
Q      : The number of process columns.
Time   : Time in seconds to solve the linear system.
Gflops : Rate of execution for solving the linear system.

(3)

The following parameter values will be used:

N      :   82432   329728
NB     :     224
PMAP   : Row-major process mapping
P      :      16
Q      :      20
PFACT  :   Right
NBMIN  :       4
NDIV   :       2
RFACT  :   Crout
BCAST  :  1ringM
DEPTH  :       1
SWAP   : Mix (threshold = 64)
L1     : transposed form
U      : transposed form
EQUIL  : yes
ALIGN  : 8 double precision words

--------------------------------------------------------------------------------

(4)

- The following scaled residual check will be computed:
        ||Ax-b||_oo / ( eps * ( || x ||_oo * || A ||_oo + || b ||_oo ) * N )
- The relative machine precision (eps) is taken to be               1.110223e-16
- Computational tests pass if scaled residuals are less than                16.0

(5)

================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR11C2R4       82432   224    16    20              73.92             5.0515e+03
HPL_pdgesv() start time Mon Feb 14 08:41:17 2022

HPL_pdgesv() end time   Mon Feb 14 08:42:31 2022

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   1.93387398e-03 ...... PASSED
================================================================================
T/V                N    NB     P     Q               Time                 Gflops
--------------------------------------------------------------------------------
WR11C2R4      329728   224    16    20            3799.69             6.2897e+03
HPL_pdgesv() start time Mon Feb 14 08:42:39 2022

HPL_pdgesv() end time   Mon Feb 14 09:45:59 2022

--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   1.40718329e-03 ...... PASSED
================================================================================

(6)

Finished      2 tests with the following results:
                2 tests completed and passed residual checks,
                0 tests completed and failed residual checks,
                0 tests skipped because of illegal input values.
--------------------------------------------------------------------------------

End of Tests.
================================================================================
```

1. Información general del benchmark

2. Explicación de los parámetros de entrada/salida

3. Parámetros utilizados

4. Criterio de aprobación

5. Información de la ejecución de las pruebas:
  - Parámetros
  - Tiempo de ejecución
  - GFLOP/s
  - Éxito/fallo de la prueba

6. Resumen de la ejecución de las pruebas:
  - Número de pruebas ejecutadas
  - Número de pruebas completadas exitosas
  - Número de pruebas completadas fallidas
  - Número de pruebas omitidas debido a valores de entrada ilegales


## Nodos de cómputo

Unresolved directive in hpl.adoc - include::partial\$reframe/nodos_computo.adoc\[\]

## Pruebas

Las pruebas realizadas con este benchmark se dividen en dos grupos:

- **Rendimiento.** Su objetivo es obtener el mayor rendimiento posible. En cada prueba 
se utiliza un tamaño de problema acorde a los recursos disponibles.

- **Eficiencia Paralela.** Su objetivo es determinar la eficiencia paralela. El tamaño 
del problema se mantiene fijo en todas las pruebas.

En las siguientas tablas se da un resumen de las pruebas realizadas en cada tipo de nodo:

<span style="color: #990819;">*Tabla 1. Pruebas en los nodos NC*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Número de CPUs</th>
<th colspan="2">Tamaño del problema</th>
<th rowspan="2">Tamaño del bloque</th>
<th colspan="2">Tamaño de la cuadrícula</th>
</tr>

<tr>
<th rowspan>Rendimiento</th>
<th rowspan>Eficiencia Paralela</th>
<th>P</th>
<th>Q</th>
</tr>

</thead>
<tbody>

<tr>
<td>1</td><td>20</td><td>82432</td><td>82432</td><td>224</td><td>4</td><td>5</td>
</tr>

<tr>
<td>2</td><td>40</td><td>116480</td><td>82432</td><td>224</td><td>5</td><td>8</td>
</tr>

<tr>
<td>4</td><td>80</td><td>164864</td><td>82432</td><td>224</td><td>8</td><td>10</td>
</tr>

<tr>
<td>8</td><td>160</td><td>233184</td><td>82432</td><td>224</td><td>10</td><td>16</td>
</tr>

<tr>
<td>12</td><td>240</td><td>285600</td><td>82432</td><td>224</td><td>15</td><td>16</td>
</tr>

<tr>
<td>16</td><td>320</td><td>329728</td><td>82432</td><td>224</td><td>16</td><td>20</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #990819;">*Tabla 2. Pruebas en los nodos TTv1*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Número de CPUs</th>
<th colspan="2">Tamaño del problema</th>
<th rowspan="2">Tamaño del bloque</th>
<th colspan="2">Tamaño de la cuadrícula</th>
</tr>

<tr>
<th>Rendimiento</th>
<th>Eficiencia Paralela</th>
<th>P</th>
<th>Q</th>
</tr>

</thead>
<tbody>

<tr>
<td>1</td><td>20</td><td>116480</td><td>116480</td><td>224</td><td>4</td><td>5</td>
</tr>

<tr>
<td>2</td><td>40</td><td>164864</td><td>116480</td><td>224</td><td>5</td><td>8</td>
</tr>

<tr>
<td>4</td><td>80</td><td>233184</td><td>116480</td><td>224</td><td>8</td><td>10</td>
</tr>

<tr>
<td>8</td><td>160</td><td>329728</td><td>116480</td><td>224</td><td>10</td><td>16</td>
</tr>

<tr>
<td>12</td><td>240</td><td>403872</td><td>116480</td><td>224</td><td>15</td><td>16</td>
</tr>

<tr>
<td>16</td><td>320</td><td>466368</td><td>116480</td><td>224</td><td>16</td><td>20</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #990819;">*Tabla 3. Pruebas en los nodos TTv2*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Número de CPUs</th>
<th colspan="2">Tamaño del problema</th>
<th rowspan="2">Tamaño del bloque</th>
<th colspan="2">Tamaño de la cuadrícula</th>
</tr>

<tr>
<th>Rendimiento</th>
<th>Eficiencia Paralela</th>
<th>P</th>
<th>Q</th>
</tr>

</thead>
<tbody>

<tr>
<td>1</td><td>32</td><td>164864</td><td>164864</td><td>224</td><td>4</td><td>8</td>
</tr>

<tr>
<td>2</td><td>64</td><td>233184</td><td>164864</td><td>224</td><td>8</td><td>8</td>
</tr>

<tr>
<td>4</td><td>128</td><td>329728</td><td>164864</td><td>224</td><td>8</td><td>16</td>
</tr>

<tr>
<td>8</td><td>256</td><td>466368</td><td>164864</td><td>224</td><td>16</td><td>16</td>
</tr>

<tr>
<td>12</td><td>384</td><td>571200</td><td>164864</td><td>224</td><td>16</td><td>24</td>
</tr>

<tr>
<td>16</td><td>512</td><td>659456</td><td>164864</td><td>224</td><td>16</td><td>32</td>
</tr>

</tbody>
</table>
</div>


## Scripts


### Estructura de directorios

Dentro de la carpeta raíz *hpl* existen tres subdirectorios principales, uno por cada tipo de nodo en el cluster Yoltla:

```bash
hpl
├── nc
|   .
|   .
|   .
├── ttv1
|   .
|   .
|   .
└── ttv2
|   .
|   .
|   .
```

Cada uno de estos directorios alberga seis pruebas de ReFrame, cada una en su directorio correspondiente:

```bash
hpl
├── nc
│   ├── nodos_01
│   │   ├── hpl_nc_20p.py
│   │   ├── logs
│   │   └── src
│   │       └── HPL.dat
│   ├── nodos_02
│   │   ├── hpl_nc_40p.py
│   │   ├── logs
│   │   └── src
│   │       └── HPL.dat
│   ├── nodos_04
│   │   ├── hpl_nc_80p.py
│   │   ├── logs
│   │   └── src
│   │       └── HPL.dat
│   ├── nodos_08
│   │   ├── hpl_nc_160p.py
│   │   ├── logs
│   │   └── src
│   │       └── HPL.dat
│   ├── nodos_12
│   │   ├── hpl_nc_240p.py
│   │   ├── logs
│   │   └── src
│   │       └── HPL.dat
│   └── nodos_16
│       ├── hpl_nc_320p.py
│       ├── logs
│       └── src
│           └── HPL.dat
├── ttv1
│   ├── nodos_01
│   │   ├── hpl_ttv1_20p.py
│   │   ├── logs
│   │   └── src
│   │       └── HPL.dat
.   .
.   .
.   .
│   └── nodos_16
│       ├── hpl_ttv1_320p.py
│       ├── logs
│       └── src
│           └── HPL.dat
└── ttv2
    ├── nodos_01
    │   ├── hpl_ttv2_32p.py
    │   ├── logs
    │   └── src
    │       └── HPL.dat
    .
    .
    .
    └── nodos_16
        ├── hpl_ttv2_512p.py
        ├── logs
        └── src
            └── HPL.dat
```

Estas pruebas van desde 1 hasta 16 nodos, y pueden ser lanzadas de manera individual o por etiquetas.

```admonish note title=" "
La versión de HPL utilizada en estos scripts es la 2.3.
```


### Lanzar pruebas


#### Individualmente

Para lanzar pruebas de forma individual, ubíquese dentro del directorio de la prueba de interés, y ejecute el comando:

```bash
reframe -c <nombre_script> -r
```

Por ejemplo, para lanzar la prueba de 16 nodos, en los nodos NC, ejecute el comando:

```bash
[t.800@yoltla nodos_16]$ reframe -c hpl_nc_320p.py -r
```


#### Etiquetas

Utilizando etiquetas puede lanzar múltiples pruebas con un solo comando. Por ejemplo, para lanzar todas las pruebas de los nodos NC, siga los siguientes pasos:

1.  Ubíquese en el directorio raíz *hpl*:

    ```bash
    [t.800@yoltla hpl]$
    ```

2.  Cree el directorio *logs*:

    ```bash
    [t.800@yoltla hpl]$ mkdir logs
    ```

3.  Ejecute el comando:

    ```bash
    [t.800@yoltla hpl]$ reframe -c . -R -t nc -r
    ```

Para lanzar todas las pruebas:

1.  Ubíquese en el directorio raíz *hpl*:

    ```bash
    [t.800@yoltla hpl]$
    ```

2.  Cree el directorio *logs*:

    ```bash
    [t.800@yoltla hpl]$ mkdir logs
    ```

3.  Ejecute el comando:

    ```bash
    [t.800@yoltla hpl]$ reframe -c . -R -t hpl -r
    ```

```admonish warning title=" "
Si no crea el directorio *logs* obtendrá el siguiente mensaje:

    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: failed to load configuration: [Errno 2] No such file or directory: '/LUSTRE/home/uam/.../t.800/.../hpl/logs/rfm.out'
    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: Log file(s) saved in '/tmp/rfm-v3564kg5.log'
```


## Resultados


### Nodos NC


#### Rendimiento

<span style="color: #990819;">*Tabla 4. Rendimiento de los nodos NC*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">GFLOP/s</th>
</tr>

<tr>
<th>Teórico</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>82432</td><td>400.00</td><td>411.05</td><td>404.29</td><td>414.69</td><td>3.73</td>
</tr>

<tr>
<td>5</td><td>2</td><td>116480</td><td>800.00</td><td>785.80</td><td>711.87</td><td>818.96</td><td>41.41</td>
</tr>

<tr>
<td>5</td><td>4</td><td>164864</td><td>1600.00</td><td>1531.58</td><td>1255.50</td><td>1617.90</td><td>138.36</td>
</tr>

<tr>
<td>5</td><td>8</td><td>233184</td><td>3200.00</td><td>3174.02</td><td>3171.10</td><td>3178.10</td><td>2.72</td>
</tr>

<tr>
<td>5</td><td>12</td><td>285600</td><td>4800.00</td><td>4671.76</td><td>4665.50</td><td>4676.80</td><td>4.38</td>
</tr>

<tr>
<td>5</td><td>16</td><td>329728</td><td>6400.00</td><td>6228.20</td><td>6044.70</td><td>6284.20</td><td>92.06</td>
</tr>

</tbody>
</table>
</div>


\
<span style="color: #1285E3;">Rendimiento de los nodos NC</span>

![Rendimiento de los nodos NC](../../../images/Reframe/benchmarks/hpl/rendimiento/nc.png)

<span style="color: #990819;">*Figura 1. Rendimiento de los nodos NC*</span>

```admonish note title=" "
Los valores teóricos se calcularon tomando como base el rendimiento teórico en 1 nodo. 
Este valor se obtuvo del siguiente [documento](https://www.intel.com/content/dam/support/us/en/documents/processors/APP-for-Intel-Xeon-Processors.pdf).

Para obtener más información, consulte el siguiente [enlace](https://www.intel.com/content/www/us/en/support/articles/000005755/processors.html).
```


#### Eficiencia paralela

<span style="color: #990819;">*Tabla 5. Rendimiento de los nodos NC*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">GFLOP/s</th>
</tr>

<tr>
<th>Teórico</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ<</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>82432</td><td>411.05</td><td>411.05</td><td>404.29</td><td>414.69</td><td>3.73</td>
</tr>

<tr>
<td>5</td><td>2</td><td>82432</td><td>822.11</td><td>776.97</td><td>694.87</td><td>799.44</td><td>41.08</td>
</tr>

<tr>
<td>5</td><td>4</td><td>82432</td><td>1644.22</td><td>1532.72</td><td>1521.20</td><td>1548.60</td><td>11.20</td>
</tr>

<tr>
<td>5</td><td>8</td><td>82432</td><td>3288.43</td><td>2838.42</td><td>2805.60</td><td>2849.70</td><td>16.56</td>
</tr>

<tr>
<td>5</td><td>12</td><td>82432</td><td>4932.65</td><td>3953.76</td><td>3931.70</td><td>3975.50</td><td>15.55</td>
</tr>

<tr>
<td>5</td><td>16</td><td>82432</td><td>6576.86</td><td>5129.76</td><td>5068.80</td><td>5171.00</td><td>38.33</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">Rendimiento de los nodos NC</span>

![Rendimiento de los nodos NC](../../../images/Reframe/benchmarks/hpl/eficiencia/nc/rendimiento.png)

<span style="color: #990819;">*Figura 2. Rendimiento de los nodos NC*</span>

```admonish note title=" "
Los valores teóricos se calcularon tomando como base el rendimiento obtenido en 1 nodo.
```

<span style="color: #990819;">*Tabla 6. SpeedUp de los nodos NC*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">SpeedUp</th>
</tr>

<tr>
<th>Ideal</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>82432</td><td>1.00</td><td>1.00</td><td>1.00</td><td>1.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>2</td><td>82432</td><td>2.00</td><td>1.88</td><td>1.68</td><td>1.98</td><td>0.11</td>
</tr>

<tr>
<td>5</td><td>4</td><td>82432</td><td>4.00</td><td>3.73</td><td>3.68</td><td>3.78</td><td>0.03</td>
</tr>

<tr>
<td>5</td><td>8</td><td>82432</td><td>8.00</td><td>6.91</td><td>6.80</td><td>7.05</td><td>0.08</td>
</tr>

<tr>
<td>5</td><td>12</td><td>82432</td><td>12.00</td><td>9.62</td><td>9.50</td><td>9.78</td><td>0.09</td>
</tr>

<tr>
<td>5</td><td>16</td><td>82432</td><td>16.00</td><td>12.48</td><td>12.29</td><td>12.62</td><td>0.11</td>
</tr>

</body>
</table>
</div>

\
<span style="color: #1285E3;">SpeedUp de los nodos NC</span>

![SpeedUp de los nodos NC](../../../images/Reframe/benchmarks/hpl/eficiencia/nc/speedup.png)

<span style="color: #990819;">*Figura 3. SpeedUp de los nodos NC*</span>

\
<span style="color: #990819;">*Tabla 7. Eficiencia paralela de los nodos NC*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">Eficiencia Paralela</th>
</tr>

<tr>
<th>Ideal</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>82432</td><td>1.00</td><td>1.00</td><td>1.00</td><td>1.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>2</td><td>82432</td><td>1.00</td><td>0.94</td><td>0.84</td><td>0.99</td><td>0.05</td>
</tr>

<tr>
<td>5</td><td>4</td><td>82432</td><td>1.00</td><td>0.93</td><td>0.92</td><td>0.95</td><td>0.01</td>
</tr>

<tr>
<td>5</td><td>8</td><td>82432</td><td>1.00</td><td>0.86</td><td>0.85</td><td>0.88</td><td>0.01</td>
</tr>

<tr>
<td>5</td><td>12</td><td>82432</td><td>1.00</td><td>0.80</td><td>0.79</td><td>0.82</td><td>0.01</td>
</tr>

<tr>
<td>5</td><td>16</td><td>82432</td><td>1.00</td><td>0.78</td><td>0.77</td><td>0.79</td><td>0.01</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">Eficiencia Paralela de los nodos NC</span>

![Eficiencia Paralela de los nodos NC](../../../images/Reframe/benchmarks/hpl/eficiencia/nc/eficiencia_paralela.png)

<span style="color: #990819;">*Figura 4. Eficiencia Paralela de los nodos NC*</span>


### Nodos TTv1
 

#### Rendimiento

<span style="color: #990819;">*Tabla 8. Rendimiento de los nodos TTv1*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">GFLOP/s</th>
</tr>

<tr>
<th>Teórico</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>116480</td><td>832.00</td><td>598.28</td><td>576.12</td><td>617.02</td><td>15.18</td>
</tr>

<tr>
<td>5</td><td>2</td><td>164864</td><td>1664.00</td><td>1140.56</td><td>1077.40</td><td>1162.60</td><td>32.24</td>
</tr>

<tr>
<td>5</td><td>4</td><td>233184</td><td>3328.00</td><td>2157.34</td><td>1698.70</td><td>2355.90</td><td>239.96</td>
</tr>

<tr>
<td>5</td><td>8</td><td>329728</td><td>6656.00</td><td>3891.14</td><td>2419.00</td><td>4632.90</td><td>787.50</td>
</tr>

<tr>
<td>5</td><td>12</td><td>403872</td><td>9984.00</td><td>4627.80</td><td>3241.60</td><td>6507.70</td><td>1433.78</td>
</tr>

<tr>
<td>5</td><td>16</td><td>466368</td><td>13312.00</td><td>5796.84</td><td>3118.60</td><td>8684.90</td><td>2121.74</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">Rendimiento de los nodos TTv1</span>

![Rendimiento de los nodos TTv1](../../../images/Reframe/benchmarks/hpl/rendimiento/ttv1.png)

<span style="color: #990819;">*Figura 5. Rendimiento de los nodos TTv1*</span>

```admonish note title=" "
Los valores teóricos se calcularon tomando como base el rendimiento teórico en 1 nodo. Este valor se obtuvo del siguiente [documento](https://www.intel.com/content/dam/support/us/en/documents/processors/APP-for-Intel-Xeon-Processors.pdf).

Para obtener más información, consulte el siguiente [enlace](https://www.intel.com/content/www/us/en/support/articles/000005755/processors.html).
```


#### Eficiencia paralela

<span style="color: #990819;">*Tabla 9. Rendimiento de los nodos TTv1*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">GFLOP/s</th>
</tr>

<tr>
<th>Teórico</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>116480</td><td>598.28</td><td>598.28</td><td>576.12</td><td>617.02</td><td>15.18</td>
</tr>

<tr>
<td>5</td><td>2</td><td>116480</td><td>1196.56</td><td>1103.86</td><td>1050.6</td><td>1146.4</td><td>38.66</td>
</tr>

<tr>
<td>5</td><td>4</td><td>116480</td><td>2393.11</td><td>2101.16</td><td>1737.2</td><td>2265.9</td><td>200.42</td>
</tr>

<tr>
<td>5</td><td>8</td><td>116480</td><td>4786.22</td><td>3702.76</td><td>2263.8</td><td>4259.7</td><td>739.10</td>
</tr>

<tr>
<td>5</td><td>12</td><td>116480</td><td>7179.34</td><td>4250.50</td><td>3245.7</td><td>6021.9</td><td>1217.63</td>
</tr>

<tr>
<td>5</td><td>16</td><td>116480</td><td>9572.45</td><td>5636.48</td><td>4197.3</td><td>7901.7</td><td>1742.36</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">Rendimiento de los nodos TTv1</span>

![Rendimiento de los nodos TTv1](../../../images/Reframe/benchmarks/hpl/eficiencia/ttv1/rendimiento.png)

<span style="color: #990819;">*Figura 6. Rendimiento de los nodos TTv1*</span>

```admonish note title=" "
Los valores teóricos se calcularon tomando como base el rendimiento obtenido en 1 nodo.
```

<span style="color: #990819;">*Tabla 10. SpeedUp de los nodos TTv1*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">SpeedUp</th>
</tr>

<tr>
<th>Ideal</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>116480</td><td>1.00</td><td>1.00</td><td>1.00</td><td>1.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>2</td><td>116480</td><td>2.00</td><td>1.84</td><td>1.72</td><td>1.95</td><td>0.08</td>
</tr>

<tr>
<td>5</td><td>4</td><td>116480</td><td>4.00</td><td>3.48</td><td>3.02</td><td>3.84</td><td>0.30</td>
</tr>

<tr>
<td>5</td><td>8</td><td>116480</td><td>8.00</td><td>5.85</td><td>3.93</td><td>7.09</td><td>1.15</td>
</tr>

<tr>
<td>5</td><td>12</td><td>116480</td><td>12.00</td><td>6.59</td><td>5.35</td><td>10.27</td><td>2.04</td>
</tr>

<tr>
<td>5</td><td>16</td><td>116480</td><td>16.00</td><td>8.63</td><td>7.05</td><td>12.81</td><td>2.68</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">SpeedUp de los nodos TTv1</span>

![SpeedUp de los nodos TTv1](../../../images/Reframe/benchmarks/hpl/eficiencia/ttv1/speedup.png)

<span style="color: #990819;">*Figura 7. SpeedUp de los nodos TTv1*</span>

\
<span style="color: #990819;">*Tabla 11. Eficiencia paralela de los nodos TTv1*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">Eficiencia Paralela</th>
</tr>

<tr>
<th>Ideal</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>116480</td><td>1.00</td><td>1.00</td><td>1.00</td><td>1.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>2</td><td>116480</td><td>1.00</td><td>0.92</td><td>0.86</td><td>0.98</td><td>0.04</td>
</tr>

<tr>
<td>5</td><td>4</td><td>116480</td><td>1.00</td><td>0.87</td><td>0.76</td><td>0.96</td><td>0.08</td>
</tr>

<tr>
<td>5</td><td>8</td><td>116480</td><td>1.00</td><td>0.73</td><td>0.49</td><td>0.89</td><td>0.14</td>
</tr>

<tr>
<td>5</td><td>12</td><td>116480</td><td>1.00</td><td>0.55</td><td>0.45</td><td>0.86</td><td>0.17</td>
</tr>

<tr>
<td>5</td><td>16</td><td>116480</td><td>1.00</td><td>0.54</td><td>0.44</td><td>0.80</td><td>0.17</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">Eficiencia Paralela de los nodos TTv1</span>

![Eficiencia Paralela de los nodos TTv1](../../../images/Reframe/benchmarks/hpl/eficiencia/ttv1/eficiencia_paralela.png)

<span style="color: #990819;">*Figura 8. Eficiencia Paralela de los nodos TTv1*</span>


### Nodos TTv2


#### Rendimiento

<span style="color: #990819;">Tabla 12. Rendimiento de los nodos TTv2</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">GFLOP/s</th>
</tr>

<tr>
<th>Teórico</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>164864</td><td>1075.20</td><td>729.58</td><td>686.95</td><td>761.56</td><td>29.24</td>
</tr>

<tr>
<td>5</td><td>2</td><td>233184</td><td>2150.40</td><td>1438.04</td><td>1381.10</td><td>1496.80</td><td>42.90</td>
</tr>

<tr>
<td>5</td><td>4</td><td>329728</td><td>4300.80</td><td>1724.86</td><td>1232.80</td><td>2659.00</td><td>539.26</td>
</tr>

<tr>
<td>5</td><td>8</td><td>466368</td><td>8601.60</td><td>3236.20</td><td>2455.10</td><td>4972.80</td><td>886.62</td>
</tr>

<tr>
<td>5</td><td>12</td><td>571200</td><td>12902.40</td><td>5254.36</td><td>2497.90</td><td>8010.10</td><td>1748.29</td>
</tr>

<tr>
<td>5</td><td>16</td><td>659456</td><td>17203.20</td><td>4508.90</td><td>2689.00</td><td>7151.30</td><td>1661.60</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">Rendimiento de los nodos TTv2</span>

![Rendimiento de los nodos TTv2](../../../images/Reframe/benchmarks/hpl/rendimiento/ttv2.png)

<span style="color: #990819;">*Figura 9. Rendimiento de los nodos TTv2*</span>

```admonish note title=" "
Los valores teóricos se calcularon tomando como base el rendimiento teórico en 1 nodo. Este valor se obtuvo del siguiente [documento](https://www.intel.com/content/dam/support/us/en/documents/processors/APP-for-Intel-Xeon-Processors.pdf).

Para obtener más información, consulte el siguiente [enlace](https://www.intel.com/content/www/us/en/support/articles/000005755/processors.html).
```


#### Eficiencia paralela

<span style="color: #990819;">*Tabla 13. Rendimiento de los nodos TTv2*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">GFLOP/s</th>
</tr>

<tr>
<th>Teórico</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>164864</td><td>729.58</td><td>729.58</td><td>686.95</td><td>761.56</td><td>29.24</td>
</tr>

<tr>
<td>5</td><td>2</td><td>164864</td><td>1459.15</td><td>1382.94</td><td>1338.30</td><td>1445.60</td><td>38.44</td>
</tr>

<tr>
<td>5</td><td>4</td><td>164864</td><td>2918.30</td><td>1574.09</td><td>416.97</td><td>2490.90</td><td>795.92</td>
</tr>

<tr>
<td>5</td><td>8</td><td>164864</td><td>5836.61</td><td>3107.22</td><td>1951.00</td><td>4834.50</td><td>1008.10</td>
</tr>

<tr>
<td>5</td><td>12</td><td>164864</td><td>8754.91</td><td>3451.72</td><td>1115.20</td><td>6475.40</td><td>1818.78</td>
</tr>

<tr>
<td>5</td><td>16</td><td>164864</td><td>11673.22</td><td>4288.94</td><td>2398.70</td><td>6023.20</td><td>1153.10</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">Rendimiento de los nodos TTv2</span>

![Rendimiento de los nodos TTv2](../../../images/Reframe/benchmarks/hpl/eficiencia/ttv2/rendimiento.png)

<span style="color: #990819;">*Figura 10. Rendimiento de los nodos TTv2*</span>

```admonish note title=" "
Los valores teóricos se calcularon tomando como base el rendimiento obtenido en 1 nodo.
```

\
<span style="color: #990819;">*Tabla 14. SpeedUp de los nodos TTv2*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">SpeedUp</th>
</tr>

<tr>
<th>Ideal</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>164864</td><td>1.00</td><td>1.00</td><td>1.00</td><td>1.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>2</td><td>164864</td><td>2.00</td><td>1.90</td><td>1.85</td><td>1.95</td><td>0.03</td>
</tr>

<tr>
<td>5</td><td>4</td><td>164864</td><td>4.00</td><td>1.43</td><td>0.61</td><td>3.27</td><td>1.01</td>
</tr>

<tr>
<td>5</td><td>8</td><td>164864</td><td>8.00</td><td>3.87</td><td>2.84</td><td>6.35</td><td>1.22</td>
</tr>

<tr>
<td>5</td><td>12</td><td>164864</td><td>12.00</td><td>3.35</td><td>1.62</td><td>8.50</td><td>2.32</td>
</tr>

<tr>
<td>5</td><td>16</td><td>164864</td><td>16.00</td><td>5.38</td><td>3.49</td><td>7.91</td><td>1.40</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">SpeedUp de los nodos TTv2</span>

![SpeedUp de los nodos TTv2](../../../images/Reframe/benchmarks/hpl/eficiencia/ttv2/speedup.png)

<span style="color: #990819;">*Figura 11. SpeedUp de los nodos TTv2*</span>

\
<span style="color: #990819;">*Tabla 15. Eficiencia paralela de los nodos TTv2*</span>

<div class="tabla-scroll">
<table style="text-align: center;">
<thead>

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Número de nodos</th>
<th rowspan="2">Tamaño del problema</th>
<th colspan="5">Eficiencia Paralela</th>
</tr>

<tr>
<th>Ideal</th>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

</thead>
<tbody>

<tr>
<td>5</td><td>1</td><td>164864</td><td>1.00</td><td>1.00</td><td>1.00</td><td>1.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>2</td><td>164864</td><td>1.00</td><td>0.95</td><td>0.93</td><td>0.98</td><td>0.02</td>
</tr>

<tr>
<td>5</td><td>4</td><td>164864</td><td>1.00</td><td>0.36</td><td>0.15</td><td>0.82</td><td>0.25</td>
</tr>

<tr>
<td>5</td><td>8</td><td>164864</td><td>1.00</td><td>0.48</td><td>0.36</td><td>0.79</td><td>0.15</td>
</tr>

<tr>
<td>5</td><td>12</td><td>164864</td><td>1.00</td><td>0.28</td><td>0.14</td><td>0.71</td><td>0.19</td>
</tr>

<tr>
<td>5</td><td>16</td><td>164864</td><td>1.00</td><td>0.34</td><td>0.22</td><td>0.49</td><td>0.09</td>
</tr>

</tbody>
</table>
</div>

\
<span style="color: #1285E3;">Eficiencia Paralela de los nodos TTv2</span>

![Eficiencia Paralela de los nodos TTv2](../../../images/Reframe/benchmarks/hpl/eficiencia/ttv2/eficiencia_paralela.png)

<span style="color: #990819;">*Figura 12. Eficiencia Paralela de los nodos TTv2*</span>


### Yoltla


#### Rendimiento

<span style="color: #1285E3;">Rendimiento promedio de los nodos del cluster Yoltla</span>

![Rendimiento promedio de los nodos del cluster Yoltla](../../../images/Reframe/benchmarks/hpl/rendimiento/yoltla.png)

<span style="color: #990819;">*Figura 13. Rendimiento promedio de los nodos del cluster Yoltla*</span>


#### Eficiencia paralela

<span style="color: #1285E3;">Rendimiento promedio de los nodos del cluster Yoltla</span>

![Rendimiento promedio de los nodos del cluster Yoltla](../../../images/Reframe/benchmarks/hpl/eficiencia/yoltla/rendimiento.png)

<span style="color: #990819;">*Figura 14. Rendimiento promedio de los nodos del cluster Yoltla*</span>

\
<span style="color: #1285E3;">SpeedUp promedio de los nodos del cluster Yoltla</span>

![SpeedUp promedio de los nodos del cluster Yoltla](../../../images/Reframe/benchmarks/hpl/eficiencia/yoltla/speedup.png)

<span style="color: #990819;">*Figura 15. SpeedUp promedio de los nodos del cluster Yoltla*</span>

\
<span style="color: #1285E3;">Eficiencia Paralela promedio de los nodos del cluster Yoltla</span>

![Eficiencia Paralela promedio de los nodos del cluster Yoltla](../../../images/Reframe/benchmarks/hpl/eficiencia/yoltla/eficiencia_paralela.png)

<span style="color: #990819;">*Figura 16. Eficiencia Paralela promedio de los nodos del cluster Yoltla*</span>


```admonish note title=" "
Todos los resultados mostrados en esta sección fueron obtenidos en el mes de Febrero del 2022.
```

## Sitios de interés

- [HPL - A Portable Implementation of the High-Performance Linpack Benchmark for Distributed-Memory Computers](https://netlib.org/benchmark/hpl/)

- [High-Performance Linpack (HPL) benchmarking on UL HPC platform](https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/)

- [How do I tune my HPL.dat file?](https://www.advancedclustering.com/act_kb/tune-hpl-dat-file/)

- [AMD \| HPL Benchmark](https://developer.amd.com/spack/hpl-benchmark/)
