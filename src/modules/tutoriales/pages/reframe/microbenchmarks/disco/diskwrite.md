# Descripción

La velocidad de escritura de un disco es el parámetro que determina la rapidez con la que se puede escribir un archivo en el sistema. Una baja velocidad de escritura puede ser signo de un disco defectuoso o de una configuración inadecuada, por lo que es importante conocer el valor de este parámetro.

Existen diferentes programas y utilidades para determinar este valor, sin embargo, muchos de ellos requieren permisos de superusuario (root) para su ejecución, con el fin de evitar este problema, se optó por utilizar el comando `dd` del del paquete [GNU Core Utilities](https://www.gnu.org/software/coreutils/).

# Ejecución

1.  Cargue el módulo de Coreutils:

    ``` shell
    [t.800@yoltla ~]$ module load coreutils-8.32-gcc-7.2.0-43jmyud
    ```

2.  Ejecute el comando:

    ``` shell
    [t.800@yoltla ~]$ sync; dd if=/dev/zero of=/tmp/write_file bs=1M count=1024 oflag=dsync status=progress; sync
    ```

# Salida

A continuación se presenta la salida de una ejecución de esta prueba:

    1064304640 bytes (1.1 GB, 1015 MiB) copied, 5 s, 213 MB/s           
    1024+0 records in                                                   
    1024+0 records out                                                  
    1073741824 bytes (1.1 GB, 1.0 GiB) copied, 5.09788 s, 211 MB/s      

- Progreso de la ejecución

- Número de registros leídos

- Número de registros escritos

- Bytes copiados, tiempo de ejecución, velocidad final de escritura

# Nodos de cómputo

Unresolved directive in diskwrite.adoc - include::partial\$reframe/nodos_computo.adoc\[\]

# Pruebas

No existe una restricción en el tamaño del archivo a escribir en esta prueba, por lo que el criterio para determinar los parámetros de la misma fue el de poder realizar pruebas rápidas y fiables. En todos los nodos se utilizaron los mismos parámetros. En las siguientas tablas se da un resumen de las pruebas realizadas:

+----------------------+----------------------+-----------------------+
| Nodo                 | bs                   | count                 |
+======================+======================+=======================+
| nc1                  | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc20                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc26                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc39                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc41                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc56                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc61                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc80                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc81                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc100                | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc102                | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc120                | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc121                | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc136                | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc141                | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| nc156                | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+

: Pruebas en los nodos NC

+----------------------+----------------------+-----------------------+
| Nodo                 | bs                   | count                 |
+======================+======================+=======================+
| tt1                  | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt9                  | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt17                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt25                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt33                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt41                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt49                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt58                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+

: Pruebas en los nodos TTv1

+----------------------+----------------------+-----------------------+
| Nodo                 | bs                   | count                 |
+======================+======================+=======================+
| tt60                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt65                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt74                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt87                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+
| tt92                 | 1M                   | 8192                  |
+----------------------+----------------------+-----------------------+

: Pruebas en los nodos TTv2

:::: note
::: title
:::

Los nodos no fueron seleccionados bajo ningún criterio en particular, salvo su disponibilidad en el cluster, y con el objetivo de obtener una muestra representativa de cada tipo de nodo.
::::

# Scripts

## Estructura de directorios

Dentro de la carpeta raíz *diskwrite* existen tres subdirectorios, uno por cada tipo de nodo en el cluster Yoltla:

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

:::: note
::: title
:::

La versión de coreutils utilizada en estos scripts es la 8.32.
::::

## Lanzar pruebas

### **Individualmente**

Para lanzar pruebas de forma individual, ubíquese dentro del directorio de la prueba de interés, y ejecute el comando:

``` shell
reframe -c <nombre_script> -r
```

Por ejemplo, para lanzar la prueba de los nodos NC, ejecute el comando:

``` shell
[t.800@yoltla nc]$ reframe -c diskwrite_nc.py -r
```

### **Etiquetas**

Utilizando etiquetas puede lanzar múltiples pruebas con un solo comando. Para lanzar todas las pruebas, siga los siguientes pasos:

1.  Ubíquese en el directorio raíz *diskwrite*:

    ``` shell
    [t.800@yoltla diskwrite]$
    ```

2.  Cree el directorio *logs*:

    ``` shell
    [t.800@yoltla diskwrite]$ mkdir logs
    ```

3.  Ejecute el comando:

    ``` shell
    [t.800@yoltla diskwrite]$ reframe -c . -R -t disk -t write -r
    ```

:::: warning
::: title
:::

Si no crea el directorio *logs* obtendrá el siguiente mensaje:

    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: failed to load configuration: [Errno 2] No such file or directory: '/LUSTRE/home/uam/.../t.800/.../diskwrite/logs/rfm.out'
    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: Log file(s) saved in '/tmp/rfm-gj0eh8gb.log'
::::

# Resultados

## Nodos NC

+---------------+----------+--------------+--------------+--------------+--------------+
| **No. de\     | **Nodo** | **MB/s**                                                  |
| ejecuciones** |          |                                                           |
|               |          +--------------+--------------+--------------+--------------+
|               |          | **Promedio** | **Mínimo**   | **Máximo**   | **σ**        |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc1      | 26.68        | 26.30        | 27.20        | 0.32         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc20     | 26.56        | 26.20        | 27.10        | 0.32         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc26     | 26.44        | 26.10        | 26.90        | 0.29         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc39     | 26.90        | 26.50        | 27.60        | 0.38         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc41     | 26.44        | 26.10        | 26.90        | 0.29         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc56     | 31.40        | 28.80        | 32.50        | 1.37         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc61     | 26.54        | 26.20        | 27.10        | 0.34         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc80     | 27.20        | 26.90        | 27.70        | 0.31         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc81     | 26.98        | 26.60        | 27.60        | 0.35         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc100    | 27.92        | 27.60        | 28.30        | 0.26         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc102    | 26.32        | 26.00        | 26.80        | 0.28         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc120    | 27.10        | 26.80        | 27.60        | 0.31         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc121    | 26.92        | 26.60        | 27.50        | 0.34         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc136    | 27.28        | 26.90        | 27.90        | 0.35         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc141    | 22.28        | 22.00        | 22.80        | 0.30         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | nc156    | 26.48        | 26.20        | 27.00        | 0.30         |
+---------------+----------+--------------+--------------+--------------+--------------+

: Resultados de la prueba DiskWrite en los nodos NC

![Resultados de la prueba DiskWrite en los nodos NC](Reframe/microBenchmarks/disco/diskwrite/nc.png)

## Nodos TTv1

+---------------+----------+--------------+--------------+--------------+--------------+
| **No. de\     | **Nodo** | **MB/s**                                                  |
| ejecuciones** |          |                                                           |
|               |          +--------------+--------------+--------------+--------------+
|               |          | **Promedio** | **Mínimo**   | **Máximo**   | **σ**        |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt1      | 184.80       | 183.00       | 188.00       | 1.72         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt9      | 211.20       | 210.00       | 212.00       | 0.75         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt17     | 210.20       | 210.00       | 211.00       | 0.40         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt25     | 212.00       | 212.00       | 212.00       | 0.00         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt33     | 212.00       | 212.00       | 212.00       | 0.00         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt41     | 190.80       | 186.00       | 194.00       | 3.06         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt49     | 212.20       | 212.00       | 213.00       | 0.40         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt58     | 213.20       | 212.00       | 214.00       | 0.75         |
+---------------+----------+--------------+--------------+--------------+--------------+

: Resultados de la prueba DiskWrite en los nodos TTv1

![Resultados de la prueba DiskWrite en los nodos TTv1](Reframe/microBenchmarks/disco/diskwrite/ttv1.png)

## Nodos TTv2

+---------------+----------+--------------+--------------+--------------+--------------+
| **No. de\     | **Nodo** | **MB/s**                                                  |
| ejecuciones** |          |                                                           |
|               |          +--------------+--------------+--------------+--------------+
|               |          | **Promedio** | **Mínimo**   | **Máximo**   | **σ**        |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt60     | 191.60       | 191.00       | 194.00       | 1.20         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt65     | 207.60       | 207.00       | 208.00       | 0.49         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt74     | 206.80       | 206.00       | 207.00       | 0.40         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt87     | 208.00       | 208.00       | 208.00       | 0.00         |
+---------------+----------+--------------+--------------+--------------+--------------+
| 5             | tt92     | 189.40       | 189.00       | 190.00       | 0.49         |
+---------------+----------+--------------+--------------+--------------+--------------+

: Resultados de la prueba DiskWrite en los nodos TTv2

![Resultados de la prueba DiskWrite en los nodos TTv2](Reframe/microBenchmarks/disco/diskwrite/ttv2.png)

## Yoltla

+-------------+-----------------+-----------------+-----------------+-----------------+
| **Nodos**   | **MB/s**                                                              |
|             +-----------------+-----------------+-----------------+-----------------+
|             | **Promedio**    | **Mínimo**      | **Máximo**      | **σ**           |
+-------------+-----------------+-----------------+-----------------+-----------------+
| NC          | 26.84           | 22.00           | 32.50           | 1.72            |
+-------------+-----------------+-----------------+-----------------+-----------------+
| TTv1        | 205.80          | 183.00          | 214.00          | 10.61           |
+-------------+-----------------+-----------------+-----------------+-----------------+
| TTv2        | 200.68          | 189.00          | 208.00          | 8.37            |
+-------------+-----------------+-----------------+-----------------+-----------------+

: Resultados de la prueba DiskWrite en el cluster Yoltla

![Resultados de la prueba DiskWrite en el cluster Yoltla](Reframe/microBenchmarks/disco/diskwrite/yoltla.png)

:::: note
::: title
:::

Todos los resultados mostrados en esta sección fueron obtenidos en el mes de Agosto del 2022.
::::

# Sitios de interés

- [dd: Convert and copy a file](https://www.gnu.org/software/coreutils/manual/coreutils.html#dd-invocation)

- [Tuning dd block size](http://blog.tdg5.com/tuning-dd-block-size/)
