# Paso a Paso: Git Clone en AWS EC2

**URL de tu repositorio:** https://github.com/Nram94/TEIS-DjangoSOLID

---

## 📋 ANTES DE CLONAR EN AWS - Haz ESTO en tu PC

### Paso 1: Verifica que todo esté listo localmente

En tu PowerShell (en la carpeta del proyecto):

```powershell
# Ver archivos sin guardar
git status
```

**Deberías ver:**
- ✅ Archivos modificados (`M`): settings.py, docker-compose.yml, urls.py, etc
- ✅ Archivos nuevos (`??`): TUTORIAL04_DOCKER_AWS.md, AWS_DEPLOYMENT_INSTRUCTIONS.md, etc

### Paso 2: Guardar todos los cambios en Git

```powershell
# Agregar TODOS los archivos (modificados y nuevos)
git add -A

# Ver cambios staged
git status

# Hacer commit
git commit -m "Tutorial 04 completado - Docker y AWS - CRISTIAN_CABARCAS"
```

### Paso 3: Enviar a GitHub

```powershell
# Push a tu repositorio
git push origin main

# Debería mostrar:
# To https://github.com/Nram94/TEIS-DjangoSOLID.git
# XX..XX main -> main
```

### Paso 4: Verifica en GitHub

Abre en navegador:
```
https://github.com/Nram94/TEIS-DjangoSOLID
```

**Debería ver:**
- ✅ Todos los archivos .md (TUTORIAL01, TUTORIAL02, TUTORIAL03, TUTORIAL04, etc)
- ✅ Archivos Dockerfile, docker-compose.yml
- ✅ Carpeta tienda_app con todo el código
- ✅ requirements.txt

---

## 🌐 EN AWS EC2 - Haz ESTO después

### Paso 5: En la terminal de AWS EC2

Cuando ya tengas acceso SSH a tu instancia EC2 (con `docker` y `git` instalados):

```bash
# 1. Clonar tu repositorio
git clone https://github.com/Nram94/TEIS-DjangoSOLID.git

# 2. Entrar a la carpeta
cd TEIS-DjangoSOLID

# 3. Verificar que están todos los archivos
ls -la

# Deberías ver:
# total XXX
# -rw-r--r--  1 ec2-user ... docker-compose.yml
# -rw-r--r--  1 ec2-user ... Dockerfile
# -rw-r--r--  1 ec2-user ... requirements.txt
# drwxr-xr-x  3 ec2-user ... tienda_app
# etc.
```

### Paso 6: Lanzar Docker en AWS

```bash
# Construir e iniciar contenedores
docker compose up -d --build

# Ver que están corriendo
docker ps

# Debería mostrar:
# CONTAINER ID  IMAGE  COMMAND  STATUS  PORTS
# xxxxxxxx      teis-djangosolid-web  ...  Up XX seconds  0.0.0.0:8000->8000/tcp
# xxxxxxxx      postgres:15  ...  Up XX seconds
```

### Paso 7: Verificar logs

```bash
# Ver logs del contenedor web
docker logs -f teis-djangosolid-web-1

# Debería mostrar:
# Watching for file changes with StatReloader
```

### Paso 8: Probar desde tu PC

Abre navegador en tu PC (NO en EC2):

```
http://100.31.109.121:8000/api/v1/comprar/
```

**Deberías ver:**
- ✅ Interfaz DRF
- ✅ Endpoint POST disponible
- ✅ Opción para hacer request

---

## 🐛 TROUBLESHOOTING

### Si `git clone` falla:

```bash
# Error: "Repository not found" o "access denied"
# Solución: Verifica que hiciste push en tu PC primero

# Vuelve a tu PC y haz:
git push origin main

# Luego vuelve a AWS e intenta:
git clone https://github.com/Nram94/TEIS-DjangoSOLID.git
```

### Si `docker compose up` falla:

```bash
# Error: "command not found: docker"
# Ya debería estar instalado en AWS, pero si no:
sudo dnf install docker -y
sudo service docker start

# Error: "permission denied"
sudo usermod -a -G docker ec2-user
# Luego: exit y reconecta a la instancia
```

### Si la API no responde:

```bash
# Espera 30-60 segundos (Docker tarda en iniciar)
# Luego intenta acceder a:
http://100.31.109.121:8000/api/v1/comprar/

# Si aún falla, revisa logs:
docker logs teis-djangosolid-web-1 | tail -20
```

---

## ✅ CHECKLIST FINAL

### En tu PC (antes de AWS):
- [ ] `git add -A` ejecutado
- [ ] `git commit -m "..."` realizado
- [ ] `git push origin main` completado
- [ ] Verificas en GitHub que están TODOS los archivos

### En AWS EC2:
- [ ] Docker instalado (`docker ps` funciona)
- [ ] Git instalado (`git --version` funciona)
- [ ] Username/Password o SSH key configurado
- [ ] `git clone` completado sin errores
- [ ] `docker ps` muestra 2 contenedores corriendo
- [ ] `http://100.31.109.121:8000/api/v1/comprar/` accesible

---

## 📸 Screenshot Final

Cuando todo esté corriendo en AWS, captura screenshot de:

```
http://100.31.109.121:8000/api/v1/comprar/
```

Mostrando:
- URL en navegador
- Interfaz DRF con endpoint POST
- Opción para hacer request
- Response: 201 Created con JSON

---

**¿LISTO PARA CLONAR EN AWS?** 🚀

1. Primero haz `git push origin main` en tu PC
2. Luego en AWS: `git clone https://github.com/Nram94/TEIS-DjangoSOLID.git`
3. Y `docker compose up -d --build`

¡Eso es todo!
