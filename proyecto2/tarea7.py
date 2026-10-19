# ejercicio_resuelto_1.py

class Vehiculo:
    def __init__(self, marca: str, modelo: str):
        self._marca = marca
        self._modelo = modelo

    def obtener_info(self) -> str:
        return f"Vehículo: {self._marca} {self._modelo}"

class AutoElectrico(Vehiculo):
    def __init__(self, marca: str, modelo: str, bateria_kwh: float):
        super().__init__(marca, modelo)
        self._bateria = bateria_kwh
        self._carga_actual = 20.0             # % inicial

    def cargar_bateria(self, porcentaje: float):
        if 0 <= porcentaje <= (100 - self._carga_actual):
            self._carga_actual += porcentaje
            print(f"Carga exitosa. Batería al {self._carga_actual}%")
        else:
            print("Error: Excede el límite de carga (100%).")

# Prueba
tesla = AutoElectrico("Tesla", "Model 3", 75.0)
print(tesla.obtener_info())
tesla.cargar_bateria(50.0)
# Salida: Carga exitosa. Batería al 70.0%



# Orientación de solución

class Estudiante:
    def __init__(self, nombre: str):
        self.__nombre = nombre
        self.__notas = []

    def agregar_nota(self, nota: float):
        if 0 <= nota <= 5.0:
            self.__notas.append(nota)
        else:
            print("Nota inválida")

    @property
    def notas(self):
        return self.__notas.copy()            # Evita mutación externa

    def promedio(self) -> float:
        return sum(self.__notas) / len(self.__notas) if self.__notas else 0.0