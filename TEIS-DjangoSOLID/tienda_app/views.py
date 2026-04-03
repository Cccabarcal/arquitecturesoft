import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

from .models import Libro, Inventario, Orden
from .infra.factories import PaymentFactory
from .services import CompraService


# ==================== PASO 1: FBV SPAGHETTI ====================
def compra_rapida_fbv(request, libro_id):
    """
    Function-Based View con MÚLTIPLES RESPONSABILIDADES (Antipatrón SRP).
    - Gestiona inventario
    - Calcula impuestos
    - Realiza I/O del sistema
    - Contiene lógica de negocio
    """
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        # VIOLACION SRP: Lógica de inventario en la vista
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad > 0:
            # VIOLACION OCP: Cálculo de negocio hardcoded
            total = float(libro.precio) * 1.19

            # VIOLACION DIP: Proceso de pago acoplado al file system
            with open("pagos_manuales.log", "a") as f:
                f.write(f"[{datetime.datetime.now()}] Pago FBV: ${total}\n")

            inventario.cantidad -= 1
            inventario.save()
            Orden.objects.create(libro=libro, total=total)

            return HttpResponse(f"Compra exitosa: {libro.titulo}")
        else:
            return HttpResponse("Sin stock", status=400)

    total_estimado = float(libro.precio) * 1.19
    return render(
        request,
        'tienda_app/compra_rapida.html',
        {'libro': libro, 'total': total_estimado}
    )


# ==================== PASO 2: CLASS-BASED VIEW ====================
class CompraRapidaView(View):
    """
    CBV: Separa los verbos HTTP (GET y POST).
    Elimina condicionales innecesarios y prepara para inyección de dependencias.
    """
    template_name = 'tienda_app/compra_rapida.html'

    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = float(libro.precio) * 1.19
        return render(request, self.template_name, {
            'libro': libro,
            'total': total,
            'view_type': 'CBV'
        })

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


# ==================== PASO 3: VISTA CON ARQUITECTURA SOLID ====================
class CompraView(View):
    """
    CBV: Vista Basada en Clases.
    Actúa como un "Portero": recibe la petición y delega al servicio.
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
            return render(
                request,
                self.template_name,
                {
                    'mensaje_exito': f"¡Gracias por su compra! Total: ${total}",
                    'total': total,
                },
            )
        except (ValueError, Exception) as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)
