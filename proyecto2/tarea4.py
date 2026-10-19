# ejemplo_polimorfismo_duck_typing.py

class NotificadorEmail:
    def enviar(self, mensaje: str):
        print(f"Enviando Email: {mensaje}")

class NotificadorSMS:
    def enviar(self, mensaje: str):
        print(f"Enviando SMS: {mensaje}")

# Función polimórfica: no le importa el tipo exacto
def notificar_alerta(notificador, texto: str):
    notificador.enviar(texto)

canal_1 = NotificadorEmail()
canal_2 = NotificadorSMS()

notificar_alerta(canal_1, "Fallo en servidor DB")
notificar_alerta(canal_2, "Fallo en servidor DB")