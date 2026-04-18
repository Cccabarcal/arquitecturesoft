# Strangler Pattern - Django + Flask + Nginx

## Descripción de la Arquitectura

Este proyecto implementa el patrón **Strangler Pattern** para migrar gradualmente de un monolito Django a una arquitectura de microservicios con Flask.

### Componentes

```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       ▼
┌──────────────────── NGINX (API Gateway) ────────────────┐
│                                                           │
│  /api/v1/*        →  Django (Monolito v1)               │
│  /api/v2/comprar  →  Flask (Microservicio v2)           │
└──────────────────────────────────────────────────────────┘
       │                        │
       ▼                        ▼
   Django v1                Flask v2
   (Puerto 8000)           (Puerto 5000)
```

### Servicios

- **web_django**: Monolito original en Django (puerto 8000 interno)
- **pagos_flask**: Microservicio Flask para pagos (puerto 5000 interno)
- **nginx**: API Gateway que rutea las solicitudes (puerto 80 público)
- **db**: Base de datos PostgreSQL (puerto 5432)

## Ejecución Local

### Requisitos

- Docker
- Docker Compose

### Pasos

1. **Construir y ejecutar los contenedores:**

```bash
docker compose up -d --build
```

2. **Verificar que los servicios están activos:**

```bash
docker compose ps
```

Deberías ver algo como:
```
NAME              COMMAND                  SERVICE      STATUS
web_django        gunicorn Tienda.wsgi...  web_django   Up
pagos_flask       gunicorn app:app...      pagos_flask  Up
nginx             nginx -g daemon off...   nginx        Up
db                postgres                 db           Up
```

3. **Ver logs de un servicio específico:**

```bash
# Logs de Nginx
docker compose logs nginx

# Logs de Flask
docker compose logs pagos_flask

# Logs de Django
docker compose logs web_django

# Todos los logs
docker compose logs -f
```

## Pruebas

### Herramientas necesarias

Usa **Postman**, **cURL**, o **VS Code REST Client** para hacer las pruebas.

### Test 1: Ruta v1 (Django - Monolito)

**GET** http://localhost/api/v1/

Respuesta esperada: Viene de Django (verifica en los logs)

```bash
curl -X GET http://localhost/api/v1/
```

Si ves errores de conexión, es porque el endpoint específico no existe. Lo importante es que la solicitud se rutea a Django.

### Test 2: Ruta v2 (Flask - Microservicio)

**POST** http://localhost/api/v2/comprar

```bash
curl -X POST http://localhost/api/v2/comprar \
  -H "Content-Type: application/json" \
  -d '{
    "producto_id": 1,
    "cantidad": 5,
    "usuario_id": 10
  }'
```

Respuesta esperada:
```json
{
  "estado": "procesada exitosamente por el Microservicio Flask",
  "timestamp": "2024-01-15T10:30:00.000000",
  "datos_recibidos": { ... },
  "servicio": "Flask Microservicio Pagos (v2)"
}
```

### Test 3: Verificar ruteo en Nginx

```bash
docker compose logs nginx
```

Deberías ver líneas como:
```
127.0.0.1 - - [15/Jan/2024:10:30:00 +0000] "GET /api/v1/ HTTP/1.1" 502 ...
127.0.0.1 - - [15/Jan/2024:10:30:05 +0000] "POST /api/v2/comprar HTTP/1.1" 200 ...
```

## Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `docker-compose.yml` | Orquestación de contenedores |
| `Dockerfile` | Imagen Docker para Django |
| `microservicio_pagos/Dockerfile` | Imagen Docker para Flask |
| `microservicio_pagos/app.py` | Aplicación Flask |
| `nginx/nginx.conf` | Configuración del API Gateway |

## Mejoras Futuras

1. **Autenticación**: Integrar JWT en Nginx
2. **Rate Limiting**: Limitar solicitudes por cliente
3. **Circuit Breaker**: Manejar fallos de servicios
4. **Logging centralizado**: ELK Stack o CloudWatch
5. **Monitoring**: Prometheus + Grafana

## Detener los Servicios

```bash
docker compose down
```

Para eliminar volúmenes (base de datos incluida):
```bash
docker compose down -v
```

## Troubleshooting

### El puerto 80 ya está en uso

```bash
# Cambiar puerto en docker-compose.yml:
# Cambiar "80:80" a "8080:80"
# Luego acceder a http://localhost:8080
```

### Flask no conecta con Nginx

```bash
# Verificar que el nombre de servicio es correcto en nginx.conf
# Debe ser "pagos_flask" (el nombre en docker-compose.yml)

# Reconstruir imágenes
docker compose down
docker compose up -d --build
```

### Base de datos no se crea

```bash
# Eliminar volúmenes y recrear
docker compose down -v
docker compose up -d
```

## Referencia de Comandos Útiles

```bash
# Ejecutar comando en un contenedor
docker compose exec web_django python manage.py migrate

# Ver variables de entorno
docker compose exec web_django env

# Entrar al contenedor (shell)
docker compose exec pagos_flask sh

# Reiniciar un servicio
docker compose restart nginx

# Reconstruir solo una imagen
docker compose build --no-cache web_django
```
