# Tutorial 06: El Primer Estrangulamiento
## Migrando el Servicio de Compras de Django a Flask (v2)

### Estado de Implementación ✅

Se ha completado la implementación del **Strangler Pattern** en tu arquitectura. El sistema ahora consta de:

1. **Django (v1)** - Monolito Original
2. **Flask (v2)** - Microservicio de Pagos (Estrangulador)
3. **Nginx** - Orquestador de Ruteo

---

## Estructura de Carpetas Creadas

```
TEIS-DjangoSOLID/
├── microservicio_pagos/          ← NUEVA CARPETA
│   ├── app.py                   ← Flask app principal
│   ├── Dockerfile               ← Contenedor para Flask
│   └── requirements.txt          ← Dependencias de Flask
├── docker-compose.yml            ← ACTUALIZADO (agregado pagos_flask)
└── nginx/
    └── nginx.conf                ← ACTUALIZADO (ruteo v1/v2)
```

---

## Cambios Realizados

### 1. Microservicio Flask (`microservicio_pagos/app.py`)
- Endpoint: `POST /api/v2/comprar`
- Recibe: `{producto_id, cantidad}`
- Responde: JSON con confirmación de compra exitosa

### 2. Dockerfile para Flask (`microservicio_pagos/Dockerfile`)
- Base: `python:3.11-alpine`
- Puerto: `5000`
- Servidor: `gunicorn`

### 3. Docker Compose Actualizado
- **Servicio antiguo**: `web_django` (Django + Gunicorn en puerto 8000)
- **Servicio nuevo**: `pagos_flask` (Flask en puerto 5000)
- **Orquestador**: `nginx` (puerto 80)

### 4. Nginx Actualizado (`nginx/nginx.conf`)
```nginx
# Ruteo del Strangler Pattern
GET  /api/v1/*    → django_v1:8000   (Django - Ruta vieja)
POST /api/v2/comprar → flask_v2:5000 (Flask - Estrangulador)
*    /             → django_v1:8000   (Todo lo demás)
```

---

## 📋 Pasos para Desplegar Localmente

### Paso 1: Construir e Iniciar los Contenedores
```bash
cd d:\Users\Cristian\Documents\Visual Projects\arquitecturesoft\TEIS-DjangoSOLID
docker compose up -d --build
```

### Paso 2: Verificar que los Servicios están Corriendo
```bash
docker compose ps
# Debe mostrar: db, web_django, pagos_flask y nginx con estado UP
```

### Paso 3: Ver los Logs de Orquestación
```bash
docker compose logs nginx
# Verás el redireccionamiento de peticiones
```

---

## 🧪 Pruebas Requeridas para la Evaluación

### Prueba 1: Coexistencia (v1 - Django)
Hacer un GET a la API vieja de Django:
```bash
curl http://localhost/api/v1/productos/
# O en Postman: GET http://localhost/api/v1/productos/
```
**Respuesta esperada**: JSON listando productos (desde Django)

### Prueba 2: Estrangulamiento (v2 - Flask)
Hacer un POST al nuevo endpoint de Flask:
```bash
curl -X POST http://localhost/api/v2/comprar \
  -H "Content-Type: application/json" \
  -d '{"producto_id": 123, "cantidad": 5}'
```

**JSON de respuesta esperado**:
```json
{
  "mensaje": "Compra procesada exitosamente por el Microservicio Flask (v2)",
  "producto_id": 123,
  "cantidad": 5,
  "status": "Aprobado"
}
```

### Prueba 3: Logs de Nginx
```bash
docker compose logs nginx
```
Debe mostrar peticiones HTTP siendo redirigidas a `web_django` y `pagos_flask`.

---

## 🚀 Despliegue en AWS

### Paso 1: Push a Git
```bash
git add .
git commit -m "Tutorial 06: Implementar Strangler Pattern con Flask"
git push origin main
```

### Paso 2: En tu instancia EC2
```bash
ssh -i tu_llave.pem ubuntu@tu-ip-e-c-2.compute.amazonaws.com
cd ~/tu-proyecto
git pull origin main
docker compose up -d --build
```

### Paso 3: Verificar Despliegue
```bash
curl http://tu-ip-ec2.compute.amazonaws.com/api/v2/comprar -X POST \
  -H "Content-Type: application/json" \
  -d '{"producto_id": 1, "cantidad": 2}'
```

---

## 📊 Arquitectura Post-Implementación

```
┌─────────────────────────────────────────────────────────────┐
│                      NGINX (Puerto 80)                      │
│                    Proxy Inverso / Router                   │
└────────┬──────────────────────────────────────┬─────────────┘
         │                                      │
    GET  /api/v1/*                         POST /api/v2/comprar
         │                                      │
    ┌────▼─────────────┐               ┌────────▼──────┐
    │ Django + Gunicorn│               │ Flask Payments │
    │   (Puerto 8000)  │               │ (Puerto 5000)  │
    │  ← MONOLITO ←    │               │ ← STRANGLER ←  │
    └────┬─────────────┘               └────────┬──────┘
         │                                      │
    ┌────▼──────────────────────────────────────┘
    │
┌───▼──────────────┐
│  PostgreSQL (db) │
│   (Puerto 5432)  │
└──────────────────┘
```

---

## 🔄 Próximos Pasos (Futuro)

Gradualmente, más funcionalidades serán "estranguladas":
- `/api/v2/inventario` → Flask
- `/api/v2/usuarios` → Flask
- Event-driven payments → Kafka/RabbitMQ

Eventualmente, Django se convertirá en un legacy service mínimo, y Flask/Microservicios dominarán la arquitectura.

---

## ✅ Checklist para Aprobación

- [ ] Carpeta `microservicio_pagos/` creada con `app.py`, `Dockerfile`, `requirements.txt`
- [ ] `docker-compose.yml` actualizado con servicio `pagos_flask`
- [ ] `nginx/nginx.conf` actualizado con ruteo de `/api/v2/comprar` hacia Flask
- [ ] Captura de screenshot: GET `/api/v1/productos/` responde desde Django
- [ ] Captura de screenshot: POST `/api/v2/comprar` responde desde Flask
- [ ] Captura de screenshot: `docker compose logs nginx` mostrando redireccionamiento
- [ ] Documento PDF con pruebas entregado

---

**Salsa Arquitectónica**: 🌶️
El Strangler Pattern es como un "constructor de nuevos órganos" en una criatura viva.
Mientras el monolito sigue funcionando, gradualmente extrae funcionalidades hacia microservicios.
¡El patrón es invisible para el usuario final!

---

*Tutorial 06 - Arquitectura de Software 2026*
