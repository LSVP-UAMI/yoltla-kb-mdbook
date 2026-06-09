# Generar certificados para HTTPS

## Certbot

**Certbot** es una herramienta para generar certificados de forma cencilla. 
**Certbot** usa al proveedor de certificados **Letsencrypt**

La instalación de certbot se realizo dentro de un contenedor usando la imagen oficial 
de docker ([Imagen](https://hub.docker.com/r/certbot/certbot/)).

### Docker compose

Para crear un contenedor de **Certbot** en docker compose se agrega lo siguiente al 
archivo *docker-compose.yml*

```yaml
...
services:
...
  yoltla_certbot:
  image: certbot/certbot:v1.32.0
  container_name: yoltla_certbot
  volumes:
   - ./volumes/certbot/www/certbot:/var/www/certbot
   - ./volumes/certbot/etc/letsencrypt:/etc/letsencrypt
...
```

Es necesario montar los volumenes para */var/www/certbot* y */etc/letsencrypt* ya que la
información que se encuentra en estos directorios debe ser compartida con el contenedor
de **Nginx**

Para montar los directorios */var/www/certbot* y */etc/letsencrypt* de **Certbot** en el
contenedor de **Nginx** es necesario agregar los volumenes correspondientes en el archivo
*docker-compose.yml*

```yaml
...
services:
  yoltla_rproxy:
  ...
    volumes:
    ...
      - ./volumes/certbot/www/certbot:/var/www/certbot
      - ./volumes/certbot/etc/letsencrypt:/etc/nginx/ssl
...
```

### Configuración de **Nginx**

Para que **Letsencrypt** pueda verificar la propiedad del dominio para el que se solicita el
certificado es necesario agregar la siguiente configuración para **Nginx** dentro del archivo
*/etc/nginx/conf.d/default.conf*

```bash
...
server {
    listen      443 ssl;
    ...
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    ...
}
...
```

### Generar certificados

Para que **Certbot** pueda generar los certificados es necesario que **Nginx** este en 
ejecución con las configuraciones previamente mencionadas.

Antes de generar los certificados es conveniente probar que todo este configurado de una 
forma adecuada para esto podemos usar el comando

```bash
docker-compose run --rm  yoltla_certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d supercomputo.izt.uam.mx
```

Si todo esta bien entonces se pueden generar los certificados con

```bash
docker-compose run --rm  yoltla_certbot certonly --webroot --webroot-path /var/www/certbot/ -d supercomputo.izt.uam.mx
```

### Configurar los certificados en **Nginx**

Una vez generados los certificados es necesario indicarle a **Nginx** donde se encuentran,
esto se logra de la siguiente forma.

```bash
...
server {
    listen      443 ssl;
    ...
    ssl_certificate /etc/nginx/ssl/live/supercomputo.izt.uam.mx/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl//live/supercomputo.izt.uam.mx/privkey.pem;
    ...
}
...
```

### Renovar los certificados

Para renovar los certificados se ejecuta el comando

```bash
docker-compose run --rm  yoltla_certbot renew
```
