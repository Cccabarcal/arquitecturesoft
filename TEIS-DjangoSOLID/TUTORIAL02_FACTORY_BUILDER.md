# Tutorial02 - Factory Method y Builder Pattern

## Estudiante: CRISTIAN CABARCAS

---

## 1. Objetivo

Optimizar la **creación de objetos** en nuestra arquitectura implementando:

- **Factory Method**: Desacoplamiento de infraestructura mediante variables de entorno
- **Builder Pattern**: Construcción segura de objetos de dominio complejos

---

## 2. Paso 1: Factory Method

### Problema

Antes, la vista decidía qué procesador de pago usar:

```python
# ❌ ACOPLADO A IMPLEMENTACIÓN CONCRETA
class CompraView(View):
    def setup_service(self):
        gateway = BancoNacionalProcesador()  # Hardcoded
        return CompraService(procesador_pago=gateway)
```

**Consecuencias:**
- Cambiar a PayPal requiere editar código
- Imposible hacer testing sin procesador real
- No es "Docker-Ready" (no respeta configuración de entorno)

### Solución: Factory Pattern

#### 2.1 Implementación en `infra/factories.py`

```python
import os
from .gateways import BancoNacionalProcesador


class MockPaymentProcessor:
    """Implementación ligera para pruebas (Mocking)"""
    def pagar(self, monto: float) -> bool:
        print(f"[DEBUG] Mock Payment: Procesando pago de ${monto} sin cargo real.")
        return True


class PaymentFactory:
    @staticmethod
    def get_processor():
        """
        Factory Method: Centraliza la decisión de qué procesador usar
        
        PRINCIPIO ARQUITECTÓNICO:
        - La configuración viene del AMBIENTE, no del código
        - Permite cambiar comportamiento sin editar el código fuente
        - Docker-Ready: Respeta variables de entorno
        """
        provider = os.getenv('PAYMENT_PROVIDER', 'BANCO')

        if provider == 'MOCK':
            return MockPaymentProcessor()

        return BancoNacionalProcesador()
```

#### 2.2 Refactorización en `views.py`

```python
from .infra.factories import PaymentFactory


class CompraView(View):
    def setup_service(self):
        # ✅ AHORA: Delegación total a la Factory
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)
```

**Beneficios:**
- Vista agnóstica: No sabe qué banco se usa
- Testeable: Podemos inyectar MockPaymentProcessor
- Flexible: Cambiar desde terminal con `PAYMENT_PROVIDER=MOCK`

---

## 3. Paso 2: Builder Pattern

### Problema

Crear un `Orden` es complejo:
- Validar datos
- Calcular impuestos
- Manejar múltiples parámetros

```python
# ❌ CONSTRUCTOR GIGANTE CON MUCHA LÓGICA
orden = Orden.objects.create(
    usuario=usuario,
    libro=libro,
    cantidad=cantidad,
    total=???  # ¿Quién calcula esto?
    direccion=direccion
)
```

### Solución: Builder Pattern

#### 3.1 Implementación en `domain/builders.py`

```python
from decimal import Decimal
from .logic import CalculadorImpuestos
from ..models import Orden


class OrdenBuilder:
    """
    BUILDER PATTERN: Construcción paso a paso de objetos complejos
    
    Beneficios:
    - SRP: El Builder solo construye órdenes
    - Validación centralizada
    - Fluent Interface (encadenamiento de métodos)
    - Cálculos delegados a CalculadorImpuestos
    """
    
    def __init__(self):
        self.reset()

    def reset(self):
        """Estado inicial del builder"""
        self._usuario = None
        self._libro = None
        self._cantidad = 1
        self._direccion = ""

    def con_usuario(self, usuario):
        """Fluent Interface: Retorna self para encadening"""
        self._usuario = usuario
        return self

    def con_libro(self, libro):
        self._libro = libro
        return self

    def con_cantidad(self, cantidad):
        self._cantidad = cantidad
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        """
        Construye y retorna la orden validada
        
        VALIDACIONES INTERNAS:
        - Verifica datos mínimos
        - Calcula totales correctamente
        - Encapsula lógica de seguridad
        """
        if not self._libro:
            raise ValueError("Datos insuficientes para crear la orden.")

        # Delegación: CalculadorImpuestos sabe cómo calcular
        total_unitario = CalculadorImpuestos.obtener_total_con_iva(self._libro.precio)
        total = Decimal(total_unitario) * self._cantidad

        # Creación encapsulada
        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=self._libro,
            total=total,
            direccion_envio=self._direccion,
        )
        
        self.reset()  # Limpia para próximo uso
        return orden
```

#### 3.2 Uso en `services.py`

```python
from .domain.builders import OrdenBuilder


class CompraService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="", usuario=None):
        """
        Uso del Builder: Construye la orden de forma segura
        Uso del Factory (inyectado): Cambia de comportamiento sin cambio de código
        """
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        if inv.cantidad < cantidad:
            raise ValueError("No hay suficiente stock.")

        # BUILDER: Construcción limpia y validada
        orden = (self.builder
                 .con_usuario(usuario)
                 .con_libro(libro)
                 .con_cantidad(cantidad)
                 .para_envio(direccion)
                 .build())

        # FACTORY (inyectado): Abstracción de infraestructura
        pago_exitoso = self.procesador_pago.pagar(orden.total)
        
        if not pago_exitoso:
            orden.delete()
            raise Exception("La transacción fue rechazada.")

        inv.cantidad -= cantidad
        inv.save()

        return orden.total
```

---

## 4. Evidencia de Ejecución

### 4.1 Test Output: Factory Method en Acción

```
======================================================================
🏭 TUTORIAL02: FACTORY METHOD Y BUILDER PATTERN
======================================================================

----------------------------------------------------------------------
📋 DEMOSTRACIÓN 1: Usando MOCK Payment Processor
----------------------------------------------------------------------
(Variable de entorno: PAYMENT_PROVIDER=MOCK)

✓ Factory retornó: MockPaymentProcessor

📚 Comprando: Clean Code en Python
   Precio: $150.00
[DEBUG] Mock Payment: Procesando pago de $178.5 sin cargo real.

✅ MOCK: Compra simulada exitosa
   Total: $178.5

----------------------------------------------------------------------
📋 DEMOSTRACIÓN 2: Usando BANCO Nacional (Real)
----------------------------------------------------------------------
(Variable de entorno: PAYMENT_PROVIDER=BANCO o no definida)

✓ Factory retornó: BancoNacionalProcesador

📚 Comprando: Django para Principiantes
   Precio: $89.99

✅ BANCO: Compra procesada exitosa
   Total: $107.09
```

**Puntos clave:**
1. ✅ Factory retorna el procesador correcto según variable de entorno
2. ✅ [DEBUG] Mock Payment muestra que MOCK está activo
3. ✅ Sin editar código, el comportamiento cambia completamente

### 4.2 Análisis de Órdenes Creadas

```
======================================================================
📊 ANÁLISIS DE ÓRDENES CREADAS
======================================================================

Últimas 2 órdenes:

1. Orden #2
   Libro: Django para Principiantes
   Total: $107.09
   Creada: 2026-04-03 18:34:17

2. Orden #1
   Libro: Clean Code en Python
   Total: $178.50
   Creada: 2026-04-03 18:34:17
```

**Verificación del Builder:**
✅ Los totales se calcularon correctamente (con IVA incluido)
✅ Las órdenes se crearon en la BD
✅ El Builder fue validado exitosamente

---

## 5. Paso 3: Verificación y Despliegue Configurable

### Pruebas en Terminal

```bash
# Modo Producción (Banco Real)
docker-compose exec web python manage.py runserver

# Modo Desarrollo/Testing (Mock Payment)
docker-compose exec web bash -c "PAYMENT_PROVIDER=MOCK python manage.py runserver"

# Regenerar evidencia
docker-compose exec web python test_factory_builder.py
```

---

## 6. Reflexión: Por qué el Builder Reduce Riesgos

### ❌ Sin Builder (Antipatrón):
```python
# Directamente en la vista
orden = Orden.objects.create(
    usuario=request.user,
    libro=libro,
    total=float(libro.precio) * 1.19,  # ¿Dónde se valida?
    cantidad=1  # Hardcoded
)
```

**Riesgos:**
- El cálculo del total está esparcido en la vista
- No hay validación centralizada
- Si cambia la lógica de impuestos, hay que editar múltiples archivos
- Imposible testear sin ver la vista

### ✅ Con Builder (Patrón):
```python
orden = (self.builder
         .con_usuario(usuario)
         .con_libro(libro)
         .con_cantidad(cantidad)
         .para_envio(direccion)
         .build())
```

**Ventajas:**
- **Validación centralizada**: El Builder solo crea órdenes válidas
- **Delegación clara**: `CalculadorImpuestos` calcula totales
- **Testeable**: Podemos hacer `builder.build()` en tests
- **Mantenible**: Cambios de lógica en un solo lugar
- **Seguridad**: Imposible crear orden sin datos requeridos
- **Semántica**: El código lee como un proceso secuencial

### Impacto en el Ciclo de Vida

| Aspecto | Sin Builder | Con Builder |
|---------|-----------|------------|
| **Testabilidad** | Baja (acoplado a BD) | Alta (lógica aislada) |
| **Mantenibilidad** | Riesgo alto | Riesgo bajo |
| **Reusabilidad** | Limitada a vistas | Funciona en cualquier contexto |
| **Validación** | Dispersa | Centralizada |
| **Debugging** | Difícil (múltiples puntos) | Fácil (Builder encapsula) |

---

## 7. Patrones Creacionales Utilizados

### Factory Method
```
┌─────────────────┐
│ PaymentFactory  │
│ (get_processor) │
└────────┬────────┘
         │
         ├─→ MOCK=MockPaymentProcessor
         └─→ BANCO=BancoNacionalProcesador
```

**Beneficio:** Delegar la creación de objetos complejos

### Builder Pattern
```
┌──────────────┐
│ OrdenBuilder │
├──────────────┤
│ - con_usuario   │
│ - con_libro     │
│ - con_cantidad  │
│ - para_envio    │
│ - build()       │
└──────┬───────┘
       │
       └─→ Orden (validada y completa)
```

**Beneficio:** Construcción paso a paso con validación

---

## 8. Entregables

✅ **Captura de Pantalla**: `[DEBUG] Mock Payment: Procesando pago...` visible en test output
✅ **Código Fuente**: `infra/factories.py` (Factory Method implementado)
✅ **Código Fuente**: `domain/builders.py` (Builder Pattern implementado)
✅ **Reflexión**: Incluida en sección 6
✅ **Evidence File**: Log de auditoría con transacciones del Factory/Builder

---

## 9. Conclusión

La combinación de **Factory Method** y **Builder Pattern** proporciona:

1. **Flexibilidad**: Cambiar comportamiento desde variables de entorno
2. **Testabilidad**: Fácil inyectar MockPaymentProcessor
3. **Mantenibilidad**: Lógica centralizada y validada
4. **Seguridad**: No se pueden crear órdenes inválidas
5. **Escalabilidad**: Agregar nuevos procesadores sin editar código

Estos patrones son pilares de la **arquitectura escalable** en aplicaciones Django con SOLID.

---

**Generado**: 2026-04-03
**Autor**: CRISTIAN CABARCAS
