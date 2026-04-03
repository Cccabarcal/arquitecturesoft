#!/usr/bin/env python
"""
TUTORIAL02: Factory Method y Builder Pattern
Demostramos cómo cambiar el comportamiento sin editar código
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tienda.settings')
django.setup()

from tienda_app.models import Libro, Inventario, Orden
from tienda_app.services import CompraService
from tienda_app.infra.factories import PaymentFactory

print("\n" + "="*70)
print("🏭 TUTORIAL02: FACTORY METHOD Y BUILDER PATTERN")
print("="*70)

# Demostración 1: Con MOCK Payment
print("\n" + "-"*70)
print("📋 DEMOSTRACIÓN 1: Usando MOCK Payment Processor")
print("-"*70)
print("(Variable de entorno: PAYMENT_PROVIDER=MOCK)")

os.environ['PAYMENT_PROVIDER'] = 'MOCK'

# Obtener procesador MOCK
procesador_mock = PaymentFactory.get_processor()
print(f"\n✓ Factory retornó: {procesador_mock.__class__.__name__}")

# Crear servicio con MOCK
servicio_mock = CompraService(procesador_pago=procesador_mock)

# Obtener libro
libro1 = Libro.objects.first()
print(f"\n📚 Comprando: {libro1.titulo}")
print(f"   Precio: ${libro1.precio}")

try:
    # Usar el Builder a través del servicio
    total = servicio_mock.ejecutar_compra(libro1.id, cantidad=1)
    print(f"\n✅ MOCK: Compra simulada exitosa")
    print(f"   Total: ${total}")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "-"*70)
print("📋 DEMOSTRACIÓN 2: Usando BANCO Nacional (Real)")
print("-"*70)
print("(Variable de entorno: PAYMENT_PROVIDER=BANCO o no definida)")

os.environ['PAYMENT_PROVIDER'] = 'BANCO'

# Obtener procesador REAL
procesador_banco = PaymentFactory.get_processor()
print(f"\n✓ Factory retornó: {procesador_banco.__class__.__name__}")

# Crear servicio con BANCO
servicio_banco = CompraService(procesador_pago=procesador_banco)

# Obtener segundo libro
libro2 = Libro.objects.all()[1] if Libro.objects.count() > 1 else libro1
print(f"\n📚 Comprando: {libro2.titulo}")
print(f"   Precio: ${libro2.precio}")

try:
    total = servicio_banco.ejecutar_compra(libro2.id, cantidad=1)
    print(f"\n✅ BANCO: Compra procesada exitosa")
    print(f"   Total: ${total}")
except Exception as e:
    print(f"\n❌ Error: {e}")

# Análisis de órdenes creadas
print("\n" + "="*70)
print("📊 ANÁLISIS DE ÓRDENES CREADAS")
print("="*70)

ordenes = Orden.objects.all().order_by('-fecha_creacion')[:5]
print(f"\nÚltimas {ordenes.count()} órdenes:\n")

for i, orden in enumerate(ordenes, 1):
    print(f"{i}. Orden #{orden.id}")
    print(f"   Libro: {orden.libro.titulo}")
    print(f"   Total: ${orden.total}")
    print(f"   Creada: {orden.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

# Verificar archivo de log
print("="*70)
print("📋 VERIFICACIÓN DE LOG DE AUDITORÍA")
print("="*70)

archivo_log = "pagos_locales_CRISTIAN_CABARCAS.log"
if os.path.exists(archivo_log):
    print(f"\n✓ Archivo encontrado: {archivo_log}\n")
    with open(archivo_log, "r") as f:
        content = f.read()
        lineas = content.split('\n')
        print(f"Total de transacciones: {len([l for l in lineas if l.strip()])}")
        print(f"\nÚltimas 5 transacciones:")
        print("-"*70)
        for linea in lineas[-5:]:
            if linea.strip():
                print(f"  {linea}")
else:
    print(f"\n✗ Archivo NO encontrado: {archivo_log}")

print("\n" + "="*70)
print("✅ PRUEBAS COMPLETADAS")
print("="*70 + "\n")
