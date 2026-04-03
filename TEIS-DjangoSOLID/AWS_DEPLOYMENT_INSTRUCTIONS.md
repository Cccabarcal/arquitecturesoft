# AWS Deployment - Instructions for Professor

**Student:** CRISTIAN_CABARCAS  
**AWS Public IP:** 100.31.109.121  
**Date:** April 3, 2026

---

## 🌐 Access the API in AWS

### Correct URL (as per requirements):
```
http://100.31.109.121:8000/api/v1/comprar/
```

### For Screenshot Validation:
Open this URL in your browser and you should see the DRF Browsable API interface showing:
- **POST** endpoint available
- Request/Response format
- JSON response with `{"estado":"exito", "mensaje":"Orden creada..."}`

---

## 📋 Deployment Steps Completed

### ✅ Local Development (Already Done)
- [x] `settings.py` configured with environment variables
- [x] `requirements.txt` generated with all dependencies
- [x] `Dockerfile` created and optimized
- [x] `docker-compose.yml` configured for local testing
- [x] API tested locally on `http://localhost:8000/api/v1/comprar/`

### ✅ AWS EC2 Deployment (Ready to Execute)

**Prerequisites:**
- AWS Academy account active
- EC2 instance launched (t2.micro, Amazon Linux 2023)
- Security Group configured to allow port 8000

**Installation Steps (run in EC2 terminal):**

```bash
# 1. Update system
sudo dnf update -y

# 2. Install Git and Docker
sudo dnf install git docker -y

# 3. Start Docker service
sudo service docker start

# 4. Add user permissions (run this, then exit and reconnect)
sudo usermod -a -G docker ec2-user
exit

# 5. Reconnect to EC2 Instance Connect

# 6. Clone repository
git clone https://github.com/YOUR_GITHUB_USERNAME/TEIS-DjangoSOLID.git
cd TEIS-DjangoSOLID

# 7. Start Docker containers
docker compose up -d --build

# 8. Verify running
docker ps
```

**Security Group Configuration:**
1. Go to EC2 → Instances
2. Select your instance → Security tab
3. Edit Inbound Rules → Add Rule
4. Type: **Custom TCP**
5. Port: **8000**
6. Source: **0.0.0.0/0** (Anywhere)
7. Save

---

## 🧪 Testing the API

### Local Test (Before Deployment):
```bash
curl -X POST http://localhost:8000/api/v1/comprar/ \
  -H "Content-Type: application/json" \
  -d '{"libro_id": 1, "cantidad": 1, "direccion_envio": "Testing"}'

# Expected Response: 201 Created
# {"estado":"exito","mensaje":"Orden creada. Total: 178.5"}
```

### AWS Test (After Deployment):
Access in browser:
```
http://100.31.109.121:8000/api/v1/comprar/
```

Or via curl from EC2 terminal:
```bash
curl -X POST http://localhost:8000/api/v1/comprar/ \
  -H "Content-Type: application/json" \
  -d '{"libro_id": 1, "cantidad": 1, "direccion_envio": "AWS"}'
```

---

## 📸 Screenshot Requirements

For validation, capture a screenshot showing:

1. **Browser URL Bar:** `http://100.31.109.121:8000/api/v1/comprar/`
2. **DRF Interface** showing:
   - Endpoint name: "Compra API View"
   - HTTP method options (GET, POST, etc.)
   - JSON response section
3. **Response body:** 
   ```json
   {
     "estado": "exito",
     "mensaje": "Orden creada. Total: 178.5"
   }
   ```

---

## 📁 Project Structure (as Deployed)

```
/home/ec2-user/TEIS-DjangoSOLID/
├── docker-compose.yml          ← Orchestration config
├── Dockerfile                  ← Image recipe
├── requirements.txt            ← Dependencies
├── manage.py                   ← Django CLI
├── Tienda/                     ← Main Django project
│   ├── settings.py            ← Environment-based config
│   └── urls.py                ← Routes (no /app/ prefix)
├── tienda_app/                 ← Main application
│   ├── views.py               ← 3 implementations + API view
│   ├── services.py            ← Business logic (CompraService)
│   ├── domain/                ← Domain layer
│   ├── infra/                 ← Infrastructure layer
│   └── api/                   ← REST API endpoints
└── TUTORIAL04_DOCKER_AWS.md   ← This documentation
```

---

## 🔧 Docker Commands (in EC2)

Monitor your application:
```bash
# See running containers
docker ps

# View logs in real-time
docker logs -f <container-id>

# Stop all containers
docker compose down

# Rebuild and restart
docker compose up -d --build
```

---

## ⚙️ Environment Variables (as configured)

The application reads these variables from `docker-compose.yml`:

```
DB_NAME=tienda_db
DB_USER=postgres
DB_PASSWORD=secret_password
DB_HOST=db              # Docker service hostname
DB_PORT=5432
```

When running in AWS with RDS, you would adjust:
```
DB_HOST=your-rds-endpoint.amazonaws.com
DB_PASSWORD=YourSecurePassword
```

---

## ✅ Validation Checklist

- [ ] EC2 instance is running (t2.micro)
- [ ] Security Group allows inbound traffic on port 8000
- [ ] Docker is installed on EC2
- [ ] Repository cloned to EC2
- [ ] `docker compose up -d --build` executed successfully
- [ ] `docker ps` shows 2 containers (web + db)
- [ ] Can access `http://100.31.109.121:8000/api/v1/comprar/` in browser
- [ ] API returns 201 Created with JSON response
- [ ] Screenshot captured showing the working API

---

## 🎓 Pedagogical Goals Achieved

This deployment demonstrates:

1. **Configuration Management:** Environment-based settings
2. **Containerization:** Docker for reproducible deployments
3. **Orchestration:** Docker Compose for multi-service apps
4. **Cloud Deployment:** AWS EC2 instance setup
5. **Infrastructure as Code:** Dockerfile + docker-compose as IaC
6. **Security:** Security Groups for network isolation
7. **DevOps:** CI/CD pipeline ready (Git → EC2 → Docker)

---

**Ready to submit to Professor!** ✅
