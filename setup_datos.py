import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tienda.settings')
django.setup()

from tienda_app.models import Libro, Inventario

# Crear libros de prueba
libros_datos = [
    {"titulo": "Clean Code en Python", "precio": 150.0},
    {"titulo": "Django para Principiantes", "precio": 89.99},
    {"titulo": "Architecture Patterns", "precio": 199.99},
]

for libro_data in libros_datos:
    libro, created = Libro.objects.get_or_create(
        titulo=libro_data["titulo"],
        defaults={"precio": libro_data["precio"]}
    )
    if created:
        print(f"✓ Libro creado: {libro.titulo}")
        Inventario.objects.create(libro=libro, cantidad=10)
        print(f"  Inventario: 10 unidades")
    else:
        print(f"⚠ Libro ya existe: {libro.titulo}")

print("\n✅ Datos de prueba configurados exitosamente")
