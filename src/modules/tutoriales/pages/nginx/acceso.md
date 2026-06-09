# Control de acceso a la base de conocimientos

Configuración del control de acceso a la base de conocimientos usando Nginx y http 
basic autentication. 
[Tutorial](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)

## Gestión de usuarios

Para la gestión de los usuarios con acceso a la base de conocimientos se hace uso del 
comando htpasswd que se encuentra en el paquete httpd-tools en CentOS 7.

La gestion de usuarios se realiza desde el host del contenedor de nginx que se quiere 
configurar.

### Crear archivo de usuarios

Se requiere crear el archivo **.htpasswd_kb** con un usuario. Esto se consigue con el 
siguiente comando.

```bash
htpasswd -c .htpasswd_kb nombre_de_usuario
```

Esto solicitara el password para el usuario y creara el archivo.

### Crear usuarios

Para crear un usuario nuevo se ejecuta

```bash
htpasswd .htpasswd_kb nuevo_usuario
```

Después solicitara el password para el nuevo usuario.

### Cambiar password

Para cambiar el password a un usuario existente se usa el mismo comando que se usa 
para crearlo.

### Borrar usuarios

Para borrar un usuario se ejecuta el comando

```bash
htpasswd -D .htpasswd_kb nombre_de_usuario
```

## Configuración de Nginx

Nginx cuenta con un modulo para control de acceso básico a ubicaciones dentro de un 
servidor de nginx. Para usar este modulo dentro de la base de conocimientos es 
necesario hacer lo siguiente:

1.  Montar el archivo de usuarios (**.htpasswd_kb**) dentro del contenedor de nginx en 
    el directorio **/etc/apache2**.

2.  Habilitar la gestión básica de control de usuarios en el archivo de configuración de 
    Nginx (/etc/nginx/default.conf) para la ubicación deseada

    ```bash
    location /kb/{
        ...
        auth_basic "Colaboradores";
        auth_basic_user_file /etc/apache2/.htpasswd_kb;
        ...
    }
    ```
