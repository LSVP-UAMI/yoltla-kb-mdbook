# Descripción

[`Quantum Espresso`](https://www.quantum-espresso.org/) es un conjunto de códigos Open-Source para
cálculos de estructuras electrónicas y modelado de materiales a nanoescala. Se basa en la teoría
funcional de la densidad, ondas planas y pseudopotenciales.

- Esta trabajo se realizo con quantum-espresso/6.4.1

- Benchmarks: AUSURF112

# PWscf

PWscf es el paquete de programas que permite a Quantum ESPRESSO utilizar ondas planas en las
simulaciones. PWscf existió como un proyecto independiente. El cual permitía realizar cálculos de
estructura electrónica implementando la teoría del funcional de la densidad, utilizando un conjunto base
de ondas planas y pseudopotenciales. PWscf también implemento la teoría del funcional de la densidad
perturbado. PWscf son las siglas en inglés de Plane-Wave Self-Consistent Field y se publicó bajo la
Licencia Pública General GNU.

## Input data

Los datos de entrada de un archivo PWscf se organizan como varias listas de nombres, seguidas de otros
campos (\"tarjetas\") introducidos por palabras clave. Las listas de nombres son:

    &CONTROL:  variables generales que controlan la ejecución
    &SYSTEM: información estructural sobre el sistema bajo investigación
    &ELECTRONS: variables electrónicas
    &IONS (optional): variables iónicas: relajación, dinámica
    &CELL (optional): optimización o dinámica de celdas variables

Para este trabajo nos interesa la sección &ELECTRONS ya que en esta apartado se pueden modificar métodos
de calculo que afectan el performance de `Quantum Espresso`. Los métodos que utilizamos son:

### [Método de diagonalización](https://www.quantum-espresso.org/Doc/INPUT_PW.html#idm805)

`Quantum Espresso` por default utiliza el método de
[Davidson](https://joshuagoings.com/2013/08/23/davidsons-method/) (`david`) ya que es el más rápido. Para
este trabajo optamos por el uso del método
[Conjugate-gradient-like](https://en.wikipedia.org/wiki/Conjugate_gradient_method) (`cg`)
ya que aunque es MUCHO más lento que `david` usa menos memoria y es (un poco) más robusto.

### [K_POINTS](https://www.quantum-espresso.org/Doc/INPUT_PW.html#idm1487)

El método que utilizamos para el calculo k-points es el método Gamma de PWscf
ya que los requisitos de memoria y CPU se reducen aproximadamente a la mitad y permite el estudio de
`Quantum Espresso` en particiones con recursos limitados.

# Quantum Espresso Performance

En el contexto de este trabajo, para revisar el performance de Quantum Espresso, solo nos interesa
los siguiente elementos:

## Total energy

Quantum Espresso muestra en cada paso de simulación la energía de la simulación, donde muestra:

- \"total energy \" en cada auto-consistente ciclo

- "!total energy" convergencia al umbral requerido

:::: formalpara
::: title
Ejemplo de salida de Quantum Espresso donde la energía converge
:::

    .
    .
    .

         total energy              =  -11427.09017110 Ry
         Harris-Foulkes estimate   =  -11427.09017284 Ry
         estimated scf accuracy    <       0.00000554 Ry

         iteration # 18     ecut=    25.00 Ry     beta= 0.70
         CG style diagonalization
         ethr =  4.50E-10,  avg # of iterations =  3.1

         negative rho (up, down):  3.087E+00 0.000E+00

         total cpu time spent up to now is     2620.2 secs

         total energy              =  -11427.09017032 Ry
         Harris-Foulkes estimate   =  -11427.09017363 Ry
         estimated scf accuracy    <       0.00001782 Ry

         iteration # 19     ecut=    25.00 Ry     beta= 0.70
         CG style diagonalization
         ethr =  4.50E-10,  avg # of iterations =  3.0

         negative rho (up, down):  3.087E+00 0.000E+00
    .
    .
    .

    !    total energy              =  -11427.09017181 Ry
         Harris-Foulkes estimate   =  -11427.09017241 Ry
         estimated scf accuracy    <       0.00000061 Ry

         The total energy is the sum of the following terms:

         one-electron contribution = -129710.07694919 Ry
         hartree contribution      =   65681.04191613 Ry
         xc contribution           =   -5524.81964526 Ry
         ewald contribution        =   58126.48229565 Ry
         smearing contrib. (-TS)   =       0.28221086 Ry

         convergence has been achieved in  20 iterations
::::

`Quantum Espresso` buscara llegar a un punto de convergencia en una determinada cantidad de iteraciones
controlada por la variable `electron_maxstep = n` en la sección `&ELECTRONS`.

Si la simulación llega a un punto de convergencia, se informara de la siguiente forma:

    .
    .
    !    total energy              =  -11427.09017181 Ry
    .
    .
         convergence has been achieved in  20 iterations
    .
    .

Donde el signo `!` indica que se llega al umbral requerido, posteriormente se informa el número de
iteraciones que se requirió.

Si la simulación no llega a un punto de convergencia y alcanza el numero máximo de iteraciones,
se detendrá la prueba y se informara de la siguiente forma:

    .
    .
         total energy              = -354349.42104690 Ry
    .
    .
         convergence NOT achieved after   30 iterations: stopping
    .
    .

:::: note
::: title
:::

Algunas simulaciones requieren un número de iteraciones muy alto y un alto tiempo de computo para cada
iteración, en dado caso solo se estudia la simulación para un número pequeño de iteraciones.
::::

## Timing info

El informe de tiempo impreso al final de una ejecución de `pw.x` contiene mucha información útil que puede
utilizarse para comprender los cuellos de botella y mejorar el rendimiento.

Quantum Espresso muestra el tiempo de cpu y tiempo de pared de los siguientes elementos:

- init_run

- electrons

- forces

Posteriormente se muestra un informe de tiempo de las sub-rutinas invocadas (`Called by :`), esto es
útil para identificar cuellos de botella.

:::: formalpara
::: title
Ejemplo de salida de Quantum Espresso
:::

    .
    .
    .
         init_run     :      2.73s CPU      3.18s WALL (       1 calls)
         electrons    :   1443.66s CPU   1450.22s WALL (       1 calls)
         forces       :      1.31s CPU      1.36s WALL (       1 calls)

         Called by init_run:
         wfcinit      :      2.34s CPU      2.58s WALL (       1 calls)
         potinit      :      0.08s CPU      0.10s WALL (       1 calls)
         hinit0       :      0.18s CPU      0.32s WALL (       1 calls)

         Called by electrons:
         c_bands      :   1427.47s CPU   1432.00s WALL (      21 calls)
         sum_band     :     14.39s CPU     16.21s WALL (      21 calls)
         v_of_rho     :      0.69s CPU      0.71s WALL (      21 calls)
         newd         :      1.00s CPU      1.18s WALL (      21 calls)
         mix_rho      :      0.14s CPU      0.15s WALL (      21 calls)
    .
    .
    .
         PWSCF        :  24m 8.44s CPU  24m16.52s WALL
::::

Para un trabajo típico, el tiempo total de pared se gasta principalmente en la rutina \"electrons\",
calculando la solución auto-consistente. Para este trabajo usaremos el tiempo de pared reportado por
\"electrons\" para calcular el performance y la eficiencia paralela.

# Eficiencia paralela

La única forma confiable de ver si un trabajo escala de manera eficiente es compararlo. Comparar un
trabajo significa ejecutar un trabajo de prueba breve y representativo varias veces en diferentes
números de CPU para encontrar un punto óptimo.

A partir de estos datos, se puede calcular la **eficiencia paralela**. Esto se define cómo:

E = (1/P) \* (T~1~/T~P~)

- P = Numero de procesadores

- T~1~ = tiempo óptimo para el algoritmo en un procesador

- T~P~ = tiempo para algoritmo paralelo en P procesadores

Dado que la evaluación comparativa en un solo núcleo a menudo puede llevar mucho tiempo y
la escala dentro de un nodo es generalmente muy buena, para los propósitos del Yoltla es suficiente
hacer este cálculo por nodo, en lugar de por CPU. Para este trabajo, usaremos 1 proceso por core
disponible.

Como regla general, los trabajos que se ejecutan con una gran cantidad de núcleos deben tener
una eficiencia paralela superior o igual a 0,7.

# AUSURF112 Benchmark

Atomic species ：Au complex (Au~112~)、 Number of atoms ： 112 atoms / cell, G-vectors : 381654, FFT dimensions : ( 125, 64, 200)

Para este Bencharmk se definió la variable `electron_maxstep = 30`, siendo la máxima iteración aceptada
para que converja.

La simulación debe llegar a un valor `! total energy` cercano a: `-11427.09017185 Ry`

![](Reframe/Apps/QuantumEspresso/Figure_Ausurf.png){alt="AUSURF112 Performance"}

![](Reframe/Apps/QuantumEspresso/Figure_Performance_Ausurf.png){alt="AUSURF112 Eficiencia Paralela"}

+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| **\#    | **CPU's Nodos nc\          | **CPU's Nodos              | **CPU's Nodos              |
| Nodos** | 20 Cores x 2.50GHz Intel   | ttv1\[1-58\]\              | ttv2\[59-104\]\            |
|         | Xeón E5-2670v2\            | 20 Cores x 2.60GHz Intel   | 32 Cores x 2.10GHz Intel   |
|         | 64GB RAM\                  | Xeón E5-2660v3\            | Xeon E5-2683v4\            |
|         | Infiniband FDR10/FDR**     | 128GB RAM\                 | 256GB RAM\                 |
|         |                            | Infiniband FDR10/FDR**     | Infiniband FDR10/FDR**     |
|         +-------------+--------------+-------------+--------------+-------------+--------------+
|         | **Electrons | **Eficiencia | **Electrons | **Eficiencia | **Electrons | **Eficiencia |
|         | Wall Time   | Paralela %** | Wall Time   | Paralela %** | Wall Time   | Paralela %** |
|         | (s)**       |              | (s)**       |              | (s)**       |              |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 1       | 4129.300    | 100.0 %      | 2817.760    | 100.0 %      | 4535.365    | 100.0 %      |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 2       | 1944.305    | 106.2 %      | 1490.185    | 94.5 %       | 2447.600    | 92.6 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 4       | 1217.410    | 84.8 %       | 870.773     | 80.9 %       | 1876.977    | 60.4 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 5       |             |              | 676.075     | 83.4 %       |             |              |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 8       | 763.187     | 67.6 %       | 521.835     | 67.5 %       | 712.180     | 79.6 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 16      | 460.930     | 56.0 %       | 329.950     | 53.4 %       | 446.970     | 63.4 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+

: Performance AUSURF112 Benchmark

Para esta aplicación notamos que el rendimiento de las simulaciones depende mucho de la cantidad de átomos
y modelo simulado, obteniendo un mejor o peor rendimiento dependiendo de como se divide la cantidad de
procesos MPI para la resolución del problema.

# GRIR443 Benchmark

Atomic species ： Carbon-Iridium complex (C~200~Ir~243~), Number of atoms ： 443 atoms / cell、 G-vectors : 1116532 G-vectors, FFT dimensions: ( 180, 180, 192)

Para este Bencharmk se definió la variable `electron_maxstep = 5`, siendo la máxima iteración que definimos
para su estudio, la simulación no converge para esta cantidad de iteraciones.

La simulación debe llegar a un valor `total energy` cercano a: `-179010.87462864 Ry`

![](Reframe/Apps/QuantumEspresso/Figure_Grir443.png){alt="GRIR443 Performance"}

![](Reframe/Apps/QuantumEspresso/Figure_Performance_Grir443.png){alt="GRIR443 Eficiencia Paralela"}

+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| **\#    | **CPU's Nodos nc\          | **CPU's Nodos              | **CPU's Nodos              |
| Nodos** | 20 Cores x 2.50GHz Intel   | ttv1\[1-58\]\              | ttv2\[59-104\]\            |
|         | Xeón E5-2670v2\            | 20 Cores x 2.60GHz Intel   | 32 Cores x 2.10GHz Intel   |
|         | 64GB RAM\                  | Xeón E5-2660v3\            | Xeon E5-2683v4\            |
|         | Infiniband FDR10/FDR**     | 128GB RAM\                 | 256GB RAM\                 |
|         |                            | Infiniband FDR10/FDR**     | Infiniband FDR10/FDR**     |
|         +-------------+--------------+-------------+--------------+-------------+--------------+
|         | **Electrons | **Eficiencia | **Electrons | **Eficiencia | **Electrons | **Eficiencia |
|         | Wall Time   | Paralela %** | Wall Time   | Paralela %** | Wall Time   | Paralela %** |
|         | (s)**       |              | (s)**       |              | (s)**       |              |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 1       | 36027.840   | 100.0 %      | 27787.965   | 100.0 %      | 42080.990   | 100.0 %      |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 4       | 12142.370   | 74.2 %       | 8676.930    | 80.1 %       | 11211.230   | 93.8 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 5       |             |              | 5679.140    | 97.9 %       |             |              |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 8       | 4730.130    | 95.2 %       | 3780.870    | 91.9 %       | 6725.420    | 78.2 %       |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+
| 16      | 2496.460    | 90.2 %       | 1955.085    | 88.8 %       |             |              |
+---------+-------------+--------------+-------------+--------------+-------------+--------------+

: Performance GRIR443 Benchmark

Para esta simulación notamos que el rendimiento depende del modelo simulado, obteniendo un mejor o peor
rendimiento dependiendo de como se divide la cantidad de procesos MPI para la resolución del problema.
En los resultados reportados, omitimos la cantidad de procesos MPI para cada tipo de nodo
que no brindaban un buen rendimiento para una mejor interpretación de los datos.

# Referencias

[Quantum Espresso](https://www.quantum-espresso.org/)

[Quantum_ESPRESSO](https://es.wikipedia.org/wiki/Quantum_ESPRESSO)

[Quantum Espresso Benchmarks](https://www.quantum-espresso.org/benchmarks/)

[pw.x input](https://www.quantum-espresso.org/Doc/INPUT_PW.html)
