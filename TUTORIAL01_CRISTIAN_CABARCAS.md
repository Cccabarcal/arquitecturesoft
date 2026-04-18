# Tutorial01 - Django SOLID: Resumen de Código

## Estudiante: CRISTIAN CABARCAS

---

## 1. Estructura de la Solución

El tutorial implementa una progresión de 3 fases en la mejora arquitectónica de una funcionalidad de compra:

1. **FBV Spaghetti** (Antipatrón): `compra_rapida_fbv()`
2. **Class-Based View (CBV)**: `CompraRapidaView`
3. **SOLID + Service Layer**: `CompraView` + `CompraRapidaService`

---

## 2. Código Implementado

### 2.1 views.py - Las tres aproximaciones

```python
# PASO 1: FBV SPAGHETTI - ANTIPATRÓN
def compra_rapida_fbv(request, libro_id):
    """
    Violaciones SOLID:
    - SRP: Mezcla lógica de inventario, cálculo de impuestos y persistencia
    - OCP: Hardcoded business logic
    - DIP: Acoplado al file system para pagos
    """
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad > 0:
            total = float(libro.precio) * 1.19
            
            with open("pagos_manuales.log", "a") as f:
                f.write(f"[{datetime.datetime.now()}] Pago FBV: ${total}\n")
            
            inventario.cantidad -= 1
            inventario.save()
            Orden.objects.create(libro=libro, total=total)
            
            return HttpResponse(f"Compra exitosa: {libro.titulo}")
        else:
            return HttpResponse("Sin stock", status=400)

    total_estimado = float(libro.precio) * 1.19
    return render(request, 'tienda_app/compra_rapida.html', 
                  {'libro': libro, 'total': total_estimado})


# PASO 2: CLASS-BASED VIEW - MEJOR SEPARACIÓN
class CompraRapidaView(View):
    """
    Mejoras:
    - Separa GET y POST
    - Más legible y mantenible
    - Prepara para inyección de dependencias
    """
    template_name = 'tienda_app/compra_rapida.html'

    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = float(libro.precio) * 1.19
        return render(request, self.template_name, 
                      {'libro': libro, 'total': total, 'view_type': 'CBV'})

    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = Inventario.objects.get(libro=libro)
        if inv.cantidad > 0:
            total = float(libro.precio) * 1.19
            inv.cantidad -= 1
            inv.save()
            Orden.objects.create(libro=libro, total=total)
            return HttpResponse(f"Comprado via CBV: {libro.titulo}")
        return HttpResponse("Error: Sin stock", status=400)


# PASO 3: ARQUITECTURA SOLID CON SERVICE LAYER
class CompraView(View):
    """
    Arquitectura Limpia:
    - Vista solo recibe y delega
    - Lógica de negocio en servicio
    - Inyección de dependencias
    """
    template_name = 'tienda_app/compra.html'

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(request, self.template_name, {
                'mensaje_exito': f"¡Gracias por su compra! Total: ${total}",
                'total': total,
            })
        except (ValueError, Exception) as e:
            return render(request, self.template_name, 
                          {'error': str(e)}, status=400)
```

---

### 2.2 services.py - Service Layer con SOLID

```python
class CompraRapidaService:
    """
    SERVICE LAYER para Compra Rápida.
    - Extrae lógica de orquestación de la vista
    - La vista solo actúa como bridge HTTP-to-business
    - Implementa principios SOLID:
      * SRP: Una responsabilidad = procesar compra
      * OCP: Extensible sin modificar código existente
      * DIP: Depende de abstracción (procesador_pago)
    """

    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago

    def procesar(self, libro_id):
        # SRP: Cada componente tiene una responsabilidad
        libro = Libro.objects.get(id=libro_id)
        inv = Inventario.objects.get(libro=libro)

        if inv.cantidad <= 0:
            raise ValueError("No hay existencias.")

        # Lógica de cálculo delegada a su propio módulo
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        # DIP: Depende de abstracción, no de implementación concreta
        if self.procesador_pago.pagar(total):
            inv.cantidad -= 1
            inv.save()
            return total
        return None
```

---

### 2.3 infra/gateways.py - Implementación del Gateway

```python
import datetime
from ..domain.interfaces import ProcesadorPago


class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Cumple la interfaz ProcesadorPago (Abstracción).
    
    Responsabilidades:
    - Procesar pagos (simulado)
    - Generar auditoría de transacciones
    """
    
    NOMBRE_ESTUDIANTE = "CRISTIAN_CABARCAS"
    
    def pagar(self, monto: float) -> bool:
        """
        Procesa el pago y registra en archivo de auditoría.
        
        ✅ Cumple DIP: La lógica de negocio no conoce esta implementación
        ✅ Cumple OCP: Podemos reemplazarla sin cambiar el servicio
        """
        archivo_log = f"pagos_locales_{self.NOMBRE_ESTUDIANTE}.log"
        
        with open(archivo_log, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] Transacción exitosa por: ${monto}\n")
        
        return True
```

---

## 3. Principios SOLID Aplicados

| Principio | Antes (FBV) | Después (SOLID) |
|-----------|------------|-----------------|
| **S**RP | ❌ Vista hace TODO | ✅ Cada clase = 1 responsabilidad |
| **O**CP | ❌ Lógica hardcoded | ✅ Extensible sin modificar |
| **L**SP | ❌ Sin abstracción | ✅ Implementation hiding |
| **I**SP | ❌ Grande monolito | ✅ Interfaces específicas |
| **D**IP | ❌ Acoplado a file system | ✅ Depende de abstracción |

---

## 4. Archivo de Log Generado

**Ubicación**: `pagos_locales_CRISTIAN_CABARCAS.log`

**Contenido** (3 transacciones exitosas):
```
[2026-04-03 18:30:38] Transacción exitosa por: $178.5
[2026-04-03 18:30:38] Transacción exitosa por: $107.08809999999998
[2026-04-03 18:30:38] Transacción exitosa por: $237.9881
```

---

## 5. Instrucciones de Verificación

### Para probar las 3 vistas:

#### FBV Spaghetti (Antipatrón):
```bash
http://localhost:8000/app/compra-rapida-fbv/1/
```

#### CBV (Mejor):
```bash
http://localhost:8000/app/compra-rapida-cbv/1/
```

#### SOLID + Service Layer (Recomendado):
```bash
http://localhost:8000/app/compra/1/
```

### Para regenerar el log:
```bash
docker-compose exec web python test_compras.py
```

---

## 6. Entregables

✅ **Archivo de Log**: `pagos_locales_CRISTIAN_CABARCAS.log` (3+ transacciones)
✅ **Código de services.py**: Implementación Service Layer completa
✅ **Código de views.py**: 3 aproximaciones (FBV → CBV → SOLID)
✅ **Documento de resumen**: Este archivo

---

## 7. Conclusiones

La evolución arquitectónica demuestra:

1. **FBV Spaghetti** ❌
   - Todo mezclado en una función
   - Difícil de testear
   - Difícil de mantener

2. **CBV** ⚠️ 
   - Mejor separación GET/POST
   - Aún lleva lógica de negocio

3. **SOLID + Service Layer** ✅
   - Vista = presentación
   - Servicio = lógica de negocio
   - Gateway = infraestructura
   - Testeable, mantenible, escalable

---


