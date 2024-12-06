from constantes import *
from funciones import *
from imagenes import *
from logica_sudoku import *
from interfaces import *

pygame.init()

# Ventana
pantalla = pygame.display.set_mode(DIMENSIONES_PANTALLA)
pygame.display.set_caption("SUDOKU v1.0")
pygame.display.set_icon(sudoku_icon)

mi_evento_segundo = pygame.USEREVENT + 1
un_segundo = 1000
pygame.time.set_timer(mi_evento_segundo, un_segundo)

# Diccionario Global
estado_juego = {
    'pantalla': pantalla,
    'estado': "inicio",
    'dificultad': "facil",
    'dificultad_calculada': False,
    'porcentaje_dif': 0.2,
    'user': "Player",
    'activo_input': False,
    'error_input': False,
    'tablero_armado': False,
    'solucion': None,
    'sudoku':  None,
    'tiempo': "",
    'errores': 0,
    'segundos': 0,
    'minutos': 0,
    'puntaje': PUNTAJE_BASE,
    'puntos_calculados': False,
    'ranking': leer_json('datos.json'),
    'musica': True,
    'sonidos': True,
    'musica_actual': None,
    'dark_mode': True,
    'colores_celdas': {},
    'celda_seleccionada': None,
    'celdas_errores': [],
    'celdas_aciertos': [],
    'sonido_win': False,
}


while True:
    # Manejar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_juego['estado'] == "inicio":
                estado_juego['estado'] = validar_colisiones_menu(evento.pos, OPCIONES_MENU, estado_juego['estado'])
            # Volver a inicio desde jugar o puntajes:
            if (estado_juego['estado'] == "jugar" or estado_juego['estado'] == "puntajes") and volver_rect.collidepoint(pygame.mouse.get_pos()):
                estado_juego['estado'] = "inicio"
            # Volver a inicio desde configuración:
            if estado_juego['estado'] == "configuracion" and volver_white_config_rect.collidepoint(pygame.mouse.get_pos()):
                estado_juego['estado'] = "inicio"
            if estado_juego['estado'] == "jugar" and reset_rect.collidepoint(pygame.mouse.get_pos()):
                resetear_juego(estado_juego)
            if estado_juego['estado'] == "jugar":
                detectar_click(estado_juego, evento) # Cambia celda seleccionada
            if estado_juego['estado'] == "win":
                # Volver a inicio desde "win" (resetea el juego)
                if volver_rect.collidepoint(pygame.mouse.get_pos()):
                    estado_juego['estado'] = "inicio"
                    resetear_juego(estado_juego)
            if estado_juego['estado'] == 'configuracion':
                validar_colisiones_configuraciones(evento, OPCIONES_CONFIG, estado_juego)
        if evento.type == pygame.KEYDOWN:
            if estado_juego['estado'] == 'jugar':
                ingresar_numero(estado_juego, evento)
        if evento.type == mi_evento_segundo and estado_juego['estado'] == "jugar":
            estado_juego['tiempo'], estado_juego['segundos'], estado_juego['minutos'] = calcular_tiempo_jugado(estado_juego['segundos'], estado_juego['minutos'], estado_juego)
        # Escritura del nombre del jugador en configuracion:
        if estado_juego['estado'] == 'configuracion':
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Verificar si se hizo click en el input:
                if INPUT_RECT.collidepoint(evento.pos):
                    estado_juego['activo_input'] = True   # Permite al jugador escribir o no.
                    if estado_juego['user'] == "Player":
                            estado_juego['user'] = ""
            # Verificar si se tipeó algo luego de hacer click:
            elif evento.type == pygame.KEYDOWN:
                if estado_juego['activo_input']:
                    # Verifica si el jugador borro un caracter
                    if evento.key == pygame.K_BACKSPACE:
                        estado_juego['user'] = estado_juego['user'][:-1]
                    # Verifica si el jugador oprimió enter
                    elif evento.key == pygame.K_RETURN:
                        if 3 <= len(estado_juego['user']) <= 15 and estado_juego['user'].isalnum():
                            estado_juego['activo_input'] = False
                            estado_juego['error_input'] = False
                        else:
                            estado_juego['error_input'] = True
                            estado_juego['activo_input'] = False
                            estado_juego['user'] = "Player" 
                    # Verifica cualquier otra tecla tipeada
                    else:
                        if evento.unicode.isalnum() and len(estado_juego['user']) < 15:
                            estado_juego['user'] += evento.unicode
    
    # Actualizar estados
    if estado_juego['estado'] != "win":
        estado_juego['sonido_win_reproducido'] = False
    if estado_juego['estado'] != "configuracion":
        estado_juego['activo_input'] = False
        if estado_juego['user'] == "":
            estado_juego['user'] = "Player"
    if estado_juego['estado'] == "inicio":
        pantalla_menu(estado_juego)  
        if estado_juego['musica'] == True:
            estado_juego['musica_actual'] = validar_musica(estado_juego['musica_actual'], MUSICA_MENU)
        elif estado_juego['musica'] == False:
            estado_juego['musica_actual'].stop()
    elif estado_juego['estado'] == "jugar":
        if estado_juego['tablero_armado'] == False:
            solucion = generar_sudoku()
            sudoku = ocultar_celdas(solucion, estado_juego['porcentaje_dif'])
            estado_juego['solucion'] = solucion
            estado_juego['sudoku'] = sudoku
            estado_juego['celdas_bloqueadas'] = inicializar_celdas_bloqueadas(estado_juego['sudoku'])
            estado_juego['celda_seleccionada'] = None
            estado_juego['tablero_armado'] = True
        if estado_juego['dificultad_calculada'] == False:
            estado_juego['puntaje'] = calcular_dificultad(estado_juego)
            estado_juego['dificultad_calculada'] = True
        if estado_juego['musica'] == True:    
            estado_juego['musica_actual'] = validar_musica(estado_juego['musica_actual'], MUSICA_JUEGO)
        pantalla_juego(estado_juego)
    elif estado_juego['estado'] == "configuracion":
        pantalla_configuracion(estado_juego)
    elif estado_juego['estado'] == "puntajes":
        ordenar_ranking(estado_juego['ranking'])
        pantalla_puntajes(estado_juego)
    elif estado_juego['estado'] == 'win':
        if estado_juego['sonido_win'] == False and estado_juego['sonidos'] == True:
            SONIDO_WIN.play(0)
            estado_juego['sonido_win'] = True
        pantalla_win(estado_juego)
    if estado_juego['tablero_armado'] != False:
        if verificar_victoria(estado_juego['sudoku'], estado_juego['solucion']) and estado_juego['estado'] == "jugar":
            estado_juego['sonido_win'] = False
            estado_juego['estado'] = "win"
            if estado_juego['puntos_calculados'] == False:
                escribir_json('datos.json', estado_juego)
                estado_juego['puntos_calculados'] = True

    pygame.display.flip()