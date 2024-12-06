import pygame
from constantes import *
from imagenes import *
from funciones import mostrar_mensaje, cargar_imagen


def dibujar_ranking(estado_juego:dict)->None:
    """
    Esta función se encarga de dibujar en pantalla el ranking de top 5, tomado de
    el diccionario del estado de juego, el cual lee el json. Previa ejecucion de esta
    funcion se ordena en el main de mayor a menor.
    Recibe: el diccionario del estado de juego
    Retorna:  None.
    """
    x = 380
    y = 250
    for i in range(len(estado_juego['ranking'])):
        if i == 5:
            break
        # "i" vale 0 en la primera iteración pero necesitamos dibujar el puesto 1:
        top = i + 1
        if top == 1:
            color = ORO
        elif top == 2:
            color = PLATA
        elif top == 3:
            color = BRONCE
        else:
            if estado_juego['dark_mode'] == True:
                color = BLANCO
            elif estado_juego['dark_mode'] == False:
                color = NEGRO
        nombre = OCHO_BITS_MEDIUM.render(estado_juego['ranking'][i]['user'], True, color)
        puntos = OCHO_BITS_MEDIUM.render(str(estado_juego['ranking'][i]['points']), True, color)
        top_texto = OCHO_BITS_MEDIUM.render(str(top), True, color)
        
        # Se dibuja el puesto en una determinada coordenada 
        estado_juego['pantalla'].blit(top_texto, (x, y))
        # Se dibuja el nombre en la misma coordenada pero corriendo hacia la derecha
        estado_juego['pantalla'].blit(nombre, (x + 100, y))
        # Se dibujan sus puntos en la misma coordenada pero corriendo mas hacia la derecha
        estado_juego['pantalla'].blit(puntos, (x + 400, y))
        # Se baja la coordenada y para que la proxima iteracion se dibuje abajo
        y += 80


def pantalla_win(estado_juego:dict)->None:
    """
    Esta función dibuja win cuando el jugador gana la partida. Muestra los
    mensajes correspondientes.
    Recibe: el diccionario del estado de juego
    Retorna: None.
    """
    estado_juego['pantalla'].blit(cargar_imagen("img/win_background.jpg"), (0, 0))
    estado_juego['pantalla'].blit(cargar_imagen('img/win.webp', (400, 300)), (480, 10))
    
    for elemento in DICCIONARIO_IMAGENES:
        if elemento['nombre'] == "volver_white":
            estado_juego['pantalla'].blit(elemento["surface"], (elemento["posicion_x"], elemento["posicion_y"]))
    
    mostrar_mensaje(f"Felicidades  {estado_juego['user']}  por completar el Sudoku", estado_juego['pantalla'], (670, 315), COLOR_BOTON, OCHO_BITS_MEDIUM)
    mostrar_mensaje(f"Tardaste  {estado_juego['tiempo']}", estado_juego['pantalla'], (670, 370), BLANCO, OCHO_BITS_MEDIUM)
    mostrar_mensaje(f"Hiciste  {estado_juego['puntaje']}  puntos", estado_juego['pantalla'], (670, 420), BLANCO, OCHO_BITS_MEDIUM)
    if estado_juego['errores'] > 0:
        if estado_juego['errores'] == 1:
            mostrar_mensaje(f"Tuviste  un  error", estado_juego['pantalla'], (670, 470), ROJO, OCHO_BITS_MEDIUM)
        else:
            mostrar_mensaje(f"Tuviste  {estado_juego['errores']}  errores", estado_juego['pantalla'], (670, 470), ROJO, OCHO_BITS_MEDIUM)
    else:
        mostrar_mensaje(f"No tuviste errores", estado_juego['pantalla'], (670, 470), BLANCO, OCHO_BITS_MEDIUM)
    
    
def dibujar_input(estado_juego:dict)->None:
    """
    Esta función dibuja la casilla de nombre del jugador
    Recibe: el diccionario del estado de juego.
    Retorna: None.
    """
    text_surface = UBUNTU_LIGHT.render(estado_juego['user'], True, BLANCO)
    color = BLANCO if estado_juego['dark_mode'] else NEGRO
    mostrar_mensaje("Nombre  de  usuario", estado_juego['pantalla'], (670, 300), color, ARCADE_CLASSIC_SMALL)
    
    # Verificar si se puso el puntero dentro del área de la casilla:
    if INPUT_RECT.collidepoint(pygame.mouse.get_pos()):
        # Cambiar el color de la casilla:
        #   INPUT_SELECCION: color, INPUT_RECT: coordenadas y dimensiones 
        pygame.draw.rect(estado_juego['pantalla'], INPUT_SELECCION, INPUT_RECT, border_radius=10)
    else:
        # Dibujar la casilla de nombre:
        pygame.draw.rect(estado_juego['pantalla'], INPUT_COLOR, INPUT_RECT, border_radius=10)
        
        
    if estado_juego['activo_input'] == True:
        pygame.draw.rect(estado_juego['pantalla'], INPUT_ACTIVO, INPUT_RECT, border_radius=10)  
    
    
    estado_juego['pantalla'].blit(text_surface, (INPUT_RECT.x + 10, INPUT_RECT.y + 10)) 


def pantalla_menu(estado_juego:dict)->None:
    """
    Esta función se encarga de dibujar la pantalla del menú.
    Recibe: el diccionario del estado de juego.
    Retorna: None.
    """
    if estado_juego['dark_mode'] == True:
        estado_juego['pantalla'].blit(cargar_imagen("img/fondo.jpeg", (1280, 720)), (0, 0))
    elif estado_juego['dark_mode'] == False:
        estado_juego['pantalla'].blit(cargar_imagen("img/fondo_claro.jpg", (1280, 720)), (0, 0))
    estado_juego['pantalla'].blit(cargar_imagen("img/logo.png", (600, 200)), (350, 40))
    dibujar_botones_menu(estado_juego['pantalla'], ARCADE_CLASSIC_SMALL, OPCIONES_MENU)


def dibujar_botones_menu(pantalla:object, fuente:object, diccionario:list[dict])->None:
    """
    Esta funcion se encarga de dibujar los botones en el menu.
    Recibe: pantalla: Pantalla inicializada en Pygame a la que se dibujara.
            fuente: Fuente que tendran los textos de los botones
            diccionario: Los nombres y coordenadas de cada boton
    Retorna: None
    """
    for opcion in diccionario:
        x, y = opcion["posicion"]
        texto = fuente.render(opcion["texto"], True, BLANCO)
        # Centramos el rectangulo del texto en el centro del boton
        texto_rect = texto.get_rect(center=(x + ANCHO_BOTON // 2, y + ALTO_BOTON // 2))
        boton_rect = pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON)
        if boton_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla, COLOR_BOTON_SELECCION, boton_rect, border_radius=RADIO_BOTON)
        else:
            pygame.draw.rect(pantalla, COLOR_BOTON, boton_rect, border_radius=RADIO_BOTON)
        pantalla.blit(texto, texto_rect.topleft)


def pantalla_juego(estado_juego:dict)->None:
    """
    Esta funcion se encarga de dibujar la pantalla del juego.
    Recibe: estado_juego(dict): Diccionario con todos los elementos importantes del juego.
    Retorna: None
    """
    
    if estado_juego['dark_mode'] == True:
        estado_juego['pantalla'].blit(cargar_imagen("img/ingame.jpg"), (0, 0))
        color = BLANCO
    elif estado_juego['dark_mode'] == False:
        estado_juego['pantalla'].blit(cargar_imagen("img/ingame_claro.webp"), (0, 0))
        color = NEGRO
    errores = str(estado_juego['errores'])
    texto_puntaje = f"Score: {str(estado_juego['puntaje'])}"
    if estado_juego['puntaje'] < 0:
        estado_juego['puntaje'] = 0
    texto_puntaje = UBUNTU_LIGHT.render(texto_puntaje, True, color)
    
    
    dibujar_temporizador(estado_juego)
    dibujar_tablero(estado_juego)
    
    errores = UBUNTU_LIGHT.render(errores, True, color)
    
    for elemento in DICCIONARIO_IMAGENES:
        # Ignoro las imagenes config ya que estoy en la pantalla de juego:
        if elemento['nombre'] == "volver_config" or elemento['nombre'] == "volver_white_config":
            continue
        if estado_juego['dark_mode'] == False:
            # Ignoro las imagenes white, ya que estoy en Modo Claro:
            if elemento['nombre'] == "volver_white" or elemento['nombre'] == "reset_white":
                continue
            estado_juego['pantalla'].blit(elemento["surface"], (elemento["posicion_x"], elemento["posicion_y"]))
        elif estado_juego['dark_mode'] == True:
            # Ignoro las imagenes normales, para tomar las white ya que estoy en dark_mode:
            if elemento['nombre'] == "volver" or elemento['nombre'] == "reset":
                continue
            estado_juego['pantalla'].blit(elemento["surface"], (elemento["posicion_x"], elemento["posicion_y"]))
    
    estado_juego['pantalla'].blit(errores, (580, 42))
    estado_juego['pantalla'].blit(texto_puntaje, (780, 42))
    

def pantalla_puntajes(estado_juego:dict)->None:
    """
    Esta funcion se encarga de dibujar la pantalla de puntajes.
    Recibe: estado_juego(dict): Diccionario con todos los elementos importantes del juego.
    Retorna: None
    """
    
    if estado_juego['dark_mode'] == True:
        estado_juego['pantalla'].blit(cargar_imagen("img/fondo.jpeg", (1280, 720)), (0, 0))
    elif estado_juego['dark_mode'] == False:
        estado_juego['pantalla'].blit(cargar_imagen("img/fondo_claro.jpg", (1280, 720)), (0, 0))
    estado_juego['pantalla'].blit(cargar_imagen("img/logo.png", (600, 200)), (350, 40))
    
    dibujar_ranking(estado_juego)
    
    for elemento in DICCIONARIO_IMAGENES:
        if elemento['nombre'] == "volver_white" and estado_juego['dark_mode'] == True:
            estado_juego['pantalla'].blit(elemento["surface"], (elemento["posicion_x"], elemento["posicion_y"]))
        elif elemento['nombre'] == "volver" and estado_juego['dark_mode'] == False:
            estado_juego['pantalla'].blit(elemento["surface"], (elemento["posicion_x"], elemento["posicion_y"]))


def pantalla_configuracion(estado_juego:dict)->None:
    """
    Esta funcion se encarga de dibujar la pantalla de puntajes.
    Recibe: estado_juego(dict): Diccionario con todos los elementos importantes del juego.
    Retorna: None
    """
    
    if estado_juego['dark_mode'] == True:
        estado_juego['pantalla'].blit(cargar_imagen("img/fondo.jpeg", (1280, 720)), (0, 0))
    elif estado_juego['dark_mode'] == False:
        estado_juego['pantalla'].blit(cargar_imagen("img/fondo_claro.jpg", (1280, 720)), (0, 0))
    estado_juego['pantalla'].blit(cargar_imagen("img/logo.png", (600, 200)), (350, 40))
    estado_juego['pantalla'].blit(cargar_imagen("img/config.webp", (330, 330)), (510, 350))
    
    dibujar_input(estado_juego)
    dibujar_botones_menu(estado_juego['pantalla'], ARCADE_CLASSIC_SMALL, OPCIONES_CONFIG)
    if estado_juego['error_input'] == True:
        mostrar_mensaje("El nombre debe tener entre 3 y 15 caracteres", estado_juego['pantalla'], (1050, 350), "red", UBUNTU_LIGHT_SMALL)
    
    for elemento in DICCIONARIO_IMAGENES:
        if elemento['nombre'] == "volver_white_config" and estado_juego['dark_mode'] == True:
            estado_juego['pantalla'].blit(elemento["surface"], (elemento["posicion_x"], elemento["posicion_y"]))
        elif elemento['nombre'] == "volver_config" and estado_juego['dark_mode'] == False:
            estado_juego['pantalla'].blit(elemento["surface"], (elemento["posicion_x"], elemento["posicion_y"]))
    

def dibujar_tablero(estado_juego:dict)->None:
    """
    Esta funcion se encarga de dibujar el tablero del sudoku durante la pantalla del juego.
    Recibe: estado_juego(dict): Diccionario con todos los datos importantes del juego.
    Retorna: None
    """
    
    # Identificar la fila, columna y submatriz 3x3 de la celda seleccionada
    fila_sel = None
    columna_sel = None  # Valores predeterminados
    fila_base = None
    columna_base = None

    if estado_juego['celda_seleccionada']:
        fila_sel, columna_sel = estado_juego['celda_seleccionada']
        fila_base = (fila_sel // 3) * 3
        columna_base = (columna_sel // 3) * 3
    
    for i in range(9):
        for j in range(9):
            # Obtener el valor de la celda actual
            value = estado_juego['sudoku'][i][j]
            
            # Colores de Texto
            # Determinar el color del texto según el estado de la celda
            if (i, j) in estado_juego['celdas_errores']:
                color_texto = CELDA_ERROR  # Color para errores
            elif (i, j) in estado_juego['celdas_aciertos']:
                color_texto = COLOR_CORRECTO  # Color para aciertos
            else:
                color_texto = NEGRO  # Color por defecto
            
            numero = SYSFONT_MEDIUM.render(str(estado_juego['sudoku'][i][j]), True, color_texto)
            
            # Colores de Celda
            if estado_juego['celda_seleccionada'] == (i, j):
                color = CELDA_SELECCIONADA
            elif (i, j) in estado_juego['colores_celdas']:
                color = estado_juego['colores_celdas'][(i, j)]
            elif fila_sel != None and (i == fila_sel or j == columna_sel):
                color = SOMBREADO_FILA_COLUMNA
            elif fila_base != None and fila_base <= i < fila_base + 3 and columna_base <= j < columna_base + 3:
                color = SOMBREADO_SUBMATRIZ
            elif (i, j) in estado_juego['celdas_bloqueadas']:
                color = CELDA_RESUELTA
            else:
                color = CELDA_VACIA

                
            # Dibuja rectangulo de cada celda con color de fondo:       X                   Y                 ANCHO     ALTO
            pygame.draw.rect(estado_juego['pantalla'], color, (j * CELDA_SIZE + 400, i * CELDA_SIZE + 100, CELDA_SIZE, CELDA_SIZE))
            # lista_coordenadas.append((j * celda_size + 400, i * celda_size + 100, celda_size, celda_size))
            # Borde para cada celda:                                         X                       Y               ANCHO       ALTO       1:QUITAR EL FONDO
            pygame.draw.rect(estado_juego['pantalla'], LINEAS_CELDAS, (j * CELDA_SIZE + 400, i * CELDA_SIZE + 100, CELDA_SIZE, CELDA_SIZE), 1)
            
            if value != " ":
            # Dibujar cada numero que figure en el sudoku siguiendo la misma logica que 
            # recien pero sumandole un poco mas a las coordenadas para que quede centrado en la celda
            #                                                      X                   Y                                            
                estado_juego['pantalla'].blit(numero, (j * CELDA_SIZE + 425, i * CELDA_SIZE + 120))
                
    for elemento in LINEAS_TABLERO:
        x1, y1, x2, y2 = elemento
        # Lineas que marcan los cuadrantes de 3x3:
        pygame.draw.line(estado_juego['pantalla'], LINEAS_EXTERNAS, (x1, y1), (x2, y2), 3)
    # Rectangulo del tablero:
    pygame.draw.rect(estado_juego['pantalla'], LINEAS_EXTERNAS, (400, 100, 545, 545), 5)
    # print(lista_coordenadas)   
    
    
def dibujar_temporizador(estado_juego:dict)->None:
    """
    Esta funcion se encarga de dibujar el cronometro durante la pantalla del juego
    Recibe: estado_juego(dict): Diccionario con todos los datos importantes del juego.
    No tiene retorno
    """
    
    if estado_juego['dark_mode'] == True:
        color = BLANCO
    elif estado_juego['dark_mode'] == False:
        color = NEGRO
    
    fuente = pygame.font.SysFont(None, 50)
    texto = fuente.render(estado_juego['tiempo'], True, color)
    estado_juego['pantalla'].blit(texto, (100, 100))