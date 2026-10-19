# atributos_clase_vs_instancia.py

class ConexionBaseDatos:
    total_conexiones = 0          # Atributo de CLASE

    def __init__(self, db_name: str):
        self.db_name = db_name    # Atributo de INSTANCIA
        ConexionBaseDatos.total_conexiones += 1

c1 = ConexionBaseDatos("Ventas")
c2 = ConexionBaseDatos("Inventario")

print(ConexionBaseDatos.total_conexiones)  # 2