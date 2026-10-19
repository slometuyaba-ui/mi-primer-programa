# herencia_multiple_mro.py

class DispositivoConectado:
    def conectar(self):
        print("Estableciendo conexión a la red...")

class CamaraSeguridad:
    def grabar(self):
        print("Grabando video HD...")

class CamaraIP(DispositivoConectado, CamaraSeguridad):  # Herencia múltiple
    pass

cam = CamaraIP()
cam.conectar()
cam.grabar()

print(CamaraIP.mro())  # Orden de resolución de métodos