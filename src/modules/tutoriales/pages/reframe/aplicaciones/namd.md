# Namd


## Descripción

NAMD, es un código de dinámica molecular paralelo diseñado para la simulación de alto rendimiento
de grandes sistemas biomoleculares. Basado en objetos paralelos *Charm++* , NAMD escala en cientos de
núcleos para simulaciones típicas y más allá de 500 000 núcleos para las simulaciones más grandes.

- NAMD utiliza el popular programa de gráficos moleculares VMD para la configuración de
  simulación y el análisis de trayectoria, pero también es compatible con archivos AMBER,
  CHARMM y X-PLOR. NAMD es distribuido de forma gratuita con el código fuente.

- Esta trabajo se realizo con NAMD 2.13.

- Benchmarks: F1-ATPase y STMV


## NAMD Performance

El rendimiento de simulación obtenido de NAMD depende de muchos factores. El protocolo de
simulación en particular que se está ejecutando es uno de los factores individuales más grandes
asociados con el rendimiento de NAMD, ya que los diferentes métodos de simulación invocan un
código diferente que puede tener costos de rendimiento sustancialmente diferentes, potencialmente con
un grado diferente de escalabilidad paralela, actividad de paso de mensajes, aceleración de hardware a
través del uso de GPU o vectorización de CPU, y otros atributos que también contribuyen al
rendimiento general de NAMD.


### Medición de desempeño

Cuando NAMD comienza a ejecutarse, realiza operaciones de E/S significativas, ajuste de FFT,
configuración de contexto de GPU y otros trabajos que no están relacionados con la actividad de
simulación normal, por lo que es importante medir el rendimiento solo cuando NAMD haya
completado el inicio y todas las unidades de procesamiento están corriendo al 100%. La mejor manera
de medir el rendimiento de NAMD es ejecutando simulaciones de NAMD con al menos 500 o 1000 pasos de
dinámica molecular, de modo que el equilibrio de carga tenga la posibilidad de realizarse varias veces,
y todas las CPU y GPU hayan aumentado hasta el 100% la velocidad de reloj.

NAMD proporciona mediciones de rendimiento en "days/ns", esto muestra la cantidad de días
de cómputo requeridos para simular 1 nanosegundo de tiempo real, es decir, cuantos menos días se
requieran, mejor.

Para estimar el rendimiento de NAMD para una simulación larga, Namd muestra
*Benchmark time:* cada cien de pasos de simulación (ver el atributo `numsteps` del archivo de entrada de
NAMD). Esta es una medida del rendimiento de NAMD después de que se hayan completado el inicio y el
equilibrio de carga inicial.

<span style="color: #990819;">*Ejemplo de salida Benchmark time*</span>

```bash
Info: Benchmark time: 20 CPUs 0.471939 s/step 5.46225 days/ns 1015.32 MB memory
```

Para este trabajo, obtenemos el rendimiento \"days/ns\" calculando el promedio de todas las salidas
\"days/ns\" presentes en *Benchmark time*.

Al final de una simulación, NAMD proporciona un resumen de los recursos utilizados.

<span style="color: #990819;">*Ejemplo de salida*</span>

```bash
WallClock: 4783.658691  CPUTime: 4783.658691  Memory: 1137.476562 MB
```

En este trabajo, para calcular su eficiencia paralela, solo nos interesa el tiempo de pared (WallClock).


### ENERGY

Las energías, junto con las temperaturas y presiones, se imprimen cada ciclo `outputEnergies` (presente en
el archivo de entrada) en una sola línea con un prefijo único
para facilitar el procesamiento con utilidades como grep y awk. El formato es el siguiente:

<span style="color: #990819;">*Formato de salida de NAMD*</span>


```bash
ETITLE:      TS           BOND          ANGLE          DIHED          IMPRP
            ELECT            VDW       BOUNDARY           MISC        KINETIC
            TOTAL           TEMP         TOTAL2         TOTAL3        TEMPAVG
        PRESSURE      GPRESSURE         VOLUME       PRESSAVG      GPRESSAVG
```

<span style="color: #990819;">*Ejemplo de salida de NAMD*</span>

```bash
.
.
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
.
.
```

Los valores de energía están en kcal/mol.Para este trabajo nos interesa el promedio del parametro
`TOTAL` que es la suma de las diversas energías potenciales y la energía `KINETIC`.


## Eficiencia paralela

La única forma confiable de ver si un trabajo escala de manera eficiente es compararlo. Comparar un
trabajo significa ejecutar un trabajo de prueba breve y representativo varias veces en diferentes
números de CPU para encontrar un punto óptimo.

A partir de estos datos, se puede calcular la **eficiencia paralela**. Esto se define cómo:

**E = (1/P) \* (T<sub>1</sub>/T<sub>P</sub>)**

- P = Numero de procesadores

- T<sub>1</sub> = tiempo óptimo para el algoritmo en un procesador

- T<sub>P</sub> = tiempo para algoritmo paralelo en P procesadores

Dado que la evaluación comparativa en un solo núcleo a menudo puede llevar mucho tiempo y
la escala dentro de un nodo es generalmente muy buena, para los propósitos del Yoltla es suficiente
hacer este cálculo por nodo, en lugar de por CPU. Para este trabajo, usaremos 1 proceso por core
disponible.

Como regla general, los trabajos que se ejecutan con una gran cantidad de núcleos deben tener
una eficiencia paralela superior o igual a 0,7.


## STMV Benchmark (Junio 2022)

STMV benchmark, 1,066,628 atoms, periodic, PME (disponible
[aquí](https://www.ks.uiuc.edu/Research/namd/utilities/)).

Los days/ns que se indican a continuación son para 10,000 pasos de dinámica molecular, que se
ejecutan en nodos completos por partición.

La simulación debe llegar a un valor `ENERGY:TOTAL` cercano a: `-2457729.98`

![Performance STMV Benchmark.](../../../images/Reframe/Apps/Namd/Figure_STMV.png)

<span style="color: #990819;">*Figure 1. Performance STMV Benchmark.*</span>

\
Para este Benchmark vemos que después de 320 núcleos, los beneficios por solicitar más
recursos se vuelven muy marginales. Usar más recursos que esto resultará en un desperdicio.

Los datos muestran que el uso de nodos *nc* proporciona una mejor aceleración y rendimiento
que otro tipo de nodo.

<span style="color: #990819;">*Table 1. Performance STMV Benchmark*</span>

<table border="1">

<tr>
<th rowspan="2"># Nodos</th>
<th colspan="2">
CPU's Nodos nc<br>
20 Cores x 2.50GHz Intel Xeón E5-2670v2<br>
64GB RAM<br>
Infiniband FDR10/FDR
</th>
<th colspan="2">
CPU's Nodos ttv1[1-58]<br>
20 Cores x 2.60GHz Intel Xeón E5-2660v3<br>
128GB RAM<br>
Infiniband FDR10/FDR
</th>
<th colspan="2">
CPU's Nodos ttv2[59-104]<br>
32 Cores x 2.10GHz Intel Xeon E5-2683v4<br>
256GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th>days/ns</th>
<th>Eficiencia Paralela %</th>
<th>days/ns</th>
<th>Eficiencia Paralela %</th>
<th>days/ns</th>
<th>Eficiencia Paralela %</th>
</tr>

<tr>
<td>1</td>
<td>5.471</td>
<td>100 %</td>
<td>5.658</td>
<td>100 %</td>
<td>4.870</td>
<td>100 %</td>
</tr>

<tr>
<td>2</td>
<td>2.647</td>
<td>100 %</td>
<td>2.732</td>
<td>98 %</td>
<td>3.276</td>
<td>99 %</td>
</tr>

<tr>
<td>4</td>
<td>1.377</td>
<td>95 %</td>
<td>1.472</td>
<td>94 %</td>
<td>2.024</td>
<td>92 %</td>
</tr>

<tr>
<td>5</td>
<td></td>
<td></td>
<td>1.174</td>
<td>91 %</td>
<td></td>
<td></td>
</tr>

<tr>
<td>8</td>
<td>0.707</td>
<td>89 %</td>
<td>0.773</td>
<td>86 %</td>
<td>1.024</td>
<td>88 %</td>
</tr>

<tr>
<td>16</td>
<td>0.362</td>
<td>79 %</td>
<td>0.424</td>
<td>76 %</td>
<td>0.473</td>
<td>73 %</td>
</tr>

</table>


### Performance STMV Benchmark en nodos NC

![Performance STMV Benchmark en nodos NC.](../../../images/Reframe/Apps/Namd/Figure_nc_error_stmv.png)

<span style="color: #990819;">*Figure 2. Performance STMV Benchmark en nodos NC.*</span>

\
<span style="color: #990819;">*Table 2. Performance STMV Benchmark en nodos nc*</span>

<table border="1">

<tr>
<th rowspan="3"># Nodos</th>
<th colspan="6">
CPU's Nodos nc<br>
20 Cores x 2.50GHz Intel Xeón E5-2670v2<br>
64GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th rowspan="2">No. Ejecuciones</th>
<th colspan="4">days/ns</th>
<th rowspan="2">Wallclock (s) Promedio</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>Desviación Estándar</th>
</tr>

<tr>
<td>1</td>
<td>20</td>
<td>5.471</td>
<td>5.419</td>
<td>5.519</td>
<td>0.0300</td>
<td>4816</td>
</tr>

<tr>
<td>2</td>
<td>20</td>
<td>2.640</td>
<td>2.627</td>
<td>2.654</td>
<td>0.0096</td>
<td>2369</td>
</tr>

<tr>
<td>4</td>
<td>20</td>
<td>1.375</td>
<td>1.363</td>
<td>1.413</td>
<td>0.0157</td>
<td>1304</td>
</tr>

<tr>
<td>8</td>
<td>20</td>
<td>0.707</td>
<td>0.699</td>
<td>0.713</td>
<td>0.0054</td>
<td>680</td>
</tr>

<tr>
<td>16</td>
<td>20</td>
<td>0.361</td>
<td>0.358</td>
<td>0.364</td>
<td>0.0026</td>
<td>391</td>
</tr>

</table>


### Performance STMV Benchmark en nodos TTV1

![Performance STMV Benchmark en nodos TTV1.](../../../images/Reframe/Apps/Namd/Figure_ttv1_error_stmv.png)

<span style="color: #990819;">*Figure 3. Performance STMV Benchmark en nodos TTV1.*</span>

\
<span style="color: #990819;">*Table 3. Performance STMV Benchmark en nodos ttv1*</span>

<table border="1">

<tr>
<th rowspan="3"># Nodos</th>
<th colspan="6">
CPU's Nodos ttv1<br>
20 Cores x 2.60GHz Intel Xeón E5-2660v3<br>
128GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th rowspan="2">No. Ejecuciones</th>
<th colspan="4">days/ns</th>
<th rowspan="2">Wallclock (s) Promedio</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>Desviación Estándar</th>
</tr>

<tr>
<td>1</td>
<td>20</td>
<td>5.658</td>
<td>5.627</td>
<td>5.696</td>
<td>0.0246</td>
<td>4860.62</td>
</tr>

<tr>
<td>2</td>
<td>20</td>
<td>2.732</td>
<td>2.724</td>
<td>2.740</td>
<td>0.0080</td>
<td>2433.665</td>
</tr>

<tr>
<td>4</td>
<td>20</td>
<td>1.472</td>
<td>1.376</td>
<td>1.702</td>
<td>0.0814</td>
<td>1292.24</td>
</tr>

<tr>
<td>5</td>
<td>20</td>
<td>1.174</td>
<td>1.117</td>
<td>1.249</td>
<td>0.0336</td>
<td>1063.44</td>
</tr>

<tr>
<td>8</td>
<td>20</td>
<td>0.773</td>
<td>0.735</td>
<td>0.869</td>
<td>0.0417</td>
<td>702.53</td>
</tr>

<tr>
<td>16</td>
<td>20</td>
<td>0.424</td>
<td>0.380</td>
<td>0.660</td>
<td>0.0842</td>
<td>397.65</td>
</tr>

</table>


### Performance STMV Benchmark en nodos TTV2

![Performance STMV Benchmark en nodos TTV2.](../../../images/Reframe/Apps/Namd/Figure_ttv2_error_stmv.png)

<span style="color: #990819;">*Figure 4. Performance STMV Benchmark en nodos TTV2.*</span>

\
<span style="color: #990819;">*Table 4. Performance STMV Benchmark en nodos ttv2*</span>

<table border="1">

<tr>
<th rowspan="3"># Nodos</th>
<th colspan="6">
CPU's Nodos ttv2<br>
32 Cores x 2.10GHz Intel Xeon E5-2683v4<br>
256GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th rowspan="2">No. Ejecuciones</th>
<th colspan="4">days/ns</th>
<th rowspan="2">Wallclock (s) Promedio</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>Desviación Estándar</th>
</tr>

<tr>
<td>1</td>
<td>20</td>
<td>4.870</td>
<td>3.769</td>
<td>5.160</td>
<td>0.5509</td>
<td>4519.31</td>
</tr>

<tr>
<td>2</td>
<td>20</td>
<td>3.276</td>
<td>2.486</td>
<td>7.662</td>
<td>1.6676</td>
<td>2214.67</td>
</tr>

<tr>
<td>4</td>
<td>20</td>
<td>2.024</td>
<td>1.305</td>
<td>7.994</td>
<td>1.6832</td>
<td>1215.76</td>
</tr>

<tr>
<td>8</td>
<td>20</td>
<td>1.024</td>
<td>0.637</td>
<td>3.881</td>
<td>0.8495</td>
<td>636.0</td>
</tr>

<tr>
<td>16</td>
<td>20</td>
<td>0.473</td>
<td>0.326</td>
<td>0.987</td>
<td>0.1744</td>
<td>381.91</td>
</tr>

</table>


### STMV: Múltiples dispositivos GPU en un solo nodo

Evaluación comparativa de STMV Benchmark en un solo nodo con equipos Tesla K20 y V100, con NAMD 2.13.
Las ejecuciones utilizaron todos los núcleos físicos y 2, 4 u 8 dispositivos GPU en el nodo.

![Performance STMV Benchmark en GPUS.](../../../images/Reframe/Apps/Namd/Grafica-STMV-GPU.png)

<span style="color: #990819;">*Figure 5. Performance STMV Benchmark en GPUS.*</span>

La ejecución en un nodo de GPU K20 (1 GPU, 20 núcleos físicos) brinda aproximadamente el mismo
rendimiento que 2 nodos nc (40 núcleos físicos). La ejecución con 4 dispositivos GPU (+ 20 núcleos
físicos) ofrece aproximadamente el mismo rendimiento que en 8 nodos nc (160 núcleos físicos).

Los resultados muestran que el rendimiento de usar 1 GPU V100 es 6 veces mejor que 1 GPU
K20. Utilizar más de una GPU V100 para este Benchmark es ineficiente.

<span style="color: #990819;">*Table 5. Performance STMV Benchmark en GPUS.*</span>

<table border="1">

<tr>
<th rowspan="2"># GPU devices</th>
<th colspan="2">
Nodos GPUs Tesla K20<br>
20 Cores<br>
64GB RAM<br>
Infiniband FDR10/FDR
</th>
<th colspan="2">
Nodos GPUs V100<br>
36 Cores<br>
256GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th>days/ns</th>
<th>WallClock (s)</th>
<th>days/ns</th>
<th>WallClock (s)</th>
</tr>

<tr>
<td>1</td>
<td>2.119</td>
<td>1938</td>
<td>0.368</td>
<td>392</td>
</tr>

<tr>
<td>2</td>
<td>1.287</td>
<td>1171</td>
<td>0.336</td>
<td>373</td>
</tr>

<tr>
<td>4</td>
<td>0.764</td>
<td>745</td>
<td>0.353</td>
<td>391</td>
</tr>

<tr>
<td>8</td>
<td>0.712</td>
<td>684</td>
<td></td>
<td></td>
</tr>

</table>


## F1-ATPase Benchmark (Junio 2022)

F1ATPase benchmark, 327,506 atoms, periodic, PME (disponible
[aquí](https://www.ks.uiuc.edu/Research/namd/utilities/)).

Los days/ns que se indican a continuación son para 10,000 pasos de dinámica molecular, que se
ejecutan en nodos completos por partición.

La simulación debe llegar a un valor `ENERGY:TOTAL` cercano a: `-725159.11`

![Performance F1ATPase Benchmark.](../../../images/Reframe/Apps/Namd/Figure_F1atpase.png)

<span style="color: #990819;">*Figure 6. Performance F1ATPase Benchmark.*</span>

El gráfico de eficiencia muestra que para un sistema molecular pequeño como ATPase, la
eficiencia cae por debajo del 70 % después de 8 nodos, siendo el valor ideal entre 160 y 256 cores para
su ejecución.

Los datos muestran que el uso de nodos *nc* proporciona un mejor rendimiento en las distintas
particiones de nodos presentes en Yoltla.

<span style="color: #990819;">*Table 6. Performance F1ATPase Benchmark*</span>

<table border="1">

<tr>
<th rowspan="2"># Nodos</th>
<th colspan="2">
CPU's Nodos nc<br>
20 Cores x 2.50GHz Intel Xeón E5-2670v2<br>
64GB RAM<br>
Infiniband FDR10/FDR
</th>
<th colspan="2">
CPU's Nodos ttv1[1-58]<br>
20 Cores x 2.60GHz Intel Xeón E5-2660v3<br>
128GB RAM<br>
Infiniband FDR10/FDR
</th>
<th colspan="2">
CPU's Nodos ttv2[59-104]<br>
32 Cores x 2.10GHz Intel Xeon E5-2683v4<br>
256GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th>days/ns</th>
<th>Eficiencia Paralela %</th>
<th>days/ns</th>
<th>Eficiencia Paralela %</th>
<th>days/ns</th>
<th>Eficiencia Paralela %</th>
</tr>

<tr>
<td>1</td>
<td>1.487</td>
<td>100 %</td>
<td>1.591</td>
<td>100 %</td>
<td>1.083</td>
<td>100 %</td>
</tr>

<tr>
<td>2</td>
<td>0.715</td>
<td>98 %</td>
<td>0.738</td>
<td>100 %</td>
<td>0.778</td>
<td>87 %</td>
</tr>

<tr>
<td>4</td>
<td>0.374</td>
<td>88 %</td>
<td>0.398</td>
<td>92 %</td>
<td>0.396</td>
<td>78 %</td>
</tr>

<tr>
<td>5</td>
<td></td>
<td></td>
<td>0.325</td>
<td>89 %</td>
<td></td>
<td></td>
</tr>

<tr>
<td>8</td>
<td>0.197</td>
<td>74 %</td>
<td>0.212</td>
<td>77 %</td>
<td>0.253</td>
<td>66 %</td>
</tr>

<tr>
<td>16</td>
<td>0.101</td>
<td>51 %</td>
<td>0.133</td>
<td>52 %</td>
<td>0.115</td>
<td>39 %</td>
</tr>

</table>


### Performance F1-ATPase Benchmark en nodos NC

![Performance F1ATPase Benchmark en nodos NC.](../../../images/Reframe/Apps/Namd/Figure_nc_error_f1atpase.png)

<span style="color: #990819;">*Figure 7. Performance F1ATPase Benchmark en nodos NC.*</span>

\
<span style="color: #990819;">*Table 7. Performance F1ATPase Benchmark en nodos nc*</span>

<table border="1">

<tr>
<th rowspan="3"># Nodos</th>
<th colspan="6">
CPU's Nodos nc<br>
20 Cores x 2.50GHz Intel Xeón E5-2670v2<br>
64GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th rowspan="2">No. Ejecuciones</th>
<th colspan="4">days/ns</th>
<th rowspan="2">Wallclock (s) Promedio</th>
</tr>
<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>Desviación Estándar</th>
</tr>

<tr>
<td>1</td>
<td>20</td>
<td>1.488</td>
<td>1.482</td>
<td>1.497</td>
<td>0.004</td>
<td>1335.32</td>
</tr>

<tr>
<td>2</td>
<td>20</td>
<td>0.720</td>
<td>0.711</td>
<td>0.782</td>
<td>0.016</td>
<td>678.47</td>
</tr>

<tr>
<td>4</td>
<td>20</td>
<td>0.374</td>
<td>0.372</td>
<td>0.382</td>
<td>0.002</td>
<td>376.60</td>
</tr>

<tr>
<td>8</td>
<td>20</td>
<td>0.197</td>
<td>0.195</td>
<td>0.201</td>
<td>0.002</td>
<td>224.89</td>
</tr>

<tr>
<td>16</td>
<td>20</td>
<td>0.101</td>
<td>0.101</td>
<td>0.102</td>
<td>0.0002</td>
<td>162.74</td>
</tr>

</table>


### Performance F1-ATPase Benchmark en nodos TTV1

![Performance F1ATPase Benchmark en nodos TTV1.](../../../images/Reframe/Apps/Namd/Figure_ttv1_error_f1atpase.png)

<span style="color: #990819;">*Figure 8. Performance F1ATPase Benchmark en nodos TTV1.*</span>

\
<span style="color: #990819;">*Table 8. Performance F1ATPase Benchmark en nodos ttv1*</span>

<table border="1">

<tr>
<th rowspan="3"># Nodos</th>
<th colspan="6">
CPU's Nodos ttv1<br>
20 Cores x 2.60GHz Intel Xeón E5-2660v3<br>
128GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th rowspan="2">No. Ejecuciones</th>
<th colspan="4">days/ns</th>
<th rowspan="2">Wallclock (s) Promedio</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>Desviación Estándar</th>
</tr>

<tr>
<td>1</td>
<td>20</td>
<td>1.591</td>
<td>1.527</td>
<td>1.677</td>
<td>0.069</td>
<td>1433.37</td>
</tr>

<tr>
<td>2</td>
<td>20</td>
<td>0.738</td>
<td>0.727</td>
<td>0.762</td>
<td>0.013</td>
<td>702.08</td>
</tr>

<tr>
<td>4</td>
<td>20</td>
<td>0.398</td>
<td>0.377</td>
<td>0.461</td>
<td>0.020</td>
<td>387.20</td>
</tr>

<tr>
<td>5</td>
<td>20</td>
<td>0.325</td>
<td>0.307</td>
<td>0.404</td>
<td>0.024</td>
<td>321.12</td>
</tr>

<tr>
<td>8</td>
<td>20</td>
<td>0.212</td>
<td>0.198</td>
<td>0.322</td>
<td>0.031</td>
<td>231.30</td>
</tr>

<tr>
<td>16</td>
<td>20</td>
<td>0.133</td>
<td>0.102</td>
<td>0.198</td>
<td>0.036</td>
<td>172.10</td>
</tr>

</table>


### Performance F1-ATPase Benchmark en nodos TTV2

![Performance F1ATPase Benchmark en nodos TTV2.](../../../images/Reframe/Apps/Namd/Figure_ttv2_error_f1atpase.png)

<span style="color: #990819;">*Figure 9. Performance F1ATPase Benchmark en nodos TTV2.*</span>

\
<span style="color: #990819;">*Table 9. Performance F1ATPase Benchmark en nodos ttv2*</span>

<table border="1">

<tr>
<th rowspan="3"># Nodos</th>
<th colspan="6">
CPU's Nodos ttv2<br>
32 Cores x 2.10GHz Intel Xeon E5-2683v4<br>
256GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th rowspan="2">No. Ejecuciones</th>
<th colspan="4">days/ns</th>
<th rowspan="2">Wallclock (s) Promedio</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>Desviación Estándar</th>
</tr>

<tr>
<td>1</td>
<td>20</td>
<td>1.083</td>
<td>0.982</td>
<td>1.365</td>
<td>0.162</td>
<td>1089.27</td>
</tr>

<tr>
<td>2</td>
<td>20</td>
<td>0.778</td>
<td>0.567</td>
<td>1.919</td>
<td>0.358</td>
<td>625.69</td>
</tr>

<tr>
<td>4</td>
<td>20</td>
<td>0.396</td>
<td>0.294</td>
<td>0.884</td>
<td>0.130</td>
<td>346.98</td>
</tr>

<tr>
<td>8</td>
<td>20</td>
<td>0.253</td>
<td>0.168</td>
<td>0.961</td>
<td>0.183</td>
<td>204.90</td>
</tr>

<tr>
<td>16</td>
<td>20</td>
<td>0.115</td>
<td>0.087</td>
<td>0.327</td>
<td>0.051</td>
<td>174.03</td>
</tr>

</table>


### F1-ATPase: Múltiples dispositivos GPU en un solo nodo

Evaluación comparativa de F1-ATPase en un solo nodo con equipos Tesla K20 y V100, con NAMD
2.13. Las ejecuciones utilizaron todos los núcleos físicos y 1, 2, 4 u 8 dispositivos GPU en el nodo.

![Performance ATPase Benchmark en GPUS.](../../../images/Reframe/Apps/Namd/Grafica-ATPASE-GPU.png)

<span style="color: #990819;">*Figure 10. Performance ATPase Benchmark en GPUS.*</span>

La ejecución con 1 dispositivos GPU V100 (+ 36 núcleos físicos) ofrece un rendimiento similar que 8
nodos en los tres tipos de nodo.

Los resultados muestran que el rendimiento de usar 4 GPU V100 es superior a 512 procesos de
nodos ttv2.

<span style="color: #990819;">*Table 10. Performance ATPase Benchmark en GPUS.*</span>

<table border="1">

<tr>
<th rowspan="2"># GPU devices</th>
<th colspan="2">
Nodos GPUs Tesla K20<br>
20 Cores<br>
64GB RAM<br>
Infiniband FDR10/FDR
</th>
<th colspan="2">
Nodos GPUs V100<br>
36 Cores<br>
256GB RAM<br>
Infiniband FDR10/FDR
</th>
</tr>

<tr>
<th>days/ns</th>
<th>WallClock (s)</th>
<th>days/ns</th>
<th>WallClock (s)</th>
</tr>

<tr>
<td>1</td>
<td>0.879</td>
<td>802</td>
<td>0.167</td>
<td>147</td>
</tr>

<tr>
<td>2</td>
<td>0.473</td>
<td>458</td>
<td>0.095</td>
<td>193</td>
</tr>

<tr>
<td>4</td>
<td>0.321</td>
<td>312</td>
<td>0.073</td>
<td>135</td>
</tr>

<tr>
<td>8</td>
<td>0.255</td>
<td>278</td>
<td></td>
<td></td>
</tr>

</table>


## Referencias

[NAMD Benchmarks](https://www.ks.uiuc.edu/Research/namd/utilities/)

[NAMD Performance](https://www.ks.uiuc.edu/Research/namd/2.13/ug/node91.html)

[NAMD Standard Output](http://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-win-html/node28.html)

[Satellite Tobacco Mosaic Virus (STMV)](https://www.ks.uiuc.edu/Research/STMV/#stmv)

[ATP hydrolysis in F1-ATPase](https://www.ks.uiuc.edu/Research/atp_hydrolysis/)
