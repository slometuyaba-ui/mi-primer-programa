import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla y la cuadrícula
CELDA_TAM = 40
COLS, FILAS = 15, 13
ANCHO = COLS * CELDA_TAM
ALTO = FILAS * CELDA_TAM
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bomberman - Multijugador de Colores")

# Definir Colores (RGB)
NEGRO = (20, 20, 20)
GRIS_OSCURO = (60, 60, 60)
GRIS_CLARO = (120, 120, 120)
VERDE_FONDO = (34, 139, 34)
AZUL_J1 = (0, 191, 255)       # Jugador 1 (Cian brillante)
ROSA_J2 = (255, 20, 147)      # Jugador 2 (Magenta brillante)
NARANJA_BLOQUE = (210, 105, 30) # Bloques destructibles
AMARILLO_BOMBA = (255, 215, 0)
ROJO_EXPLOSION = (255, 69, 0)
BLANCO = (255, 255, 255)

# Mapa inicial (1: Muro indestructible, 2: Bloque destructible, 0: Vacío)
MAPA_INICIAL = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,2,2,2,2,2,2,2,2,2,0,0,1],
    [1,0,1,2,1,2,1,2,1,2,1,2,1,0,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,0,1,2,1,2,1,2,1,2,1,2,1,0,1],
    [1,0,0,2,2,2,2,2,2,2,2,2,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Jugador:
    def __init__(self, x, y, color, controles):
        self.x_inicio = x
        self.y_inicio = y
        self.color = color
        self.controles = controles
        self.reset()

    def reset(self):
        self.x = self.x_inicio
        self.y = self.y_inicio
        self.vivo = True

    def mover(self, dx, dy, mapa):
        nueva_x = self.x + dx
        nueva_y = self.y + dy
        # Comprobar colisión con los límites y muros/bloques
        if 0 <= nueva_x < COLS and 0 <= nueva_y < FILAS:
            if mapa[nueva_y][nueva_x] == 0:
                self.x = nueva_x
                self.y = nueva_y

    def dibujar(self, superficie):
        if self.vivo:
            centro = (self.x * CELDA_TAM + CELDA_TAM // 2, self.y * CELDA_TAM + CELDA_TAM // 2)
            pygame.draw.circle(superficie, self.color, centro, CELDA_TAM // 2 - 4)
            pygame.draw.circle(superficie, BLANCO, centro, 4)

class Bomba:
    def __init__(self, x, y, jugador):
        self.x = x
        self.y = y
        self.tiempo = pygame.time.get_ticks()
        self.duracion = 2000 # 2 segundos
        self.jugador = jugador

    def dibujar(self, superficie):
        centro = (self.x * CELDA_TAM + CELDA_TAM // 2, self.y * CELDA_TAM + CELDA_TAM // 2)
        pygame.draw.circle(superficie, AMARILLO_BOMBA, centro, CELDA_TAM // 3)

# Configuración inicial del estado del juego
j1 = Jugador(1, 1, AZUL_J1, {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izq': pygame.K_a, 'der': pygame.K_d, 'bomba': pygame.K_SPACE})
j2 = Jugador(COLS - 2, FILAS - 2, ROSA_J2, {'arriba': pygame.K_UP, 'abajo': pygame.K_DOWN, 'izq': pygame.K_LEFT, 'der': pygame.K_RIGHT, 'bomba': pygame.K_RETURN})

jugadores = [j1, j2]
mapa = [fila[:] for fila in MAPA_INICIAL]
bombas = []
explosiones = []

tiempo_fin_juego = None # Marca de tiempo cuando alguien muere para controlar la pausa de reinicio

reloj = pygame.time.Clock()

# Bucle principal del juego
while True:
    tiempo_actual = pygame.time.get_ticks()
    
    # 1. Gestión de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif evento.type == pygame.KEYDOWN and tiempo_fin_juego is None:
            for j in jugadores:
                if not j.vivo:
                    continue
                if evento.key == j.controles['arriba']:
                    j.mover(0, -1, mapa)
                elif evento.key == j.controles['abajo']:
                    j.mover(0, 1, mapa)
                elif evento.key == j.controles['izq']:
                    j.mover(-1, 0, mapa)
                elif evento.key == j.controles['der']:
                    j.mover(1, 0, mapa)
                elif evento.key == j.controles['bomba']:
                    # Colocar bomba si no hay otra en esa celda
                    if not any(b.x == j.x and b.y == j.y for b in bombas):
                        bombas.append(Bomba(j.x, j.y, j))

    # 2. Comprobar colisión directa entre jugadores en la misma casilla
    if j1.vivo and j2.vivo and j1.x == j2.x and j1.y == j2.y:
        j1.vivo = False
        j2.vivo = False
        explosiones.append((j1.x, j1.y, tiempo_actual))

    # 3. Actualizar Bombas y Explosiones
    nuevas_bombas = []
    for b in bombas:
        if tiempo_actual - b.tiempo >= b.duracion:
            # ¡La bomba explota!
            bx, by = b.x, b.y
            explosiones.append((bx, by, tiempo_actual))
            
            direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in direcciones:
                nx, ny = bx + dx, by + dy
                if 0 <= nx < COLS and 0 <= ny < FILAS:
                    if mapa[ny][nx] == 2:
                        mapa[ny][nx] = 0 # Destruir bloque destructible
                    elif mapa[ny][nx] == 0:
                        explosiones.append((nx, ny, tiempo_actual))
            
            # Comprobar si algún jugador está en la zona de explosión
            for j in jugadores:
                if (j.x == bx and j.y == by) or any((j.x == bx + dx and j.y == by + dy) for dx, dy in direcciones):
                    j.vivo = False
        else:
            nuevas_bombas.append(b)
    bombas = nuevas_bombas

    # Limpiar explosiones visuales después de 300 ms
    explosiones = [(x, y, t) for x, y, t in explosiones if tiempo_actual - t < 300]

    # 4. Dibujar Elementos en Pantalla
    PANTALLA.fill(VERDE_FONDO)

    # Dibujar el mapa
    for fila in range(FILAS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELDA_TAM, fila * CELDA_TAM, CELDA_TAM, CELDA_TAM)
            if mapa[fila][col] == 1:
                pygame.draw.rect(PANTALLA, GRIS_OSCURO, rect)
            elif mapa[fila][col] == 2:
                pygame.draw.rect(PANTALLA, NARANJA_BLOQUE, rect)
                pygame.draw.rect(PANTALLA, GRIS_CLARO, rect, 2)

    # Dibujar Explosiones
    for ex, ey, _ in explosiones:
        rect_ex = pygame.Rect(ex * CELDA_TAM, ey * CELDA_TAM, CELDA_TAM, CELDA_TAM)
        pygame.draw.rect(PANTALLA, ROJO_EXPLOSION, rect_ex)

    # Dibujar Bombas
    for b in bombas:
        b.dibujar(PANTALLA)

    # Dibujar Jugadores
    for j in jugadores:
        j.dibujar(PANTALLA)

    # 5. Control de Fin de Juego y Reinicio
    if not j1.vivo or not j2.vivo:
        if tiempo_fin_juego is None:
            tiempo_fin_juego = tiempo_actual # Registrar momento de fin de partida

        fuente = pygame.font.SysFont(None, 48)
        texto = "¡Empate!" if not j1.vivo and not j2.vivo else ("¡Jugador 2 (Rosa) Gana!" if not j1.vivo else "¡Jugador 1 (Cian) Gana!")
        img_texto = fuente.render(texto, True, BLANCO)
        PANTALLA.blit(img_texto, (ANCHO // 2 - img_texto.get_width() // 2, ALTO // 2 - img_texto.get_height() // 2))

        # Esperar 2 segundos (2000 ms) mostrando el resultado antes de reiniciar
        if tiempo_actual - tiempo_fin_juego >= 2000:
            mapa = [fila[:] for fila in MAPA_INICIAL]
            bombas.clear()
            explosiones.clear()
            for j in jugadores:
                j.reset()
            tiempo_fin_juego = None

    pygame.display.flip()
    reloj.tick(30)
