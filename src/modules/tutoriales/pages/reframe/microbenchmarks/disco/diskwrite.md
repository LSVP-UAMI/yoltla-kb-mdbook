# DiskWrite

## Descripción

La velocidad de escritura de un disco es el parámetro que determina la rapidez con 
la que se puede escribir un archivo en el sistema. Una baja velocidad de escritura 
puede ser signo de un disco defectuoso o de una configuración inadecuada, por lo que 
es importante conocer el valor de este parámetro.

Existen diferentes programas y utilidades para determinar este valor, sin embargo, muchos 
de ellos requieren permisos de superusuario (root) para su ejecución, con el fin de evitar 
este problema, se optó por utilizar el comando `dd` del del paquete 
[GNU Core Utilities](https://www.gnu.org/software/coreutils/).


## Ejecución

1.  Cargue el módulo de Coreutils:

    ```bash
    [t.800@yoltla ~]$ module load coreutils-8.32-gcc-7.2.0-43jmyud
    ```

2.  Ejecute el comando:

    ```bash
    [t.800@yoltla ~]$ sync; dd if=/dev/zero of=/tmp/write_file bs=1M count=1024 oflag=dsync status=progress; sync
    ```

## Salida

A continuación se presenta la salida de una ejecución de esta prueba:

```bash
1064304640 bytes (1.1 GB, 1015 MiB) copied, 5 s, 213 MB/s          (1) 
1024+0 records in                                                  (2) 
1024+0 records out                                                 (3) 
1073741824 bytes (1.1 GB, 1.0 GiB) copied, 5.09788 s, 211 MB/s     (4) 
```

1. Progreso de la ejecución

2. Número de registros leídos

3. Número de registros escritos

4. Bytes copiados, tiempo de ejecución, velocidad final de escritura

## Nodos de cómputo

Unresolved directive in diskwrite.adoc - include::partial\$reframe/nodos_computo.adoc\[\]

## Pruebas

No existe una restricción en el tamaño del archivo a escribir en esta prueba, por lo 
que el criterio para determinar los parámetros de la misma fue el de poder realizar 
pruebas rápidas y fiables. En todos los nodos se utilizaron los mismos parámetros. 
En las siguientas tablas se da un resumen de las pruebas realizadas:

<span style="color: #990819;">*Tabla 1. Pruebas en los nodos NC*</span>

| **Nodo** | **bs** | **count** |
|:--------:|:------:|:---------:|
| nc1      | 1M     | 8192      |
| nc20     | 1M     | 8192      |
| nc26     | 1M     | 8192      |
| nc39     | 1M     | 8192      |
| nc41     | 1M     | 8192      |
| nc56     | 1M     | 8192      |
| nc61     | 1M     | 8192      |
| nc80     | 1M     | 8192      |
| nc81     | 1M     | 8192      |
| nc100    | 1M     | 8192      |
| nc102    | 1M     | 8192      |
| nc120    | 1M     | 8192      |
| nc121    | 1M     | 8192      |
| nc136    | 1M     | 8192      |
| nc141    | 1M     | 8192      |
| nc156    | 1M     | 8192      |

<span style="color: #990819;">*Tabla 2. Pruebas en los nodos TTv1*</span>

| **Nodo** | **bs** | **count** |
|:--------:|:------:|:---------:|
| tt1      | 1M     | 8192      |
| tt9      | 1M     | 8192      |
| tt17     | 1M     | 8192      |
| tt25     | 1M     | 8192      |
| tt33     | 1M     | 8192      |
| tt41     | 1M     | 8192      |
| tt49     | 1M     | 8192      |
| tt58     | 1M     | 8192      |

<span style="color: #990819;">*Tabla 3. Pruebas en los nodos TTv2*</span>

| **Nodo** | **bs** | **count** |
|:--------:|:------:|:---------:|
| tt60     | 1M     | 8192      |
| tt65     | 1M     | 8192      |
| tt74     | 1M     | 8192      |
| tt87     | 1M     | 8192      |
| tt92     | 1M     | 8192      |


```admonish note title=" "
Los nodos no fueron seleccionados bajo ningún criterio en particular, salvo su 
disponibilidad en el cluster, y con el objetivo de obtener una muestra representativa 
de cada tipo de nodo.
```


## Scripts

### Estructura de directorios

Dentro de la carpeta raíz *diskwrite* existen tres subdirectorios, uno por cada tipo 
de nodo en el cluster Yoltla:

    diskwrite
    ├── nc
    │   ├── logs
    │   ├── diskwrite_nc.py
    │   └── src
    ├── ttv1
    │   ├── logs
    │   ├── diskwrite_ttv1.py
    │   └── src
    └── ttv2
        ├── logs
        ├── diskwrite_ttv2.py
        └── src

Cada uno de estos directorios alberga una prueba de ReFrame.

```admonish note title=" "
La versión de coreutils utilizada en estos scripts es la 8.32.
```


### Lanzar pruebas


#### Individualmente

Para lanzar pruebas de forma individual, ubíquese dentro del directorio de la prueba de 
interés, y ejecute el comando:

```bash
reframe -c <nombre_script> -r
```

Por ejemplo, para lanzar la prueba de los nodos NC, ejecute el comando:

```bash
[t.800@yoltla nc]$ reframe -c diskwrite_nc.py -r
```


#### Etiquetas

Utilizando etiquetas puede lanzar múltiples pruebas con un solo comando. Para lanzar 
todas las pruebas, siga los siguientes pasos:

1.  Ubíquese en el directorio raíz *diskwrite*:

    ```bash
    [t.800@yoltla diskwrite]$
    ```

2.  Cree el directorio *logs*:

    ```bash
    [t.800@yoltla diskwrite]$ mkdir logs
    ```

3.  Ejecute el comando:

    ```bash
    [t.800@yoltla diskwrite]$ reframe -c . -R -t disk -t write -r
    ```

```admonish warning title=" "
Si no crea el directorio *logs* obtendrá el siguiente mensaje:

    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: failed to load configuration: [Errno 2] No such file or directory: '/LUSTRE/home/uam/.../t.800/.../diskwrite/logs/rfm.out'
    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: Log file(s) saved in '/tmp/rfm-gj0eh8gb.log'
```


## Resultados


### Nodos NC

<span style="color: #990819;">*Tabla 4. Resultados de la prueba DiskWrite en los nodos NC*</span>

<table border="1">

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Nodo</th>
<th colspan="4">MB/s</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

<tr>
<td>5</td><td>nc1</td><td>26.68</td><td>26.30</td><td>27.20</td><td>0.32</td>
</tr>

<tr>
<td>5</td><td>nc20</td><td>26.56</td><td>26.20</td><td>27.10</td><td>0.32</td>
</tr>

<tr>
<td>5</td><td>nc26</td><td>26.44</td><td>26.10</td><td>26.90</td><td>0.29</td>
</tr>

<tr>
<td>5</td><td>nc39</td><td>26.90</td><td>26.50</td><td>27.60</td><td>0.38</td>
</tr>

<tr>
<td>5</td><td>nc41</td><td>26.44</td><td>26.10</td><td>26.90</td><td>0.29</td>
</tr>

<tr>
<td>5</td><td>nc56</td><td>31.40</td><td>28.80</td><td>32.50</td><td>1.37</td>
</tr>

<tr>
<td>5</td><td>nc61</td><td>26.54</td><td>26.20</td><td>27.10</td><td>0.34</td>
</tr>

<tr>
<td>5</td><td>nc80</td><td>27.20</td><td>26.90</td><td>27.70</td><td>0.31</td>
</tr>

<tr>
<td>5</td><td>nc81</td><td>26.98</td><td>26.60</td><td>27.60</td><td>0.35</td>
</tr>

<tr>
<td>5</td><td>nc100</td><td>27.92</td><td>27.60</td><td>28.30</td><td>0.26</td>
</tr>

<tr>
<td>5</td><td>nc102</td><td>26.32</td><td>26.00</td><td>26.80</td><td>0.28</td>
</tr>

<tr>
<td>5</td><td>nc120</td><td>27.10</td><td>26.80</td><td>27.60</td><td>0.31</td>
</tr>

<tr>
<td>5</td><td>nc121</td><td>26.92</td><td>26.60</td><td>27.50</td><td>0.34</td>
</tr>

<tr>
<td>5</td><td>nc136</td><td>27.28</td><td>26.90</td><td>27.90</td><td>0.35</td>
</tr>

<tr>
<td>5</td><td>nc141</td><td>22.28</td><td>22.00</td><td>22.80</td><td>0.30</td>
</tr>

<tr>
<td>5</td><td>nc156</td><td>26.48</td><td>26.20</td><td>27.00</td><td>0.30</td>
</tr>

</table>

\
<span style="color: #1285E3;">Resultados de la prueba DiskWrite en los nodos NC</span>

![Resultados de la prueba DiskWrite en los nodos NC](../../../../images/Reframe/microBenchmarks/disco/diskwrite/nc.png)

<span style="color: #990819;">*Figura 1. Resultados de la prueba DiskWrite en los nodos NC*</span>


### Nodos TTv1

<span style="color: #990819;">*Tabla 5. Resultados de la prueba DiskWrite en los nodos TTv1*</span>

<table border="1">

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Nodo</th>
<th colspan="4">MB/s</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

<tr>
<td>5</td><td>tt1</td><td>184.80</td><td>183.00</td><td>188.00</td><td>1.72</td>
</tr>

<tr>
<td>5</td><td>tt9</td><td>211.20</td><td>210.00</td><td>212.00</td><td>0.75</td>
</tr>

<tr>
<td>5</td><td>tt17</td><td>210.20</td><td>210.00</td><td>211.00</td><td>0.40</td>
</tr>

<tr>
<td>5</td><td>tt25</td><td>212.00</td><td>212.00</td><td>212.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>tt33</td><td>212.00</td><td>212.00</td><td>212.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>tt41</td><td>190.80</td><td>186.00</td><td>194.00</td><td>3.06</td>
</tr>

<tr>
<td>5</td><td>tt49</td><td>212.20</td><td>212.00</td><td>213.00</td><td>0.40</td>
</tr>

<tr>
<td>5</td><td>tt58</td><td>213.20</td><td>212.00</td><td>214.00</td><td>0.75</td>
</tr>

</table>

\
<span style="color: #1285E3;">Resultados de la prueba DiskWrite en los nodos TTv1</span>

![Resultados de la prueba DiskWrite en los nodos TTv1](../../../../images/Reframe/microBenchmarks/disco/diskwrite/ttv1.png)

<span style="color: #990819;">*Figura 2. Resultados de la prueba DiskWrite en los nodos TTv1*</span>


### Nodos TTv2

<span style="color: #990819;">*Tabla 6. Resultados de la prueba DiskWrite en los nodos TTv2*</span>

<table border="1">

<tr>
<th rowspan="2">No. de ejecuciones</th>
<th rowspan="2">Nodo</th>
<th colspan="4">MB/s</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

<tr>
<td>5</td><td>tt60</td><td>191.60</td><td>191.00</td><td>194.00</td><td>1.20</td>
</tr>

<tr>
<td>5</td><td>tt65</td><td>207.60</td><td>207.00</td><td>208.00</td><td>0.49</td>
</tr>

<tr>
<td>5</td><td>tt74</td><td>206.80</td><td>206.00</td><td>207.00</td><td>0.40</td>
</tr>

<tr>
<td>5</td><td>tt87</td><td>208.00</td><td>208.00</td><td>208.00</td><td>0.00</td>
</tr>

<tr>
<td>5</td><td>tt92</td><td>189.40</td><td>189.00</td><td>190.00</td><td>0.49</td>
</tr>

</table>

\
<span style="color: #1285E3;">Resultados de la prueba DiskWrite en los nodos TTv2</span>

![Resultados de la prueba DiskWrite en los nodos TTv2](../../../../images/Reframe/microBenchmarks/disco/diskwrite/ttv2.png)

<span style="color: #990819;">*Figura 3. Resultados de la prueba DiskWrite en los nodos TTv2*</span>


### Yoltla

<span style="color: #990819;">*Tabla 7. Resultados de la prueba DiskWrite en el cluster Yoltla*</span>

<table border="1">

<tr>
<th rowspan="2">Nodos</th>
<th colspan="4">MB/s</th>
</tr>

<tr>
<th>Promedio</th>
<th>Mínimo</th>
<th>Máximo</th>
<th>σ</th>
</tr>

<tr>
<td>NC</td><td>26.84</td><td>22.00</td><td>32.50</td><td>1.72</td>
</tr>

<tr>
<td>TTv1</td><td>205.80</td><td>183.00</td><td>214.00</td><td>10.61</td>
</tr>

<tr>
<td>TTv2</td><td>200.68</td><td>189.00</td><td>208.00</td><td>8.37</td>
</tr>

</table>

\
<span style="color: #1285E3;">Resultados de la prueba DiskWrite en el cluster Yoltla</span>

![Resultados de la prueba DiskWrite en el cluster Yoltla](../../../../images/Reframe/microBenchmarks/disco/diskwrite/yoltla.png)

<span style="color: #990819;">*Figura 4. Resultados de la prueba DiskWrite en el cluster Yoltla*</span>

```admonish note title=" "
Todos los resultados mostrados en esta sección fueron obtenidos en el mes de Agosto del 2022.
```

## Sitios de interés

- [dd: Convert and copy a file](https://www.gnu.org/software/coreutils/manual/coreutils.html#dd-invocation)

- [Tuning dd block size](http://blog.tdg5.com/tuning-dd-block-size/)
