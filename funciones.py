import pygame
import json
from constantes import *
from logica_sudoku import *


def cargar_imagen(ruta:str, dimensiones:int|None = None)->object:
    """
    Esta funcion se encarga de cargar una imagen.
    Recibe: ruta del archivo. Dimensiones que queramos darle opcionalmente.
    Retorna: La imagen cargada con pygame.
    """
    imagen = pygame.image.load(ruta)
    if dimensiones != None:
        imagen = pygame.transform.scale(imagen, dimensiones)
    return imagen



def limpiar_lista_tuplas(lista_tuplas:list[tuple], fila:int, columna:int)->None:
    """
    Elimina todas las tuplas de la lista que sean iguales a la tupla (fila, columna).
    Recibe: lista_tuplas(list[tuple]): Lista de tuplas a limpiar.
            fila(int): El valor de la fila que se buscara en las tuplas
            columna(int): El valor de la columna que se buscará en las tuplas
    No tiene retorno.
    """
    # Recorremos la lista de forma invertida para evitar problemas con las posiciones
    for i in range(len(lista_tuplas) - 1, -1, -1):
        f, c = lista_tuplas[i]
        if (f, c) == (fila, columna):
            lista_tuplas.pop(i)


def validar_colisiones_menu(coordenadas:tuple, opciones:dict, estado:str)->str:
    """
    Esta funcion se encarga de validar las colisiones de los botones del menu. Cuando se pulse un boton cambia el estado del juego.
    Recibe: coordenadas(tupla): coordenadas donde se hace click
            opciones(list[dict]): Opciones para cada boton.
            estado(str): Estado del juego
    Retorna: estado(str): Estado del juego
    """
    x, y = coordenadas
    for opcion in opciones:
        texto_rect = pygame.Rect(opcion["posicion"][0], opcion["posicion"][1], ANCHO_BOTON, ALTO_BOTON)
        if texto_rect.collidepoint(x, y):
            if opcion["texto"] == "Jugar":
                estado = "jugar"
            elif opcion["texto"] == "Puntajes":
                estado = "puntajes"
            elif opcion["texto"] == "Configuracion":
                estado = "configuracion"
            elif opcion["texto"] == "Salir":
                pygame.quit()
                quit()
    return estado

def validar_colisiones_configuraciones(evento, opciones:list[dict], estado_juego:dict)->None:
    """
    Esta funcion se encarga de validar las colisiones de los botones de la configuracion.
    Recibe: evento: Evento al que se le recuperaran las coordenadas
            opciones(list[dict]): Todas las opciones de los botones de la configuracion
            estado_juego(dict): Diccionario con los datos del juego
    No tiene retorno
    """
    x, y = evento.pos
    for opcion in opciones:
        texto_rect = pygame.Rect(opcion["posicion"][0], opcion["posicion"][1], ANCHO_BOTON, ALTO_BOTON)
        if texto_rect.collidepoint(x, y):
            if opcion['btn'] == 1: 
                if estado_juego['dificultad'] == 'facil':
                    estado_juego['dificultad'] = "intermedio"
                    estado_juego['porcentaje_dif'] = 0.4
                    opcion["texto"] = f"Dificultad  {DIFICULTADES[1]}"
                elif estado_juego['dificultad'] == 'intermedio':
                    estado_juego['dificultad'] = 'dificil'
                    estado_juego['porcentaje_dif'] = 0.6
                    opcion["texto"] = f"Dificultad  {DIFICULTADES[2]}"
                elif estado_juego['dificultad'] == 'dificil':
                    opcion["texto"] = f"Dificultad  {DIFICULTADES[0]}"
                    estado_juego['dificultad'] = 'facil'
                    estado_juego['porcentaje_dif'] = 0.2
                if estado_juego['sudoku'] != None:
                    resetear_juego(estado_juego)
            elif opcion['btn'] == 2:
                if estado_juego['musica'] == False:
                    opcion['texto'] = f"Musica  {SI_NO[0]}"
                    estado_juego['musica'] = True
                    if estado_juego['musica_actual']:
                        estado_juego['musica_actual'].play(-1)
                elif estado_juego['musica'] == True:
                    opcion['texto'] = f"Musica  {SI_NO[1]}"
                    estado_juego['musica'] = False
                    if estado_juego["musica_actual"]:
                        estado_juego['musica_actual'].stop()
            elif opcion['btn'] == 3:
                if estado_juego['sonidos'] == False:
                    opcion['texto'] = f"Sonido  {SI_NO[0]}"
                    estado_juego['sonidos'] = True
                elif estado_juego['sonidos'] == True:
                    opcion['texto'] = f"Sonido  {SI_NO[1]}"
                    estado_juego['sonidos'] = False
            elif opcion['btn'] == 4:
                if estado_juego['dark_mode'] == True:
                    opcion["texto"] = f"Modo oscuro  {SI_NO[1]}"
                    estado_juego['dark_mode'] = False
                elif estado_juego['dark_mode'] == False:
                    opcion["texto"] = f"Modo oscuro  {SI_NO[0]}"
                    estado_juego['dark_mode'] = True

def calcular_tiempo_jugado(segundos:int, minutos:int, estado_juego:dict)->tuple:
    """
    Esta funcion se encarga de calcular el tiempo que lleva transcurrido el juego.
    Recibe segundos y minutos inicializados en 0.
    Retorna: Una tupla.
    La tupla contiene: cadena(str): Cadena formateada en minutos y segundos.
                       segundos(int): Segundos actual
                       minutos(int): Minutos actual
    """
    segundos += 1
    if segundos >= 60:
        minutos += 1
        segundos = 0
        estado_juego['puntaje'] -= PENALIZACION_POR_TIEMPO
    if minutos < 10:
        cadena_minutos = "0" + str(minutos)
    else:
        cadena_minutos = str(minutos)
    if segundos < 10:
        cadena_segundos = "0" + str(segundos)
    else:
        cadena_segundos = str(segundos)
    cadena = cadena_minutos + ":" + cadena_segundos
    return cadena, segundos, minutos
    
def detectar_click(estado_juego, evento):
    """
    Detecta el clic del usuario y actualiza la celda seleccionada en el estado del juego.
    """
    CELDA_SIZE = 60
    tablero_x = 400
    tablero_y = 100

    if evento.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = evento.pos

        # Verificar si el clic está dentro del tablero
        if (tablero_x <= mouse_x and mouse_x <= (tablero_x + 9 * CELDA_SIZE)) and (tablero_y <= mouse_y and mouse_y <= (tablero_y + 9 * CELDA_SIZE)):
            # Calcular las coordenadas de la celda
            columna = (mouse_x - tablero_x) // CELDA_SIZE
            fila = (mouse_y - tablero_y) // CELDA_SIZE
            estado_juego['celda_seleccionada'] = (fila, columna)
        else:
            # Si el clic está fuera del tablero, deseleccionar
            estado_juego['celda_seleccionada'] = None
            
def ingresar_numero(estado_juego:dict, evento)->None:
    """
    Esta función permite al usuario ingresar un número en la celda seleccionada.
    Recibe: el diccionario de estado de juego, el evento actual
    Retorna: None
    """
    # Si ninguna celda es clickeada o se clickea en otro lado 'celda_seleccionada' está en None.
    if estado_juego['celda_seleccionada']:
        fila, columna = estado_juego['celda_seleccionada']
        
        # Verificar si el evento corresponde a un número del 1 al 9
        if (fila, columna) not in estado_juego['celdas_bloqueadas']:
            if evento.unicode.isdigit() and (1 <= int(evento.unicode) and int(evento.unicode) <= 9):
                numero_ingresado = int(evento.unicode)
                # Compara el numero ingresado en esa posicion con la matriz solucion
                # Si es correcto:
                if numero_ingresado == estado_juego['solucion'][fila][columna]:
                    if (fila, columna) in estado_juego['celdas_errores']:
                        limpiar_lista_tuplas(estado_juego['celdas_errores'], fila, columna)
                        estado_juego['colores_celdas'].pop((fila, columna), None)
                    estado_juego['sudoku'][fila][columna] = numero_ingresado
                    estado_juego['puntaje'] += BONIFICACION_POR_ACIERTO
                    estado_juego['celdas_bloqueadas'].append((fila, columna))
                    estado_juego['celdas_aciertos'].append((fila, columna))
                    if estado_juego['sonidos'] == True:
                        SONIDO_CORRECTO.play()
                # Si es incorrecto:
                else:
                    estado_juego['sudoku'][fila][columna] = numero_ingresado
                    estado_juego['colores_celdas'][(fila, columna)] = COLOR_ERROR
                    estado_juego['errores'] += 1
                    estado_juego['puntaje'] -= PENALIZACION_POR_ERRORES
                    estado_juego['celdas_errores'].append((fila, columna))
            elif evento.key == pygame.K_BACKSPACE or pygame.K_DELETE:
                estado_juego['sudoku'][fila][columna] = " "  # Borrar el contenido de la celda
                estado_juego['colores_celdas'].pop((fila, columna), None)

def inicializar_celdas_bloqueadas(tablero:list)->list:
    """
    Esta funcion detecta las celdas que tienen valores prellenados (no vacías) y las marca como bloqueadas.
    Recibe: La copia de la matriz solución que tiene las celdas "ocultas"/prellenadas
    Retorna: Una lista de tuplas. Donde cada tupla es una coordenada (fila, columna) de una celda no prellenada. 
    """
    celdas_bloqueadas = []
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] != " ":  # Si la celda tiene un valor, está bloqueada
                celdas_bloqueadas.append((fila, columna))
    return celdas_bloqueadas

def mostrar_mensaje(mensaje:str, pantalla:object, coordenadas:tuple, color:str|tuple, fuente:object):
    """
    Esta función muestra un mensaje en pantalla.
    Recibe: el mensaje a mostrar, la pantalla, donde se debe ubicar el mensaje,
    el color que tendrá, la fuente.
    Retorna: None.
    """
    texto = fuente.render(mensaje, True, color) 
    texto_rect = texto.get_rect(center=coordenadas)
    pantalla.blit(texto, texto_rect)

def poner_musica(ruta, volumen, loops):
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(loops)
    
def validar_musica(musica_actual, musica_a_validar):
    if musica_actual != musica_a_validar:
            if musica_actual != None:
                musica_actual.stop()
            musica_a_validar.play(-1)
            musica_actual = musica_a_validar
    return musica_actual

def calcular_dificultad(estado_juego:dict)->int:
    """
    Esta función segun la dificultad seleccionada, setea la bonificacion
    correspondiente e incrementa el puntaje del jugador.
    Recibe: el diccionario del estado del juego.
    Retorna: El puntaje del jugador incrementado segun la dificultad.
    """
    if estado_juego['dificultad'] == "facil":
        dificultad = BONIFICACION_DIFICULTAD_FACIL
    elif estado_juego['dificultad'] == "intermedio":
        dificultad = BONIFICACION_DIFICULTAD_MEDIA
    elif estado_juego['dificultad'] == "dificil":
        dificultad = BONIFICACION_DIFICULTAD_DIFICIL
        
    return int(estado_juego['puntaje'] * dificultad)

def ordenar_ranking(lista_ranking:list[dict])->None:
    """
    Esta función se encarga de ordenar la lista de jugadores desde el jugador
    con mayor puntaje hasta el jugador con menor puntaje a traves de un
    ordenamiento por burbujeo.
    Recibe: la lista de diccionarios donde cada diccionario es un jugador.
    Retorna: None.
    """
    for i in range(len(lista_ranking) - 1):
        for j in range(i + 1, len(lista_ranking)):
            if lista_ranking[i]['points'] < lista_ranking[j]['points']:  
                aux = lista_ranking[j]
                lista_ranking[j] = lista_ranking[i]
                lista_ranking[i] = aux

def leer_json(ruta:str)->list[dict]:
    """
    Esta función lee el archivo .json y guarda su contenido
    Recibe: una ruta al archivo
    Retorna: el json convertido a tipo de dato que puede manejar python
    """
    with open(ruta, "r") as archivo:
        data = json.load(archivo)
    return data

def escribir_json(ruta:str, estado_juego:dict)->None:
    """
    Esta funcion se encarga de escribir en un archivo json los datos de cada partida. 
    Recibe: ruta(str): Directorio donde se escribira el archivo
            estado_juego(dict): Diccionario con todos los elementos del juego.
    Esta funcion no tiene retorno.
    """
    data_user = {
        "user": estado_juego['user'],
        "points": estado_juego['puntaje'],
        "minutos": estado_juego['minutos'],
        "errores": estado_juego['errores']
    }
    
    agregar_usuario(estado_juego['ranking'], data_user)
    
    with open(ruta, "w") as archivo:
        json.dump(estado_juego['ranking'], archivo, indent=4)
        
def agregar_usuario(ranking:list, data_user:dict)->None:
    """
    Esta funcion se encarga de agregar un usuario al diccionario del ranking validando que ya no haya un usuario con ese nombre.
    En caso de que existe ese usuario, quedara el usuario con mayor puntaje.
    Recibe: ranking(list): Lista de diccionarios de cada partida
            data_user(dict): Diccionario de la partida a agregar
    Esta funcion no tiene retorno
    """
    se_encontro_user = False
    for i in range(len(ranking)):
        if ranking[i]['user'] == data_user['user']:
            ranking[i]['points'] = data_user['points']
            ranking[i]['minutos'] = data_user['minutos']
            ranking[i]['errores'] = data_user['errores']
            se_encontro_user = True
        
    if se_encontro_user != True:
        ranking.append(data_user)

def resetear_juego(estado_juego):
    """
    Esta funcion se encarga de resetear todo el juego, incluyendo tablero, puntaje, dificultad, tiempo, y estilos visuales.
    Recibe: estado_juego(dict): Diccionario con todos los datos del juego.
    No tiene retorno.
    """
    estado_juego['tablero_armado'] = False
    estado_juego['puntaje'] = PUNTAJE_BASE
    estado_juego['dificultad_calculada'] = False
    estado_juego['puntos_calculados'] = False
    estado_juego['colores_celdas'] = {}
    estado_juego['errores'] = 0
    estado_juego['tiempo'], estado_juego['segundos'], estado_juego['minutos'] = "", 0, 0
    estado_juego['celdas_bloqueadas'] = inicializar_celdas_bloqueadas(estado_juego['sudoku'])
    estado_juego['celdas_errores'] = []
    estado_juego['celdas_aciertos'] = []
