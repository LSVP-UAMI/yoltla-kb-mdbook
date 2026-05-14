# Descripción

La latencia de datos o ancho de banda es uno de los elementos
clave responsables del rendimiento y la escalabilidad de las aplicaciones.
Cuanto menor sea la latencia, mejor será el rendimiento que podemos obtener.

Uno de los principales factores que influyen en el rendimiento de las aplicaciones HPC
es la latencia de las operaciones de transferencia de datos. InfiniBand aborda el
desafío de la latencia con un enfoque doble: por un lado, proporciona una latencia de red extremadamente
baja y, por otro lado, presenta herramientas inteligentes para mejorar la latencia de
las operaciones de datos complejos.

Estas ventajas distinguen a InfiniBand como la solución de
interconexión líder para las plataformas de supercomputación actuales y futuras.

Para este trabajo se probo:

- La operación MPI_Altoall

- Versión de MPI: intel-impi-2017u4

# OSU MPI Micro-Benchmark: All-to-all.

El `osu_alltoall` benchmark mide la latencia mínima, máxima y promedio de la operación
colectiva de bloqueo `MPI_Alltoall` en N procesos, para varias longitudes de mensajes, en una gran
cantidad de iteraciones. En la versión predeterminada, este benchmark informa la latencia promedio
para cada mensaje de hasta 1024 MB. Ejecutamos este benchmark desde un mínimo de 1 nodo hasta 16
nodos, aumentando el número de nodos en potencias de dos.

El benchmark ofrece las siguientes opciones:

- `-f`. Se puede usar para informar estadísticas adicionales del benchmark, como latencias mínimas y
  máximas y el número de iteraciones.

- `-m`. La opción se puede utilizar para establecer la longitud mínima y máxima del mensaje que se
  utilizará en un benchmark en KB.

- `-x`. Se puede usar para configurar el número de iteraciones de calentamiento para cada
  longitud de mensaje.

- `-i`. Se puede utilizar para establecer el número de iteraciones que se ejecutarán para cada longitud
  de mensaje.

- `-M`. Se puede utilizar para establecer el consumo máximo de memoria por proceso.

La latencia (us -- micro-segundos) que se indica a continuación es el promedio de la ejecución del
benchmark Osu en diferentes nodos para un mensaje de 512 MB con 5,000
iteraciones que se ejecutan en nodos completos por partición, 1 proceso por core.

![](Reframe/microBenchmarks/osu/latency/Figure_osu.png){alt="Figure osu"}

+-----------------+-----------------+-----------------+-----------------+
| **\# Nodos**    | **CPU's Nodos   | **CPU's Nodos   | **CPU's Nodos   |
|                 | nc\             | ttv1\[1-58\]\   | ttv2\[59-104\]\ |
|                 | 20 Cores x      | 20 Cores x      | 32 Cores x      |
|                 | 2.50GHz Intel   | 2.60GHz Intel   | 2.10GHz Intel   |
|                 | Xeón E5-2670v2\ | Xeón E5-2660v3\ | Xeon E5-2683v4\ |
|                 | 64GB RAM\       | 128GB RAM\      | 256GB RAM\      |
|                 | Infiniband      | Infiniband      | Infiniband      |
|                 | FDR10/FDR**     | FDR10/FDR**     | FDR10/FDR**     |
|                 +-----------------+-----------------+-----------------+
|                 | **Avg           | **Avg           | **Avg           |
|                 | Latency(us)**   | Latency(us)**   | Latency(us)**   |
+-----------------+-----------------+-----------------+-----------------+
| 1               | 7765.70         | 5145.375        | 18924.79        |
+-----------------+-----------------+-----------------+-----------------+
| 2               | 47352.84        | 46934.865       | 138239.36       |
+-----------------+-----------------+-----------------+-----------------+
| 4               | 157410.27       | 155996.02       | 387857.28       |
+-----------------+-----------------+-----------------+-----------------+
| 5               |                 | 272740.99       |                 |
+-----------------+-----------------+-----------------+-----------------+
| 8               | 379142.63       | 408208.79       | 1284194.83      |
+-----------------+-----------------+-----------------+-----------------+
| 16              | 1135023.25      | 1055702.73      | 3215126.28      |
+-----------------+-----------------+-----------------+-----------------+

Observamos una latencia consistente en los diferentes tipo de nodos presente en el cluster Yoltla.

## Performance OSU MPI Micro-Benchmark: All-to-all en nodos NC.

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 1 nodos NC
:::

    Nodos usados: nc20

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                     26.29               23.46               28.34        5000
    2048                     34.65               30.22               37.81        5000
    4096                     56.13               49.09               61.05        5000
    8192                     97.84               86.43              105.72        5000
    16384                   179.84              161.17              192.23        5000
    32768                   358.97              319.40              381.19        5000
    65536                   564.19              559.91              569.32        5000
    131072                 2185.79             2165.16             2207.01        5000
    262144                 3993.69             3968.22             4020.70        5000
    524288                 7782.54             7745.99             7817.15        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 2 nodos NC
:::

    Nodos usados: nc[82,127]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                    362.46              354.55              371.12        5000
    2048                    500.86              487.72              515.25        5000
    4096                    655.14              637.05              672.22        5000
    8192                    976.45              950.09              999.54        5000
    16384                  1594.11             1555.70             1624.65        5000
    32768                  4273.53             4079.77             4397.28        5000
    65536                  7919.12             7672.45             8038.30        5000
    131072                13749.62            13671.99            13827.41        5000
    262144                24405.09            24230.80            24574.33        5000
    524288                47364.66            47059.82            47672.54        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 4 nodos NC
:::

    Nodos usados: nc[20,79,119-120]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                    476.85              410.33              516.31        5000
    2048                   1102.09             1028.31             1177.30        5000
    4096                   2712.97             2669.93             2738.44        5000
    8192                   3612.90             3553.12             3655.93        5000
    16384                  5842.51             5767.78             5932.87        5000
    32768                 11169.04            10995.98            11328.12        5000
    65536                 21728.15            21672.35            21801.08        5000
    131072                41412.41            41283.17            41491.20        5000
    262144                78043.57            77830.34            78256.45        5000
    524288               155042.18           154653.57           155466.99        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 8 nodos NC
:::

    Nodos usados: nc[47-48,63-64,103,113,122,148]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                   1746.92             1409.69             1957.26        5000
    2048                   3740.85             3212.10             4199.33        5000
    4096                   6588.41             6523.32             6642.87        5000
    8192                   8835.22             8512.81             9097.04        5000
    16384                 15822.28            15724.47            15921.00        5000
    32768                 31674.12            31444.79            31900.96        5000
    65536                 69865.05            69773.19            69938.16        5000
    131072               137189.49           136948.45           137365.44        5000
    262144               254510.92           252322.68           256565.37        5000
    524288               479501.29           460676.15           493836.46        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 16 nodos NC
:::

    Nodos usados: nc[82,90-91,94,102,104,116,124-125,127,134,144-146,149-150]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                   4747.35             4202.93             5110.66        5000
    2048                  11315.42            11245.16            11407.20        5000
    4096                  13058.54            12975.21            13141.17        5000
    8192                  19388.60            19296.36            19518.30        5000
    16384                 33290.76            32526.34            33808.37        5000
    32768                 63480.28            62110.02            64212.39        5000
    65536                130474.96           126965.55           133086.84        5000
    131072               255817.57           250074.76           260439.26        5000
    262144               461933.75           450774.84           474823.23        5000
    524288               923377.30           902362.76           953703.00        5000
::::

## Performance OSU MPI Micro-Benchmark: All-to-all en nodos TTV1.

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 1 nodos
:::

    Nodos usados: tt15

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                     20.68               19.88               21.49        2500
    2048                     25.46               24.04               27.33        2500
    4096                     38.20               35.38               41.25        2500
    8192                     64.40               61.18               67.44        2500
    16384                   148.39              143.74              152.53        2500
    32768                   305.05              296.33              313.84        2500
    65536                   332.73              319.89              343.59        2500
    131072                 1192.27             1183.53             1203.45        2500
    262144                 2374.60             2343.79             2405.87        2500
    524288                 4736.43             4683.40             4764.06        2500
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 2 nodos
:::

    Nodos usados: tt[13-14]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                    130.87               91.98              151.60        2500
    2048                    272.69              200.56              312.21        2500
    4096                    645.04              581.85              693.55        2500
    8192                    956.53              943.50              970.09        2500
    16384                  1545.88             1525.88             1565.64        2500
    32768                  3094.90             3072.49             3118.19        2500
    65536                  6391.97             6373.72             6407.74        2500
    131072                12602.77            12567.53            12628.00        2500
    262144                23620.45            23506.56            23767.59        2500
    524288                47058.50            46831.75            47320.13        2500
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 4 nodos
:::

    Nodos usados: tt[45,51-53]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                    633.97              540.18              749.06        5000
    2048                   1712.48             1399.37             2303.08        5000
    4096                   2877.68             2730.35             3024.90        5000
    8192                   4220.07             3995.20             4448.54        5000
    16384                  7001.21             6704.04             7366.81        5000
    32768                 14729.09            14253.68            15221.03        5000
    65536                 26044.48            25547.83            26898.81        5000
    131072                48789.37            47810.40            50714.06        5000
    262144                83188.23            81773.01            86548.40        5000
    524288               162836.15           160077.38           169730.54        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 5 nodos
:::

    Nodos usados: tt[45,51-53,56]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                   1133.52              927.77             1463.97        5000
    2048                   3084.68             2333.06             4441.90        5000
    4096                   4641.18             4043.52             4933.58        5000
    8192                   6631.27             5693.71             7033.73        5000
    16384                 10503.04             8890.87            11182.25        5000
    32768                 20884.48            20119.28            21843.25        5000
    65536                 35876.77            31448.91            37555.32        5000
    131072                71854.79            63074.10            75986.21        5000
    262144               127378.42           117568.70           140600.85        5000
    524288               255203.38           235462.77           281833.40        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 8 nodos
:::

    Nodos usados: tt[5-8,25-28]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                   1558.66             1461.59             1639.47        5000
    2048                   3484.55             3112.31             3709.58        5000
    4096                   6148.86             6114.58             6178.68        5000
    8192                   9395.37             9326.98             9442.08        5000
    16384                 12652.00            12617.11            12676.39        5000
    32768                 25346.14            25266.20            25413.26        5000
    65536                 43391.27            43319.04            43450.57        5000
    131072                85481.69            85350.67            85607.38        5000
    262144               166844.82           166682.42           167012.90        5000
    524288               335818.97           335333.66           336253.66        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 16 nodos
:::

    Nodos usados: tt[9-11,16,27-28,30-31,33-34,36-39,41,51]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                   5104.50             4584.35             5525.90        5000
    2048                  10368.31             8858.16            11143.89        5000
    4096                  12667.99            12567.19            12787.16        5000
    8192                  19613.77            19193.74            20039.72        5000
    16384                 35116.81            33844.35            36307.51        5000
    32768                 66878.16            63821.00            69705.83        5000
    65536                132352.76           125254.34           138684.29        5000
    131072               257477.14           246594.54           268258.71        5000
    262144               508940.78           480543.74           537383.67        5000
    524288              1086029.60          1016553.95          1148786.78        5000
::::

## Performance OSU MPI Micro-Benchmark: All-to-all en nodos TTV2.

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 1 nodos
:::

    Nodos usados: tt79

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                     59.40               55.88               62.02        2500
    2048                     71.03               66.91               74.78        2500
    4096                    107.37              101.21              113.86        2500
    8192                    176.79              173.11              181.71        2500
    16384                   329.17              316.10              345.14        2500
    32768                  1495.33             1488.51             1500.83        2500
    65536                  2193.72             2145.04             2247.23        2500
    131072                 4804.25             4744.28             4888.10        2500
    262144                 9505.45             9297.05             9599.45        2500
    524288                18842.91            18464.61            19141.38        2500
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 2 nodos
:::

    Nodos usados: tt[94-95]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                   1206.23              948.10             1314.85        5000
    2048                   1652.16             1363.45             1766.34        5000
    4096                   2047.29             1608.95             2235.83        5000
    8192                   2923.37             2112.71             3347.64        5000
    16384                  4583.37             3382.13             5517.71        5000
    32768                  9248.94             7500.60            10269.78        5000
    65536                 19908.96            18702.52            20369.39        5000
    131072                39471.92            39203.36            39718.30        5000
    262144                66323.77            65353.20            67446.38        5000
    524288               129793.41           129009.48           130332.28        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 4 nodos
:::

    Nodos usados: tt[91,93-95]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                   4237.58             3828.33             4474.73        5000
    2048                   5354.75             4894.14             5581.80        5000
    4096                   6776.79             6271.42             7062.35        5000
    8192                   9933.31             9896.38             9981.56        5000
    16384                 15301.58            15102.94            15430.59        5000
    32768                 28368.50            28328.40            28434.78        5000
    65536                 71314.31            70618.22            71804.81        5000
    131072                97172.00            97149.33            97192.67        5000
    262144               188284.06           188243.39           188326.93        5000
    524288               375476.16           375416.18           375573.02        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 8 nodos
:::

    Nodos usados: tt[83-90]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                  11917.72            11435.81            12278.61        5000
    2048                  13536.99            12948.32            13950.34        5000
    4096                  17556.16            16774.30            18100.49        5000
    8192                  26423.91            24731.37            28184.78        5000
    16384                 41177.23            39528.12            42408.99        5000
    32768                 73353.34            69930.43            75596.65        5000
    65536                169240.16           167853.45           169836.99        5000
    131072               335889.91           333840.93           336943.05        5000
    262144               593603.68           591963.47           594677.78        5000
    524288              1137449.09          1133976.34          1139810.17        5000
::::

:::: formalpara
::: title
Salida OSU MPI: All-to-all en 16 nodos
:::

    Nodos usados: tt[61-62,64-67,69-76,91,93]

    # OSU MPI All-to-All Personalized Exchange Latency Test
    # Size         Avg Latency(us)     Min Latency(us)     Max Latency(us)  Iterations
    1024                  25937.48            25392.11            26425.01        5000
    2048                  31260.35            30591.90            31875.63        5000
    4096                  39254.73            38336.62            39959.09        5000
    8192                  59557.50            58132.53            61100.59        5000
    16384                106811.97           105059.42           108375.99        5000
    32768                205126.30           201991.39           207760.06        5000
    65536                461338.37           456315.95           464018.20        5000
    131072               862566.72           855378.09           866137.83        5000
    262144              1562595.70          1553116.55          1567931.80        5000
    524288              3419295.70          3401225.80          3429099.33        5000
::::

# Referencias

[OSU micro-benchmarks](http://mvapich.cse.ohio-state.edu/benchmarks/)

[Tutorial: Building and Runnning OSU Micro-Benchmarks](https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/OSU_MicroBenchmarks/)

[ReFrame Test Library: OSU microbenchmarks](https://reframe-hpc.readthedocs.io/en/stable/hpctestlib.html)
