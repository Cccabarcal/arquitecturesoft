import datetime
from ..domain.interfaces import ProcesadorPago


class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log auditable.
    
    IMPORTANTE: Cambiar "CRISTIAN_CABARCAS" por tu nombre real.
    """
    
    # TODO: Personaliza esto con tu nombre completo
    NOMBRE_ESTUDIANTE = "CRISTIAN_CABARCAS"
    
    def pagar(self, monto: float) -> bool:
        """
        Procesa el pago y registra en archivo de auditoría.
        Simula una operación de red o persistencia externa.
        """
        archivo_log = f"pagos_locales_{self.NOMBRE_ESTUDIANTE}.log"
        
        with open(archivo_log, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] Transacción exitosa por: ${monto}\n")
        
        return True
