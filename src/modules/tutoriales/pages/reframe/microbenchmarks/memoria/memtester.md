# Descripción

memtester es una utilidad para probar el subsistema de memoria en una computadora para determinar si está defectuoso.

Para obtener más información, visite el sitio oficial de [memtester](https://pyropus.ca./software/memtester/).

# Compilación

1.  Descargue el [código fuente](https://pyropus.ca./software/memtester/old-versions/memtester-4.5.1.tar.gz) de memtester:

    ``` shell
    [t.800@yoltla Descargas]$ wget --no-check-certificate https://pyropus.ca./software/memtester/old-versions/memtester-4.5.1.tar.gz
    --2022-08-09 10:48:21--  https://pyropus.ca./software/memtester/old-versions/memtester-4.5.1.tar.gz
    Resolving pyropus.ca.... 96.126.125.117
    Connecting to pyropus.ca.|96.126.125.117|:443... connected.
    WARNING: cannot verify pyropus.ca.’s certificate, issued by “/C=US/O=Let's Encrypt/CN=R3”:
      Issued certificate has expired.
    WARNING: no certificate subject alternative name matches
            requested host name “pyropus.ca.”.
    HTTP request sent, awaiting response... 200 OK
    Length: 23655 (23K) [application/x-gzip]
    Saving to: “memtester-4.5.1.tar.gz”

    100%[===================================================================================================>] 23,655      --.-K/s   in 0.03s

    2022-08-09 10:48:22 (783 KB/s) - “memtester-4.5.1.tar.gz” saved [23655/23655]
    ```

2.  Descomprima el archivo *memtester-4.5.1.tar.gz*:

    ``` shell
    [t.800@yoltla Descargas]$ tar -xvf memtester-4.5.1.tar.gz
    memtester-4.5.1/
    memtester-4.5.1/tests.h
    memtester-4.5.1/make-load.sh
    memtester-4.5.1/BUGS
    memtester-4.5.1/memtester.c
    memtester-4.5.1/COPYING
    memtester-4.5.1/tests.c
    memtester-4.5.1/CHANGELOG
    memtester-4.5.1/memtester.h
    memtester-4.5.1/make-compile.sh
    memtester-4.5.1/find-systype.sh
    memtester-4.5.1/README.tests
    memtester-4.5.1/types.h
    memtester-4.5.1/trycpp.c
    memtester-4.5.1/memtester.8
    memtester-4.5.1/warn-auto.sh
    memtester-4.5.1/README
    memtester-4.5.1/conf-ld
    memtester-4.5.1/extra-libs.sh
    memtester-4.5.1/make-makelib.sh
    memtester-4.5.1/conf-cc
    memtester-4.5.1/Makefile
    memtester-4.5.1/sizes.h
    ```

3.  Cambie al directorio *memtester-4.5.1*:

    ``` shell
    [t.800@yoltla Descargas]$ cd memtester-4.5.1
    [t.800@yoltla memtester-4.5.1]$
    ```

4.  Cargue el módulo de GCC:

    ``` shell
    [t.800@yoltla memtester-4.5.1]$ module load gcc/7.2.0
    ```

5.  Ejecute el comando `make`:

    ``` shell
    [t.800@yoltla memtester-4.5.1]$ make
    ( cat warn-auto.sh; \
            echo CC=\'`head -1 conf-cc`\'; \
            echo LD=\'`head -1 conf-ld`\' \
            ) > auto-ccld.sh
    cat auto-ccld.sh make-compile.sh > make-compile
    chmod 755 make-compile
    cat auto-ccld.sh find-systype.sh > find-systype
    chmod 755 find-systype
    ./find-systype > systype
    ( cat warn-auto.sh; ./make-compile "`cat systype`" ) > \
            compile
    chmod 755 compile
    ./compile memtester.c
    ./compile tests.c
    cat auto-ccld.sh make-load.sh > make-load
    chmod 755 make-load
    ( cat warn-auto.sh; ./make-load "`cat systype`" ) > load
    chmod 755 load
    ./extra-libs.sh "`cat systype`" >extra-libs
    ./load memtester tests.o `cat extra-libs`
    ```

# Ejecución

Para ejecutar memtester, siga el siguiente formato:

    memtester <memoria> [iteraciones]

+-----------------------------------+-----------------------------------+
| Opción                            | Descripción                       |
+===================================+===================================+
| \<memoria\>                       | Es la cantidad de memoria a       |
|                                   | probar, en megabytes por          |
|                                   | defecto.\                         |
|                                   | Opcionalmente, puede incluir un   |
|                                   | sufijo de B, K, M o G (para       |
|                                   | bytes, kilobytes, megabytes y     |
|                                   | gigabytes, respectivamente).      |
+-----------------------------------+-----------------------------------+
| \[iteraciones\]                   | Es un límite opcional para el     |
|                                   | número de ejecuciones a través de |
|                                   | todas las pruebas.                |
+-----------------------------------+-----------------------------------+

Para este ejemplo, utilice el comando:

``` shell
[t.800@yoltla memtester-4.5.1]$ ./memtester 100M 1
```

# Salida

A continuación se presenta la salida de una ejecución de memtester:

``` shell
memtester version 4.5.1 (64-bit)
Copyright (C) 2001-2020 Charles Cazabon.
Licensed under the GNU General Public License version 2 (only).

pagesize is 4096
pagesizemask is 0xfffffffffffff000
want 100MB (104857600 bytes)
got  100MB (104857600 bytes), trying mlock ...locked.
Loop 1/1:
  Stuck Address       : ok  
  Random Value        : ok  
  Compare XOR         : ok  
  Compare SUB         : ok  
  Compare MUL         : ok  
  Compare DIV         : ok  
  Compare OR          : ok  
  Compare AND         : ok  
  Sequential Increment: ok  
  Solid Bits          : ok  
  Block Sequential    : ok  
  Checkerboard        : ok  
  Bit Spread          : ok  
  Bit Flip            : ok  
  Walking Ones        : ok  
  Walking Zeroes      : ok  
  8-bit Writes        : ok
  16-bit Writes       : ok

Done.
```

- Determina si las ubicaciones de memoria a las que el programa intenta acceder están direccionadas correctamente o no. Si esta prueba informa errores, es casi seguro que hay un problema en alguna parte del subsistema de memoria. Los resultados del resto de las pruebas no se pueden considerar precisos si esta prueba falla.

- Estas pruebas detectan principalmente errores de memoria debido a bits defectuosos que están permanentemente atascados en un nivel alto o bajo.

- Estas pruebas capturan bits escamosos (flaky bits), que pueden o no tener un valor real.

- Estas pruebas detectan bits defectuosos que dependen de los valores actuales de los bits circundantes en la misma word32, o en las word32s anteriores y posteriores.

# Nodos de cómputo

Unresolved directive in memtester.adoc - include::partial\$reframe/nodos_computo.adoc\[\]

# Scripts

## Estructura de directorios

Dentro de la carpeta raíz *memtester* existen tres subdirectorios, uno por cada tipo de nodo en el cluster Yoltla:

    memtester
    ├── nc
    │   ├── logs
    │   ├── memtester_nc.py
    │   └── src
    ├── ttv1
    │   ├── logs
    │   ├── memtester_ttv1.py
    │   └── src
    └── ttv2
        ├── logs
        ├── memtester_ttv2.py
        └── src

Cada uno de estos directorios alberga una prueba de ReFrame.

:::: note
::: title
:::

La versión de memtester utilizada en estos scripts es la 4.3.0.
::::

## Lanzar pruebas

### **Individualmente**

Para lanzar pruebas de forma individual, ubíquese dentro del directorio de la prueba de interés, y ejecute el comando:

``` shell
reframe -c <nombre_script> -r
```

Por ejemplo, para lanzar la prueba de los nodos NC, ejecute el comando:

``` shell
[t.800@yoltla nc]$ reframe -c memtester_nc.py -r
```

### **Etiquetas**

Utilizando etiquetas puede lanzar múltiples pruebas con un solo comando. Para lanzar todas las pruebas, siga los siguientes pasos:

1.  Ubíquese en el directorio raíz *memtester*:

    ``` shell
    [t.800@yoltla memtester]$
    ```

2.  Cree el directorio *logs*:

    ``` shell
    [t.800@yoltla memtester]$ mkdir logs
    ```

3.  Ejecute el comando:

    ``` shell
    [t.800@yoltla memtester]$ reframe -c . -R -t memtester -r
    ```

:::: warning
::: title
:::

Si no crea el directorio *logs* obtendrá el siguiente mensaje:

    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: failed to load configuration: [Errno 2] No such file or directory: '/LUSTRE/home/uam/.../t.800/.../memtester/logs/rfm.out'
    /LUSTRE/home/uam/.../t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/reframe-3.9.2-gqmjpwbafkinwklzww777oktqutklrfn/bin/reframe: Log file(s) saved in '/tmp/rfm-jxeonz2e.log'
::::

# Sitios de interés

- [memtester](https://pyropus.ca./software/memtester/)
