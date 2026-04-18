#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tienda.settings')
django.setup()

from tienda_app.models import Libro, Inventario

# Eliminar datos existentes (opcional)
Libro.objects.all().delete()

# Crear libros de prueba
libros_data = [
    {"titulo": "Clean Code", "precio": 45.99},
    {"titulo": "Django for Beginners", "precio": 29.99},
    {"titulo": "Python Advanced", "precio": 39.99},
    {"titulo": "REST API Design", "precio": 34.99},
    {"titulo": "Microservices Patterns", "precio": 55.99},
]

for libro_data in libros_data:
    libro = Libro.objects.create(**libro_data)
    # Crear inventario con stock inicial
    Inventario.objects.create(libro=libro, cantidad=50)
    print(f"✓ Creado: {libro.titulo} (${libro.precio}) - Stock: 50")

print(f"\n✅ {len(libros_data)} libros creados exitosamente")
