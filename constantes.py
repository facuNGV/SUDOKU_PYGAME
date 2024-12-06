import pygame

# CONFIGURACIONES
DIMENSIONES_PANTALLA = (1280, 720)
OPCIONES_MENU = [
    {"texto": "Jugar", "posicion": (520, 300)},
    {"texto": "Puntajes", "posicion": (520, 400)},
    {"texto": "Configuracion", "posicion": (520, 500)},
    {"texto": "Salir", "posicion": (520, 600)},
]

DIFICULTADES = ["Facil", "Normal", "Dificil"]
SI_NO = ["SI", "NO"]

OPCIONES_CONFIG = [
    {"btn": 1, "texto": f"Dificultad  {DIFICULTADES[0]}", "posicion": (200, 400)},
    {"btn": 2, "texto": f"Musica  {SI_NO[0]}", "posicion": (200, 500)},
    {"btn": 3, "texto": f"Sonido  {SI_NO[0]}", "posicion": (200, 600)},
    {"btn": 4, "texto": f"Modo oscuro  {SI_NO[0]}", "posicion": (850, 400)},
    {"btn": 5, "texto": f"Resolucion", "posicion": (850, 500)},
    {"btn": 6, "texto": f"Idioma", "posicion": (850, 600)},
]

# Coordenadas y dimensiones del tablero: (x:400, y:100, w:545, h:545)
LINEAS_TABLERO = [
    # x    y    W    H
    (580, 102, 580, 640),   # Primera Linea vertical
    (760, 103, 760, 640),   # Segunda linea vertical
    (403, 280, 940, 280),   # Primera linea horizontal
    (403, 460, 940, 460),   # Segunda linea horizontal
]

INPUT_RECT = pygame.Rect(520, 325, 300, 50)
CELDA_SIZE = 60

# BOTONES MENU
ANCHO_BOTON = 310
ALTO_BOTON = 70
RADIO_BOTON = 15

# COLORES
COLOR_FONDO = "#183b4a"
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
COLOR_SELECCION = (255, 0, 0)
COLOR_BOTON = "#3b65a3"
COLOR_BOTON_SELECCION = "#5382c9"

COLOR_CORRECTO = "#325aaf"
COLOR_ERROR = "#f7cfd6"
CELDA_ERROR = "#e55c6c"

INPUT_COLOR = "#03274d"
INPUT_SELECCION = "#032c57"
INPUT_ACTIVO = "#032040"

LINEAS_EXTERNAS = "#1c3742"
LINEAS_CELDAS = "#71828a"
# CELDA_RESUELTA = "#abb6ba"
CELDA_RESUELTA = "#ebedeb"
# CELDA_VACIA = "#c8d5db"
CELDA_VACIA = "#ffffff"
CELDA_SELECCIONADA = "#78bcf5"
SOMBREADO_SUBMATRIZ = "#BBDEFB"
SOMBREADO_FILA_COLUMNA = "#BBDEFB"

# MUSICA
pygame.mixer.init()
MUSICA_MENU = pygame.mixer.Sound("music/intro.mp3")
MUSICA_JUEGO = pygame.mixer.Sound("music/juego.mp3")

# PUNTAJE
PUNTAJE_BASE = 1000
PENALIZACION_POR_ERRORES = 7
PENALIZACION_POR_TIEMPO = 10
BONIFICACION_POR_ACIERTO = 5
BONIFICACION_DIFICULTAD_FACIL = 1.0
BONIFICACION_DIFICULTAD_MEDIA = 1.4
BONIFICACION_DIFICULTAD_DIFICIL = 2.0

# RANKING
ORO = "#e3ba24"
PLATA = "#969695"
BRONCE = "#6e5401"


# FUENTES

pygame.font.init()
OCHO_BITS_SMALL = pygame.font.Font("fonts/8bitoperator_jve.ttf", 32)
OCHO_BITS_MEDIUM = pygame.font.Font("fonts/8bitoperator_jve.ttf", 50)

ARCADE_CLASSIC_SMALL = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 30)

UBUNTU_LIGHT_SMALL = pygame.font.Font("fonts/Ubuntu-Light.TTF", 18)
UBUNTU_LIGHT = pygame.font.Font("fonts/Ubuntu-Light.TTF", 30)

SYSFONT_MEDIUM = pygame.font.SysFont(None, 40)
# SOUNDS

SONIDO_WIN = pygame.mixer.Sound("music/win.mp3")
SONIDO_CORRECTO = pygame.mixer.Sound("music/correcto.mp3")