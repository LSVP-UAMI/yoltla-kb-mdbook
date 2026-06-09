# Manual para instalar vvgpu-smi-snmp


## Introducción

En este documento se explica como se realizo la instalación de 
[Nvgpu-smi-snmp](http://sourceforge.net/p/nvgpu-smi-snmp/code/ci/master/tree) 
en los nodos con gpus.

[Nvgpu-smi-snmp](https://sourceforge.net/p/nvgpu-smi-snmp/code/ci/master/tree/) es un 
modulo para [Net-SNMP](http://www.net-snmp.org) que permite obtener metricas de las 
gpus de nvidia y enviarlas por red mediante el protocolo SNMP.


## Requisitos previos

1.  Centos 6.10 o superior

2.  Singularity 2.6 [Como instalar](https://sylabs.io/guides/2.6/user-guide/installation.html)

3.  Tarjeta grafica Nvidia (GeForce/Quadro/Tesla)

4.  Controladores de Nvidia y nvidia-smi [Como instalar](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)


## Instalación

Para la instalación se utilizó un contenedor de [Singularity 2.6](https://sylabs.io/guides/2.6/user-guide/) 
el cual puede crear imágenes que se ejecutan como sistemas independientes dentro de un host.

Antes de construir la imagen se necesita descargar una imagen base con centos 6, es 
importante que se use una imagen con centos 6 por motivos de compatibilidad con el host. 
Para descargar la imagen se ejecuta el comando.

```bash
$singularity pull --name centos6.img library://library/default/centos:6
```

Para poder crear esta imagen Singularity requiere un archivo de texto con las instrucciones 
para poder instalar todo lo necesario dentro del la imagen. El contenido de ese archivo 
es el siguiente.

<span style="color: #990819;">*Singularity*</span> 

```bash
Unresolved directive in nvgpu.adoc - include::example$sing_nvgpu_snmp.txt[]
```


### Instalación de NET-SNMP y nvgpu-smi-snmp

En la sección `%post` de el archivo `Singularity` le indicamos a singularity las acciones 
necesarias para la instalación de NET-SNMP y nvgpu-smi-snmp dentro de la imagen, y estas son.

1.  Instalar los paquetes `make gcc git perl-ExtUtils-Embed libxml2-devel` desde el 
    repositorio de centos6

2.  Descargar el codigo de NET-SNMP

3.  Compilar e instalar NET-SNMP

4.  Descargar el codigo de nvgpu-smi-snmp

5.  Compilar e instalar nvgpu-smi-snmp

Cada uno de estos puntos corresponde con una linea de la sección `%post`.

### Configuración de NET-SNMP

Debido a que el host ya tiene una instalación de NET-SNMP la instalación dentro del 
contenedor debe utilizar un puerto diferente y para lograr esto se debe modificar el 
archivo `snmpd.conf` que por default se encuentra en la ruta `/usr/local/etc/snmp/snmpd.conf`. 
En la sección `%files` del archivo `Singularity` se especifica que queremos copiar los 
archivos `snmpd.conf` y `snmp.conf` a la carpeta indicada dentro de la imagen. Es necesario 
tener estos archivos en la ruta desde la que se construya la imagen.
El archivo `snmpd.conf` es una copia del archivo que se encuentra en el host con algunos 
cambios, y esos cambios son.

1.  Agregar una línea con `agentAddress udp:10161` para indicarle a NET-SNMP que utilice 
    el puerto `10161` en lugar del puerto por default que es `161`. Esta configuración se 
    encuentra documentada en el manual de snmpd.conf en la pagina 5.

2.  Agregar la línea `dlmod nvCtrlTable /usr/local/lib/snmp/dlmod/nvgpu-snmp.so`. 
    Esta línea le indica a NET-SNMP que cargue el objeto compartido del modulo 
    nvgpu-smi-snmp cuando inicie el servicio.

El archivo `snmp.conf` es una copia del archivo de configuración por default con el mismo 
nombre. A este archivo solo se le agrego la línea `mibs +NV-CTRL-MIB` para indicar que 
queremos que se cargue el archivo mib relacionado con el modulo nvgpu-smi-snmp.


### Construccion de la imagen

Para construir la imagen se requiere contar con los archivos de configuración `snmpd.conf`
y `snmp.conf` en el directorio en el que se realizara la construcción de la imagen así como
una imagen de centos6, la cual se puede descargar como se indicó anteriormente.

Para la construcción de la imagen se ejecuta el comando

```bash
$singularity build snmpd_gpu Singularity
```

Este comando da como resultado una imagen de singularity con el nombre `snmpd_gpu`.


### Ejecución

Se requiere que el contenido de la sección `%startscript` del archivo `Singularity`
se ejecute como un servicio y para lograr esto singularity tiene una función especial,
para esto se ejecuta el comando

```bash
$singularity instance.start --nv snmpd_gpu snmpd_gpu
```

Este comando ejecuta la sección `%startscript` del archivo `Singularity`.
Es importante incluir la opción `--nv` ya que así es como le indicamos a singularity que
incluya los archivos del host relacionados con `nvidia-smi` en la ejecución.
De otra forma el modulo nvgpu-smi-snmp no tendrá forma de acceder a la información de las 
gpus y el proceso snmpd de la instancia se detendrá.

Para verificar que singularity esta ejecutando una instancia de nuestra imagen
se puede hacer uso del comando

```bash
$singularity instance.list
```

Esto mostrara una lista con todas las instancias que singularity tiene en ejecución.

Para detener la ejecución de la instancia podemos ejecutar

```bash
$singularity instance.stop snmpd_gpu
```

Esto detendrá la ejecución de la instancia con nombre `snmpd_gpu` que singularity
tenia en ejecución.


### Verificación

Para verificar que el modulo nvgpu-smi-snmp esta funcionando correctamente podemos ejecutar

```bash
snmpwalk -c tst -v2c localhost:10161 1.3.6.1.4.1.2021.13.42.2
```

Y si todo funciona correctamente se nos debe mostrar una salida con las métricas de las 
gpus conectadas en el host.
