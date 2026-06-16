# NGINX


## Descripción

NGINX es un un servidor HTTP/proxy inverso, un servidor proxy de correo y un servidor 
proxy TCP/UDP genérico.

Para obtener más información, consulte la documentación oficial de [NGINX](https://nginx.org/en/docs/).


## Instalación

Para obtener una guía detallada de la instalación de NGINX, consulte la sección 
[Installing nginx](https://nginx.org/en/docs/install.html) de la documentación oficial 
de NGINX. De forma alternativa puede utilizar un [contenedor de Docker](https://hub.docker.com/_/nginx).

## Archivos de configuración

El comportamiento de NGINX y sus módulos es descrito en sus archivos de configuración. 
El archivo de configuración principal de NGINX, llamado *nginx.conf*, se ubica en el 
directorio */etc/nginx*:

<span style="color: #990819;">/etc/nginx/nginx.conf</span> 

```bash
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

El resto de archivos de configuración de NGINX se encuentran en el directorio 
*/etc/nginx/conf.d/*. Por defecto, en este directorio solo existe el archivo 
*default.conf*:

<span style="color: #990819;">*default.conf*</span> 

```bash

server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
```

```admonish important title=" "
Todas las configuraciones mostradas en las siguientes secciones deben realizarse en el 
archivo *default.conf*, a menos que se indique lo contrario.
```


## Reverse Proxy

Configuración de NGINX como un proxy inverso para HTTP.

Para obtener más información, consulta la sección [NGINX Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) 
de la documentación oficial de NGINX.

### Passing a Request to a Proxied Server

Para pasar una solicitud a un servidor proxy HTTP, la directiva `proxy_pass` se 
especifica  dentro de una ubicación (*location*). Por ejemplo:

```bash
    location /some/path/ {
        proxy_pass http://www.example.com/;
    }
```

Esta configuración de ejemplo pasa todas las solicitudes procesadas en la ubicación 
`/some/path/` al servidor proxy de la dirección `http://www.example.com/`. Esta dirección 
se puede especificar como un nombre de dominio o una dirección IP. La dirección también 
puede incluir un puerto:

```bash
    location / {
        proxy_pass http://148.206.50.80:3035/;
    }
```

### Passing Request Headers

De forma predeterminada, NGINX redefine el campo de encabezado `Host` utilizando la variable 
`$proxy_host`. Para cambiar esta configuración, así como modificar otros campos de encabezado, 
usa la directiva `proxy_set_header`. Por ejemplo:

```bash
    location /kb/ {
        proxy_pass http://148.206.50.80:3036/;
        proxy_set_header Host $http_host/kb;
        proxy_set_header X-Real-IP $remote_addr;
    }
```

Para obtener más información de la directiva `proxy_set_header`, consulta la sección 
[proxy_set_header](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header) 
de la documentación oficial de NGINX.

## Upstream

La directiva `upstream` permite definir grupos de servidores. Esta directiva debe 
colocarse dentro de un bloque `http`.

Los servidores de un grupo son configurados utilizando la directiva `server`. Por ejemplo, 
la siguiente configuración define un grupo llamado `supercomputo` con un servidor:

```bash
upstream supercomputo {
    server 148.206.50.80:3035;
}
```    

Para pasar solicitudes a un grupo de servidores, el nombre del grupo debe ser especificado 
en la directiva `proxy_pass`:

```bash
    location / {
        proxy_pass http://supercomputo/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
    }
```    

Para obtener más información, consulta la sección 
[Proxying HTTP Traffic to a Group of Servers](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/#proxying-http-traffic-to-a-group-of-servers) 
de la documentación oficial de NGINX.


## HTTPS


### Certificados SSL

Para configurar un servidor HTTPS, verifica que el servidor está escuchando en el 
puerto 443, e incluya el parámetro `ssl` en directiva `listen`:

```bash
server {
    listen      443 ssl;
    server_name supercomputo.izt.uam.mx;

    ...
}
```

Después especifica las ubicaciones del certificado del servidor y los archivos de 
clave privada:

```bash
server {
    listen      443 ssl;
    server_name supercomputo.izt.uam.mx;

    ssl_certificate /etc/nginx/ssl/live/supercomputo.izt.uam.mx/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl//live/supercomputo.izt.uam.mx/privkey.pem;

    ...
}
```

Para obtener más información, consulta la sección 
[Setting up an HTTPS Server](https://docs.nginx.com/nginx/admin-guide/security-controls/terminating-ssl-http/#setting-up-an-https-server) 
de la documentación oficial de NGINX.

### HTTP to HTTPS Redirect

Para redirigir el tráfico HTTP a HTTPS, cree un nuevo bloque `server`, y agregue la 
siguiente información:

```bash
server {
    listen 80;
    server_name supercomputo.izt.uam.mx;

    return 301 https://$host$request_uri;
}
```

Para obtener más información, consulta el siguiente [sitio](https://linuxhint.com/nginx-redirect-http-https/).
