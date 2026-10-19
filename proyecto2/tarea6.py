# ejemplo_encapsulacion.py

class CuentaBancaria:
    def __init__(self, titular: str, saldo_inicial: float):
        self.titular = titular
        self.__saldo = saldo_inicial          # Privado

    def depositar(self, monto: float):
        if monto > 0:
            self.__saldo += monto
        else:
            print("Error: Monto inválido.")

    def obtener_saldo(self) -> float:         # Getter controlado
        return self.__saldo

cuenta = CuentaBancaria("Ing. Hernández", 5000.0)
cuenta.depositar(1500.0)
print(cuenta.obtener_saldo())                 # 6500.0
# print(cuenta.__saldo)  → AttributeError






# decorador_property.py

class Empleado:
    def __init__(self, nombre: str, salario: float):
        self.nombre = nombre
        self._salario = salario               # Protegido

    @property
    def salario(self) -> float:               # Getter
        return self._salario

    @salario.setter
    def salario(self, nuevo_salario: float):  # Setter con validación
        if nuevo_salario >= 1300.0:
            self._salario = nuevo_salario
        else:
            raise ValueError("El salario no puede ser inferior al mínimo legal.")

emp = Empleado("Carlos Gómez", 2000.0)
emp.salario = 2500.0                          # Usa el setter
print(emp.salario)                            # 2500.0