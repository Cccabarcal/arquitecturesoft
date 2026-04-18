import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tienda.settings')
django.setup()

from tienda_app.models import Libro
from tienda_app.services import CompraRapidaService
from tienda_app.infra.gateways import BancoNacionalProcesador

# Inicializar el servicio
procesador = BancoNacionalProcesador()
servicio = CompraRapidaService(procesador)

# Obtener los libros
libros = Libro.objects.all()[:3]

print("\n" + "="*60)
print("🛒 PRUEBAS DE COMPRA RÁPIDA - GENERANDO LOG DE AUDITORÍA")
print("="*60 + "\n")

for i, libro in enumerate(libros, 1):
    print(f"📚 Compra {i}: {libro.titulo}")
    print(f"   Precio: ${libro.precio}")
    
    try:
        total = servicio.procesar(libro.id)
        print(f"   ✅ Compra exitosa - Total: ${total}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()

# Verificar que el archivo de log existe
archivo_log = f"pagos_locales_{procesador.NOMBRE_ESTUDIANTE}.log"
if os.path.exists(archivo_log):
    print(f"\n✅ Archivo de log creado: {archivo_log}")
    print("\n📋 Contenido del log:")
    print("-" * 60)
    with open(archivo_log, "r") as f:
        print(f.read())
    print("-" * 60)
else:
    print(f"\n❌ Archivo de log NO encontrado: {archivo_log}")

print("\n" + "="*60)
print("✅ PRUEBAS COMPLETADAS")
print("="*60 + "\n")
