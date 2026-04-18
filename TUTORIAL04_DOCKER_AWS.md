# Tutorial 04: Dockerización y Deploy en AWS EC2

**Objetivo:** Elevar la arquitectura del Tutorial 03 (API REST) empaquetándola en Docker y desplegándola en AWS EC2.

**Autores:** CRISTIAN_CABARCAS  
**Tecnologías:** Django 5.2, PostgreSQL 15, Docker, AWS EC2  
**Patrón Arquitectónico:** Containerización + Infraestructura en la Nube

---

## 1. Refactorización de Configuración: Environment Variables

### 1.1 Modificar `settings.py`

El archivo ya está actualizado para usar variables de entorno:

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key-dev')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'tienda_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'secret_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

**Beneficio:** La misma imagen Docker funciona en:
- 💻 Laptop local (con `localhost`)
- 🐳 Docker Compose (con `db` como hostname)
- ☁️ AWS EC2 (con IP o nombre del RDS)

### 1.2 Requirements.txt

```bash
$ pip freeze > requirements.txt
```

**Contenido verificado:**
```
asgiref==3.11.1
Django==5.2.12
djangorestframework==3.17.1
psycopg2-binary==2.9.11
sqlparse==0.5.5
```

---

## 2. Dockerfile: La Receta de la Imagen

El archivo `Dockerfile` ya existe y está optimizado:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

**Optimizaciones:**
- ✅ `python:3.11-slim` → Base ligera (~160MB)
- ✅ `--no-cache-dir` → Reduce tamaño de imagen
- ✅ `postgresql-client` → Para conectar a DB remota
- ✅ `0.0.0.0:8000` → Escucha desde cualquier interfaz

---

## 3. Docker Compose Local

El archivo `docker-compose.yml` está configurado correctamente:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=tienda_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=secret_password

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_NAME=tienda_db
      - DB_USER=postgres
      - DB_PASSWORD=secret_password
      - DB_HOST=db
      - DEBUG=True

volumes:
  postgres_data:
```

### Prueba Local:
```bash
docker-compose up --build
```

Accede a: `http://localhost:8000/app/api/v1/comprar/`

---

## 4. Despliegue en AWS Academy

### 4.1 Lanzamiento de Instancia EC2

1. Ingresa a **AWS Academy** → Lanza el laboratorio
2. Consola AWS → **EC2** → **Launch Instances**
3. **Name:** `Servidor-Django`
4. **AMI:** Amazon Linux 2023 (Free tier)
5. **Instance Type:** `t2.micro`
6. **Key Pair:** `vockey`
7. **Security Group:** 
   - ✅ Allow SSH (port 22)
   - ✅ Allow HTTP (port 80)
   - ✅ Allow HTTPS (port 443)
   - ✅ Allow Custom TCP 8000
8. **Launch**

### 4.2 Conexión SSH

1. En la consola de EC2, selecciona tu instancia
2. Clic en **Connect**
3. Usa **EC2 Instance Connect** (terminal en navegador)

### 4.3 Instalación de Software

En la terminal de AWS EC2:

```bash
# Actualizar sistema
sudo dnf update -y

# Instalar Git y Docker
sudo dnf install git docker -y

# Iniciar Docker
sudo service docker start

# Dar permisos al usuario
sudo usermod -a -G docker ec2-user

# IMPORTANTE: Cierra terminal y reconéctate para aplicar permisos
exit
```

Reconéctate a la instancia.

### 4.4 Clonar y Desplegar

```bash
# 1. Clonar repositorio (reemplaza con tu URL)
git clone https://github.com/TU_USUARIO/TEIS-DjangoSOLID.git

# 2. Entrar a la carpeta
cd TEIS-DjangoSOLID

# 3. Lanzar contenedores con Docker Compose
docker compose up -d --build

# 4. Verificar que está corriendo
docker ps
docker logs <container-id>
```

### 4.5 Abrir Puerto 8000 en Security Group

1. EC2 → **Instances** → Selecciona tu instancia
2. **Security** → Haz clic en el Security Group
3. **Edit Inbound Rules** → **Add Rule**
4. **Type:** Custom TCP
5. **Port Range:** 8000
6. **Source:** 0.0.0.0/0 (Anywhere)
7. **Save Rules**

### 4.6 Acceder a la Aplicación en AWS

Obtén la **IP pública** de tu instancia y accede:

```
http://<EC2-PUBLIC-IP>:8000/app/api/v1/comprar/
```

---

## 5. Verificación y Pruebas

### Test en AWS:

```bash
# Dentro de EC2
curl -X POST http://localhost:8000/app/api/v1/comprar/ \
  -H "Content-Type: application/json" \
  -d '{"libro_id": 1, "cantidad": 2, "direccion_envio": "AWS Test"}'

# Esperado: 201 Created + JSON response
```

### Ver logs:

```bash
docker logs <container-id> -f
```

---

## 6. Consideraciones para Producción

| Aspecto | Local | AWS |
|--------|-------|-----|
| **DEBUG** | True | False |
| **ALLOWED_HOSTS** | localhost | EC2-PUBLIC-IP |
| **SECRET_KEY** | Hardcoded | Variables de entorno |
| **Database** | PostgreSQL local | RDS o PostgreSQL en EC2 |
| **Static Files** | Django serve | S3 + CloudFront |

### Archivo `.env` para AWS:

```bash
DEBUG=False
ALLOWED_HOSTS=ec2-xy-xy-xy-xy.compute.amazonaws.com
SECRET_KEY=tu-clave-segura-muy-luerte
DB_NAME=tienda_aws
DB_USER=admin
DB_PASSWORD=SuperSe€ura123!
DB_HOST=database.cxyz123.us-east-1.rds.amazonaws.com
```

---

## 7. Resumen Arquitectónico

```
┌─────────────────────────────────────────┐
│         Desarrollo Local (Laptop)       │
│  docker-compose up (Django + PostgreSQL)│
└─────────────────────────────────────────┘
                    ↓
                    │ Git push
                    ↓
┌─────────────────────────────────────────┐
│        AWS EC2 Instance (t2.micro)      │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │  Docker Container                │   │
│  │  ┌────────────────────────────┐  │   │
│  │  │  Django REST API           │  │   │
│  │  │  (CompraService)           │  │   │
│  │  └────────────────────────────┘  │   │
│  │         ↓                        │   │
│  │  ┌────────────────────────────┐  │   │
│  │  │  PostgreSQL 15             │  │   │
│  │  │  (tienda_db)               │  │   │
│  │  └────────────────────────────┘  │   │
│  └──────────────────────────────────┘   │
│                                         │
│  Acceso: http://PUBLIC-IP:8000/app/... │
└─────────────────────────────────────────┘
```

---

## 8. Checklist Final

- [ ] `settings.py` usa variables de entorno
- [ ] `requirements.txt` está actualizado
- [ ] `Dockerfile` está optimizado
- [ ] `docker-compose.yml` funciona localmente
- [ ] Instancia EC2 creada con Security Group correcto
- [ ] Docker instalado en EC2
- [ ] Código clonado en EC2
- [ ] `docker compose up -d` ejecutado en AWS
- [ ] Puerto 8000 abierto en Security Group
- [ ] API accesible vía `http://PUBLIC-IP:8000/app/api/v1/comprar/`

---

## 9. Troubleshooting

| Problema | Solución |
|----------|----------|
| **Error: "db" host not found | Asegurate que `DB_HOST=db` en docker-compose |
| **Puerto 8000 no responde | Verifica Security Group inbound rules |
| **Connection refused en EC2 | Espera 2-3 min, Docker puede estar iniciando |
| **psycopg2 error | Incluye `postgresql-client` en Dockerfile |

---

**Conclusión:** Has completado tu arquitectura Django SOLID desde el código hasta la nube. ¡Felicidades! 🚀
