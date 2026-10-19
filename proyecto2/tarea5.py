# polimorfismo_abc_contratos.py

from abc import ABC, abstractmethod

class ProcesadorPago(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> bool:
        pass

class PagoTarjeta(ProcesadorPago):
    def procesar(self, monto: float) -> bool:
        print(f"Cobrando ${monto} vía Pasarela de Tarjeta.")
        return True

# p = ProcesadorPago()  → Error: no se puede instanciar una clase abstracta
pago = PagoTarjeta()
pago.procesar(150.50)