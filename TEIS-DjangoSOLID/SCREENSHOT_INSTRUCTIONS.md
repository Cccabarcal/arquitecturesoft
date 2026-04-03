# Screenshot Instructions for AWS Deployment

**Goal:** Capture proof that the API is running on AWS EC2

---

## 📸 Steps to Capture Screenshot

### Step 1: Open Browser
Navigate to:
```
http://100.31.109.121:8000/api/v1/comprar/
```

### Step 2: You Should See
The **Django REST Framework Browsable API** interface showing:

```
┌─────────────────────────────────────────────────────┐
│ Compra API                                          │
│ Endpoint para procesar compras via JSON.            │
│ POST /api/v1/comprar/                              │
│                                                     │
│ Payload: {"libro_id": 1, ...}                      │
│ Allow: POST, OPTIONS                               │
│ Content-Type: application/json                     │
│                                                     │
│ [Request] [Response]                               │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Content Type: [application/json]                │ │
│ │                                                 │ │
│ │ {"estado":"exito",                             │ │
│ │  "mensaje":"Orden creada. Total: 178.5"}       │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Step 3: Make a POST Request (Optional but better evidence)

**Using Postman:**
1. Create new request → **POST**
2. URL: `http://100.31.109.121:8000/api/v1/comprar/`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "libro_id": 1,
  "cantidad": 1,
  "direccion_envio": "AWS Testing"
}
```
5. Click **Send**
6. **Screenshot** showing:
   - Request URL
   - POST method
   - Request body
   - Response: 201 Created
   - Response body with `"estado":"exito"`

**Using Browser:**
1. Scroll down on the DRF interface
2. Fill the form fields:
   - libro_id: `1`
   - cantidad: `1`
   - direccion_envio: `AWS Testing`
3. Click **POST** button
4. **Screenshot** showing the response

### Step 4: What to Capture

**Essential Elements in Screenshot:**
- ✅ URL bar showing: `http://100.31.109.121:8000/api/v1/comprar/`
- ✅ HTTP method: **POST**
- ✅ Request body with JSON
- ✅ Response status: **201 Created**
- ✅ Response body: `{"estado":"exito",...}`

---

## 💻 Alternative: Using PowerShell (Windows)

If screenshot from browser doesn't work, prove it via terminal:

```powershell
# In your local PowerShell (NOT EC2 terminal):

$body = @{
    libro_id = 1
    cantidad = 1
    direccion_envio = "AWS Testing"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://100.31.109.121:8000/api/v1/comprar/" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body `
    -UseBasicParsing

Write-Host "Status Code: $($response.StatusCode)"
Write-Host "Response: $($response.Content)"
```

**Screenshot the output showing:**
- Status Code: 201
- Response: `{"estado":"exito",...}`

---

## 🎯 What the Professor Will Check

1. **URL in browser:** Matches `http://100.31.109.121:8000/api/v1/comprar/`
2. **API Response:** Returns JSON with `"estado": "exito"`
3. **HTTP Status:** 201 Created (not 200, not error)
4. **Infrastructure:** Proves Docker + AWS EC2 working together
5. **Code Reuse:** Same `CompraService` used in HTML and API

---

## 🔄 If You Get 404 or Error

**Troubleshoot:**

1. **Check AWS Security Group:**
   ```bash
   # In AWS console:
   EC2 → Instances → Select instance → Security tab
   # Verify inbound rule: Custom TCP, Port 8000, Source 0.0.0.0/0
   ```

2. **Check Docker is running:**
   ```bash
   # In EC2 terminal:
   docker ps
   # Should show 2 containers: web and db
   ```

3. **Check logs:**
   ```bash
   docker logs teis-djangosolid-web-1
   # Look for "Watching for file changes" or errors
   ```

4. **Wait a few seconds:**
   - Docker container may still be starting
   - Try again after 30 seconds

---

## 📋 Final Submission

**Files to give to Professor:**

1. This screenshot (visual proof)
2. `TUTORIAL04_DOCKER_AWS.md` (instructions)
3. All source code files
4. `docker-compose.yml` (deployment config)
5. `Dockerfile` (container recipe)

**Proof of Success:**
- ✅ Local: `http://localhost:8000/api/v1/comprar/` works
- ✅ AWS: `http://100.31.109.121:8000/api/v1/comprar/` works
- ✅ Same code, different infrastructure

---

**Now take your screenshot and you're done!** 📸✅
