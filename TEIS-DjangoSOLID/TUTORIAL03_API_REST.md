# Tutorial03: DRF & API - Evidencia de Entrega

**Estudiante:** CRISTIAN CABARCAS  
**Fecha:** 2026-04-03

---

## Objetivo

Demostrar que la **API REST** y las **vistas HTML** reutilizan la **misma lógica de negocio**. 

**"Ambas puertas conducen a la misma habitación"**

---

## 1. Evidencia de Ejecución

### 1.1 Compra vía API

**Endpoint:** `POST /api/v1/comprar/`

**Payload:**
```json
{
  "libro_id": 1,
  "direccion_envio": "Calle Principal 123, Apartado 5",
  "cantidad": 1
}
```

**Respuesta (HTTP 201 Created):**
```json
{
  "estado": "exito",
  "mensaje": "Orden creada. Total: $178.5"
}
```

### 1.2 Verificación de Cambios en Inventario

```
ANTES de compra API:  10 unidades
  ↓ (Compra vía API)
DESPUÉS de compra API: 9 unidades

✓ Stock decrementado correctamente
```

### 1.3 Orden Registrada en Base de Datos

```
Orden #7 creada:
  - Libro: Clean Code en Python
  - Total: $178.50
  - Dirección: Calle Principal 123, Apartado 5
  - Timestamp: 2026-04-03 18:37:45
```

### 1.4 Log de Auditoría Registrado

```
[2026-04-03 18:37:45] Transacción exitosa por: $178.5
```

---

## 2. Arquitectura: La Prueba de Integración

### Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────┐
│            MISMA LÓGICA, MÚLTIPLES PUERTAS              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PUERTA 1: HTML                PUERTA 2: API REST       │
│  ↓                              ↓                       │
│  CompraView.post()       →      CompraAPIView.post()   │
│  (vistasHTML)                  (API JSON)              │
│  ↓ (request.POST)              ↓ (JSON payload)        │
│  └──────────────────────────────┘                      │
│             ↓                                           │
│  CAPA DE SERVICIOS (La Verdad Única)                   │
│             ↓                                           │
│  CompraService.ejecutar_compra(                        │
│    libro_id = datos['libro_id'],                       │
│    cantidad = datos['cantidad'],                       │
│    direccion = datos['direccion_envio'],               │
│    usuario = request.user                              │
│  )                                                      │
│             ↓                                           │
│  ├─ 1. Obtener libro                                   │
│  ├─ 2. Validar stock                                   │
│  ├─ 3. Calcular total (IVA incluido)                   │
│  ├─ 4. Procesar pago (Factory inyecta Mock/Real)       │
│  ├─ 5. Crear orden                                     │
│  ├─ 6. Decrementar inventario                          │
│  └─ 7. Registrar en log                                │
│             ↓                                           │
│  BD: Misma orden                                        │
│  LOG: Misma transacción                                │
│  INVENTARIO: Mismo descuento                           │
│             ↓                                           │
│  Respuesta al usuario                                  │
│  (HTML: render template)  (API: JSON)                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Código: La Implementación

### 3.1 Serializer (API Input Adapter)

```python
class OrdenInputSerializer(serializers.Serializer):
    """
    Adapter Pattern: Transforma JSON en datos internos
    Validación de entrada: ANTES de tocar la lógica
    """
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)
    cantidad = serializers.IntegerField(min_value=1, default=1)
```

### 3.2 API View (El Controlador)

```python
class CompraAPIView(APIView):
    """
    Endpoint REST que reutiliza CompraService
    MISMO servicio, diferente entrada (JSON vs form)
    """
    def post(self, request):
        # 1. Validar entrada (Adapter)
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        datos = serializer.validated_data
        
        try:
            # 2. Inyectar dependencias (Factory)
            gateway = PaymentFactory.get_processor()
            
            # 3. REUTILIZAR servicio (Punto clave)
            servicio = CompraService(procesador_pago=gateway)
            
            # 4. Ejecutar MISMA lógica
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                cantidad=datos.get('cantidad', 1),
                direccion=datos['direccion_envio'],
                usuario=request.user if request.user.is_authenticated else None,
            )
            
            # 5. Retornar
            return Response(
                {'estado': 'exito', 'mensaje': f'Orden creada. Total: {resultado}'},
                status=HTTP_201_CREATED
            )
        
        except ValueError as e:
            return Response({'error': str(e)}, status=HTTP_409_CONFLICT)
except Exception:
            return Response({'error': 'Error interno'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
```

### 3.3 HTML View (El Original)

```python
class CompraView(View):
    """
    HTML que TAMBIÉN reutiliza CompraService
    MISMO servicio, diferente entrada (form vs JSON)
    """
    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            # MISMA llamada al servicio
            total = servicio.ejecutar_compra(
                libro_id=libro_id,
                cantidad=1,
                usuario=request.user
            )
            return render(request, template, {'mensaje_exito': f'Total: ${total}'})
        except Exception as e:
            return render(request, template, {'error': str(e)}, status=400)
```

---

## 4. Principios Aplicados

| Principio | Aplicación |
|-----------|-----------|
| **DRY (Don't Repeat Yourself)** | Una sola CompraService para HTML y API |
| **Adapter Pattern** | OrdenInputSerializer adapta JSON a datos internos |
| **Dependency Injection** | Factory inyecta procesador (Mock/Real) |
| **Single Source of Truth** | Lógica en CompraService, no duplicada |
| **Separation of Concerns** | API View ≠ Service; Serializer ≠ Logic |

---

## 5. Testigos y Pruebas

### 5.1 Test Output
```
TUTORIAL03: DRF & API - Evidencia de Integración
===============================================

1. ESTADO INICIAL DEL INVENTARIO
Stock ANTES de comprar: 10 unidades

2. SIMULACIÓN DE COMPRA VÍA API
POST /app/api/v1/comprar/
Payload: {
  "libro_id": 1,
  "direccion_envio": "Calle Principal 123",
  "cantidad": 1
}

Respuesta Status: 201
Response: {
  "estado": "exito",
  "mensaje": "Orden creada. Total: $178.5"
}

3. VERIFICACIÓN DE INVENTARIO - DESPUÉS
Stock DESPUÉS: 9 unidades
Decrementado: 10 → 9 ✓

4. ÓRDENES CREADAS
Orden #7: Clean Code en Python - $178.50

5. LOG DE AUDITORÍA
[2026-04-03 18:37:45] Transacción exitosa por: $178.5
```

### 5.2 Verificación Manual

**Paso 1:** Crear orden vía API
```bash
curl -X POST http://localhost:8000/app/api/v1/comprar/ \
  -H "Content-Type: application/json" \
  -d '{"libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1}'
```

**Paso 2:** Verificar que el inventario cambió
```bash
# La BD refleja el cambio
# El log registra la transacción
# La orden existe en Orden.objects
```

**Paso 3:** Verificar con HTML
```bash
# POST http://localhost:8000/app/compra/1/
# MISMO inventario decrementado
# MISMO log registrado
# MISMA lógica ejecutada
```

---

## 6. Conclusión: Multiples Clientes, Una Lógica

```
                Lógica de Negocio
                    (Service)
                       ↑
        ┌──────────────┼──────────────┐
        │              │              │
    HTML View      API View      CLI Script
        │              │              │
     Request       JSON POST      Python Call
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                   BD Única
                (Orden + Inventario)
```

**Beneficio:** 
- ✅ Cambio en lógica se aplica a TODAS las interfaces
- ✅ No hay duplicación de código
- ✅ Fácil de testear (lógica centralizada)
- ✅ Arquitectura robusta y escalable

---

## 7. Archivos Entregables

✅ `test_api_evidence.py` - Script de demostración  
✅ `TUTORIAL03_API_REST.md` - Este documento  
✅ `tienda_app/api/serializers.py` - Adapter Pattern  
✅ `tienda_app/api/views.py` - API View con reutilización  
✅ `pagos_locales_CRISTIAN_CABARCAS.log` - Auditoría actualizado  
✅ Screenshot Postman (cuando ejecutes el test)  

---

## 8. Instrucciones para Captura Postman

1. **Abrir Postman** (o usar interfaz web de DRF en `http://localhost:8000/app/api/v1/comprar/`)

2. **Crear request:**
   - Method: `POST`
   - URL: `http://localhost:8000/app/api/v1/comprar/`
   - Headers: `Content-Type: application/json`
   - Body (raw):
   ```json
   {
     "libro_id": 1,
     "direccion_envio": "Calle Principal 123",
     "cantidad": 1
   }
   ```

3. **Click SEND**

4. **Capturar pantalla mostrando:**
   - ✅ Request details
   - ✅ Response status (201 Created)
   - ✅ Response body con "estado": "exito"
   - ✅ Inventario decrementado en BD

---

**Generado:** 2026-04-03  
**Autor:** CRISTIAN CABARCAS  
**Estado:** ✅ LISTO PARA ENTREGA
