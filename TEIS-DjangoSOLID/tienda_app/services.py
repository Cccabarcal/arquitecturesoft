from django.shortcuts import get_object_or_404

from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro, Orden


class CompraRapidaService:
    """
    PASO 3: SERVICE LAYER para Compra Rápida.
    Extrae la lógica de orquestación de la vista.
    La vista solo actúa como un puente entre la web y el servicio.
    """

    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago

    def procesar(self, libro_id):
        """
        Procesa una compra rápida siguiendo SOLID:
        - SRP: Cada componente tiene una responsabilidad
        - OCP: Extensible sin modificar código existente
        - DIP: Depende de abstracciones (procesador_pago)
        """
        libro = Libro.objects.get(id=libro_id)
        inv = Inventario.objects.get(libro=libro)

        if inv.cantidad <= 0:
            raise ValueError("No hay existencias.")

        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        if self.procesador_pago.pagar(total):
            inv.cantidad -= 1
            inv.save()
            return total
        return None


class CompraService:
    """
    SERVICE LAYER: Orquesta la interacción entre el dominio,
    la infraestructura y la base de datos.
    """

    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="", usuario=None):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        if inv.cantidad < cantidad:
            raise ValueError("No hay suficiente stock para completar la compra.")

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_libro(libro)
            .con_cantidad(cantidad)
            .para_envio(direccion)
            .build()
        )

        pago_exitoso = self.procesador_pago.pagar(orden.total)
        if not pago_exitoso:
            orden.delete()
            raise Exception("La transacción fue rechazada por el banco.")

        inv.cantidad -= cantidad
        inv.save()

        return orden.total
