# Descripción

La velocidad de lectura de un disco es el parámetro que determina la rapidez con la 
que se puede leer un archivo en el sistema. Una baja velocidad de lectura puede ser 
signo de un disco defectuoso o de una configuración inadecuada, por lo que es importante 
conocer el valor de este parámetro.

Existen diferentes programas y utilidades para determinar este valor, sin embargo, muchos 
de ellos requieren permisos de superusuario (root) para su ejecución, con el fin de evitar 
este problema, se optó por utilizar el comando `dd` del del paquete 
[GNU Core Utilities](https://www.gnu.org/software/coreutils/).

# Ejecución

1.  Cargue el módulo de Coreutils:

    ```bash
    [t.800@yoltla ~]$ module load coreutils-8.32-gcc-7.2.0-43jmyud
    ```

2.  Cree el archivo a leer:

    ```bash
    [t.800@yoltla ~]$ sync; dd if=/dev/zero of=/tmp/read_file bs=1M count=2048 oflag=dsync status=progress; sync
    ```

3.  Descarte de la memoria caché los datos del archivo a leer:

    ```bash
    [t.800@yoltla ~]$ dd if=/tmp/read_file iflag=nocache count=0
    [t.800@yoltla ~]$ dd of=/tmp/read_file oflag=nocache conv=notrunc,fdatasync count=0
    ```

4.  Ejecute el comando:

    ```bash
    [t.800@yoltla ~]$ sync; dd if=/tmp/read_file of=/dev/null bs=1M status=progress; sync
    ```

# Salida

A continuación se presenta la salida de una ejecución de esta prueba:

```bash
1357905920 bytes (1.4 GB, 1.3 GiB) copied, 7 s, 194 MB/s          (1)  
2048+0 records in                                                 (2) 
2048+0 records out                                                (3)
2147483648 bytes (2.1 GB, 2.0 GiB) copied, 7.73725 s, 278 MB/s    (4)  
```

1. Progreso de la ejecución

2. Número de registros leídos

3. Número de registros escritos

4. Bytes copiados, tiempo de ejecución, velocidad final de lectura


# Nodos de cómputo

Unresolved directive in diskread.adoc - include::partial\$reframe/nodos_computo.adoc\[\]

# Pruebas

No existe una restricción en el tamaño del archivo a leer en esta prueba, por lo que el 
criterio para determinar los parámetros de la misma fue el de poder realizar pruebas 
rápidas y fiables. En todos los nodos se utilizaron los mismos parámetros. En las siguientas 
tablas se da un resumen de las pruebas realizadas:

<span style="color: #990819;">*Tabla 1. Pruebas en los nodos NC*</span>

| **Nodo** | **bs** | **count** |
|----------|--------|-----------|
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

<span style="color: #990819;">*Pruebas en los nodos TTv1*</span>

| **Nodo** | **bs** | **count** |
|----------|--------|-----------|
| tt1      | 1M     | 8192      |
| tt9      | 1M     | 8192      |
| tt17     | 1M     | 8192      |
| tt25     | 1M     | 8192      |
| tt33     | 1M     | 8192      |
| tt41     | 1M     | 8192      |
| tt49     | 1M     | 8192      |
| tt58     | 1M     | 8192      |


<span style="color: #990819;">*Pruebas en los nodos TTv2*</span>

| **Nodo** | **bs** | **count** |
|----------|--------|-----------|
| tt60     | 1M     | 8192      |
| tt65     | 1M     | 8192      |
| tt74     | 1M     | 8192      |
| tt87     | 1M     | 8192      |
| tt92     | 1M     | 8192      |

```admonish info title=" "
Los nodos no fueron seleccionados bajo ningún criterio en particular, salvo su disponibilidad en el cluster, y con el objetivo de obtener una muestra representativa de cada tipo de nodo.
```


# Scripts


## Estructura de directorios

Dentro de la carpeta raíz *diskread* existen tres subdirectorios, uno por cada tipo 
de nodo en el cluster Yoltla:

    diskread
    ├── nc
    │   ├── logs
    │   ├── diskread_nc.py
    │   └── src
    ├── ttv1
    │   ├── logs
    │   ├── diskread_ttv1.py
    │   └── src
    └── ttv2
        ├── logs
        ├── diskread_ttv2.py
        └── src

Cada uno de estos directorios alberga una prueba de ReFrame.

```admonish info title=" "
La versión de coreutils utilizada en estos scripts es la 8.32.
```


## Lanzar pruebas


### **Individualmente**

Para lanzar pruebas de forma individual, ubíquese dentro del directorio de la prueba 
de interés, y ejecute el comando:

```bash
reframe -c <nombre_script> -r
```

Por ejemplo, para lanzar la prueba de los nodos NC, ejecute el comando:

```bash
[t.800@yoltla nc]$ reframe -c diskread_nc.py -r
```


### **Etiquetas**

Utilizando etiquetas puede lanzar múltiples pruebas con un solo comando. Para lanzar 
todas las pruebas, siga los siguientes pasos:

1.  Ubíquese en el directorio raíz *diskread*:

    ```bash
    [t.800@yoltla diskread]$
    ```

2.  Cree el directorio *logs*:

    ```bash
    [t.800@yoltla diskread]$ mkdir logs
    ```

3.  Ejecute el comando:

    ```bash
    [t.800@yoltla diskread]$ reframe -c . -R -t disk -t read -r
    ```

```admonish warning title=" "
Si no crea el directorio *logs* obtendrá el siguiente mensaje:

    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: failed to load configuration: [Errno 2] No such file or directory: '/LUSTRE/home/uam/.../t.800/.../diskread/logs/rfm.out'
    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: Log file(s) saved in '/tmp/rfm-gj0eh8gb.log'
```


# Resultados


## Nodos NC

<span style="color: #990819;">*Pruebas en los nodos TTv2*</span>
```
+---------------+----------+--------------+--------------+--------------+--------------+
| **No. de\     | **Nodo** | **MB/s**                                                  |
| ejecuciones** |          |                                                           |
|               |          +--------------+--------------+--------------+--------------+
|               |          | **Promedio** | **Mínimo**   | **Máximo**   | **σ**        |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc1      | 168.00       | 168.00       | 168.00       | 0.00         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc20     | 170.00       | 170.00       | 170.00       | 0.00         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc26     | 171.20       | 171.00       | 172.00       | 0.40         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc39     | 173.20       | 172.00       | 174.00       | 0.75         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc41     | 158.40       | 158.00       | 159.00       | 0.49         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc56     | 143.00       | 139.00       | 146.00       | 2.90         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc61     | 165.60       | 165.00       | 166.00       | 0.49         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc80     | 166.00       | 164.00       | 168.00       | 1.79         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc81     | 168.40       | 155.00       | 173.00       | 6.86         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc100    | 161.40       | 158.00       | 163.00       | 2.06         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc102    | 162.00       | 160.00       | 163.00       | 1.26         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc120    | 169.80       | 164.00       | 173.00       | 3.12         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc121    | 165.60       | 164.00       | 167.00       | 1.02         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc136    | 166.20       | 166.00       | 167.00       | 0.40         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc141    | 128.02       | 97.10        | 136.00       | 15.46        |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc156    | 169.00       | 169.00       | 169.00       | 0.00         |
+---------------+----------+--------------+--------------+--------------+--------------+
```
\
<span style="color: #1285E3;">Resultados de la prueba DiskRead en los nodos NC</span>

![Resultados de la prueba DiskRead en los nodos NC](../../../../images/Reframe/microBenchmarks/disco/diskread/nc.png)

<span style="color: #990819;">*Figura 1. Resultados de la prueba DiskRead en los nodos NC*</span>


## Nodos TTv1

<span style="color: #990819;">*Tabla 5. Resultados de la prueba DiskRead en los nodos TTv1*</span>
```
+---------------+----------+--------------+--------------+--------------+--------------+
| **No. de\     | **Nodo** | **MB/s**                                                  |
| ejecuciones** |          |                                                           |
|               |          +--------------+--------------+--------------+--------------+
|               |          | **Promedio** | **Mínimo**   | **Máximo**   | **σ**        |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt1      | 115.20       | 112.00       | 116.00       | 1.60         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt9      | 283.80       | 281.00       | 286.00       | 1.72         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt17     | 281.00       | 278.00       | 283.00       | 1.79         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt25     | 280.60       | 280.00       | 283.00       | 1.20         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt33     | 283.40       | 281.00       | 287.00       | 1.96         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt41     | 115.20       | 112.00       | 116.00       | 1.60         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt49     | 280.80       | 279.00       | 284.00       | 1.83         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt58     | 280.00       | 273.00       | 285.00       | 4.10         |
+---------------+----------+--------------+--------------+--------------+--------------+
```
\
<span style="color: #1285E3;">Resultados de la prueba DiskRead en los nodos TTv1</span>

![Resultados de la prueba DiskRead en los nodos TTv1](../../../../images/Reframe/microBenchmarks/disco/diskread/ttv1.png)

<span style="color: #990819;">*Figura 2. Resultados de la prueba DiskRead en los nodos TTv1*</span>


## Nodos TTv2

<span style="color: #990819;">*Tabla 6. Resultados de la prueba DiskRead en los nodos TTv2*</span>
```
+---------------+----------+--------------+--------------+--------------+--------------+
| **No. de\     | **Nodo** | **MB/s**                                                  |
| ejecuciones** |          |                                                           |
|               |          +--------------+--------------+--------------+--------------+
|               |          | **Promedio** | **Mínimo**   | **Máximo**   | **σ**        |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt60     | 115.40       | 113.00       | 116.00       | 1.20         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt65     | 264.60       | 263.00       | 266.00       | 1.36         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt74     | 266.00       | 265.00       | 267.00       | 0.63         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt87     | 257.80       | 248.00       | 265.00       | 6.58         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt92     | 114.00       | 112.00       | 115.00       | 1.26         |
+---------------+----------+--------------+--------------+--------------+--------------+
```
\
<span style="color: #1285E3;">Resultados de la prueba DiskRead en los nodos TTv2</span>

![Resultados de la prueba DiskRead en los nodos TTv2](../../../../images/Reframe/microBenchmarks/disco/diskread/ttv2.png)

<span style="color: #990819;">*Figura 3. Resultados de la prueba DiskRead en los nodos TTv2*</span>


## Yoltla

<span style="color: #990819;">*Tabla 7. Resultados de la prueba DiskRead en el cluster Yoltla*</span>
```
+-------------+-----------------+-----------------+-----------------+-----------------+
| **Nodos**   | **MB/s**                                                              |
|             +-----------------+-----------------+-----------------+-----------------+
|             | **Promedio**    | **Mínimo**      | **Máximo**      | **σ**           |
+-------------+-----------------+-----------------+-----------------+-----------------+
| NC          | 162.86          | 97.10           | 174.00          | 12.13           |
+-------------+-----------------+-----------------+-----------------+-----------------+
| TTv1        | 240.00          | 112.00          | 287.00          | 72.10           |
+-------------+-----------------+-----------------+-----------------+-----------------+
| TTv2        | 203.56          | 112.00          | 267.00          | 72.68           |
+-------------+-----------------+-----------------+-----------------+-----------------+
```
\
<span style="color: #1285E3;">Resultados de la prueba DiskRead en el cluster Yoltla</span>

![Resultados de la prueba DiskRead en el cluster Yoltla](../../../../images/Reframe/microBenchmarks/disco/diskread/yoltla.png)

<span style="color: #990819;">*Figura 4. Resultados de la prueba DiskRead en el cluster Yoltla*</span>

```admonish info title=" "
Todos los resultados mostrados en esta sección fueron obtenidos en el mes de Agosto del 2022.
```

# Sitios de interés

- [dd: Convert and copy a file](https://www.gnu.org/software/coreutils/manual/coreutils.html#dd-invocation)

- [Tuning dd block size](http://blog.tdg5.com/tuning-dd-block-size/)
