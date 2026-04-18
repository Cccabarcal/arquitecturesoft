#!/bin/bash
# deploy.sh - Script de ayuda para desplegar en AWS EC2
# Uso: Ejecutar en la instancia EC2 después de clonar el repo

set -e  # Salir si algún comando falla

echo "==========================================="
echo "  DEPLOY TEIS-DjangoSOLID en AWS EC2"
echo "==========================================="

# 1. Verificar que Docker está instalado
echo "✓ Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi
echo "✓ Docker está presente"

# 2. Crear archivo .env desde .env.example
echo "✓ Configurando variables de entorno..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Archivo .env creado. Edítalo si es necesario."
else
    echo "✓ .env ya existe"
fi

# 3. Construir y lanzar contenedores
echo "✓ Construyendo imagen Docker..."
docker compose down || true  # Detiene contenedores previos si existen
docker compose up -d --build

echo ""
echo "==========================================="
echo "  ✅ DESPLIEGUE COMPLETADO"
echo "==========================================="
echo ""
echo "🌐 Accede a la aplicación en:"
echo "   http://\$(hostname -I | awk '{print \$1}'):8000/app/api/v1/comprar/"
echo ""
echo "📋 Comandos útiles:"
echo "   docker ps                    # Ver contenedores activos"
echo "   docker logs -f <id>          # Ver logs en tiempo real"
echo "   docker compose down          # Detener contenedores"
echo ""
