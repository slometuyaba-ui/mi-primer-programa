# ejercicio_resuelto_2.py

from abc import ABC, abstractmethod

class TareaServidor(ABC):
    @abstractmethod
    def ejecutar(self) -> bool:
        pass

class TareaLimpiezaLogs(TareaServidor):
    def ejecutar(self) -> bool:
        print("Depurando archivos .log antiguos en /var/log...")
        return True

class TareaBackupDB(TareaServidor):
    def ejecutar(self) -> bool:
        print("Generando copia de respaldo en Amazon S3...")
        return True

def procesar_cola(tareas: list[TareaServidor]):
    for t in tareas:
        t.ejecutar()                          # Llamada polimórfica

cola = [TareaLimpiezaLogs(), TareaBackupDB(), TareaLimpiezaLogs()]
procesar_cola(cola)

# Orientación de solución

class TarjetaCredito:
    def calcular_cashback(self, monto: float) -> float:
        return 0.0

class TarjetaGold(TarjetaCredito):
    def calcular_cashback(self, monto: float) -> float:
        return monto * 0.02

class TarjetaBlack(TarjetaCredito):
    def calcular_cashback(self, monto: float) -> float:
        return monto * 0.05