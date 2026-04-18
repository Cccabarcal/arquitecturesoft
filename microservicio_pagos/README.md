# Microservicio Flask - Pagos (v2)

Este es el microservicio que estrangula la funcionalidad de compras del monolito Django.

## Estructura

- `app.py` - Aplicación Flask principal
- `Dockerfile` - Imagen Docker para Flask
- `requirements.txt` - Dependencias Python

## Endpoints

### POST /api/v2/comprar
Endpoint principal para procesar pagos. Reemplaza la función de compra del monolito.

**Request:**
```json
{
  "producto_id": 1,
  "cantidad": 5,
  "usuario_id": 10
}
```

**Response:**
```json
{
  "estado": "procesada exitosamente por el Microservicio Flask",
  "timestamp": "2024-01-15T10:30:00.000000",
  "datos_recibidos": {...},
  "servicio": "Flask Microservicio Pagos (v2)"
}
```

### GET /health
Health check endpoint para monitoreo.

### GET /
Endpoint raíz con información del servicio.

## Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python app.py
```

El servidor estará disponible en `http://localhost:5000`

## Docker

```bash
# Construir imagen
docker build -t pagos_flask:latest .

# Ejecutar contenedor
docker run -p 5000:5000 pagos_flask:latest
```
