import random
import copy

def inicializar_matriz(cant_filas:int, cant_columnas:int, valor_inicial:any)->list[list[any]]:
    """
    Esta función se encarga de inicializar una matriz con un valor inicial.
    Recibe: cant_filas(int): Cantidad de filas que va a tener la matriz
            cant_columnas(int): Cantidad de columnas que va a tener la matriz
            valor_inicial(any): Dato con el que se va a inicializar la matriz
    Retorna: matriz(list[list[any]]): Matriz con las dimensiones creada con los datos cargados como valor inicial. 
    """
    matriz = []
    for _ in range(cant_filas):
        fila = [valor_inicial] * cant_columnas
        matriz += [fila]
    return matriz

def mostrar_sudoku(matriz:list[list])->None:
    """
    Esta funcion se encarga de imprimir en consola la cuadricula del sudoku.
    Recibe: matriz(list[list])
    No retorna nada.
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if j == 3 or j == 6:
                print(" ", end=" ")  
            print(matriz[i][j], end=" ")
        if i == 2 or i == 5:
            print(" ")
        print("")

def generar_sudoku()->list[list[int]]:
    """
    Esta funcion se encarga de cargar una matriz 9x9 respetando las reglas del sudoku.
    Recibe: matriz(list[list]): Matriz inicializada a cargar
    Retorna: False si no encuentra numeros validos para cargar. 
            True si todas las celdas se llenaron.
    """
    # Creamos la matriz vacia
    matriz = inicializar_matriz(9, 9, 0)
    
    completo = False  
    while not completo:
        # Buscamos que al primer error volvamos a empezar
        completo = True  
        # Iteramos cada elemento de la matriz
        for fila in range(9):
            for columna in range(9):
                if matriz[fila][columna] == 0:  
                    # Creamos la lista con los numeros del sudoku (1 al 9)
                    numeros = list(range(1, 10))  
                    random.shuffle(numeros) # Mezclamos los elementos
                    colocado = False  
                    for numero in numeros: # Iteramos cada numero
                        if validar_numero_sudoku(matriz, numero, fila, columna):  
                            matriz[fila][columna] = numero
                            colocado = True
                            break  
                    if not colocado:  
                        completo = False  
                        break  # Rompemos el bucle que itera la matriz
        # Si hubo un error, limpiamos la matriz para volver a empezar
        if not completo:  
            for fila in range(9):
                for columna in range(9):
                    if matriz[fila][columna] != 0:
                        matriz[fila][columna] = 0
    return matriz  

def validar_numero_sudoku(matriz:list[list], numero:int, fila:int, columna:int)->bool:
    """
    Esta funcion se encarga de validar que el numero que se va a ingresar a una celda no se encuentre
    en la subcuadricula, ni en la misma fila, ni en la columna.
    Recibe: matriz(list[list]): Matriz a validar.
            numero(int): Numero a validar en la fila o columna.
            fila(int): Indice de la fila a validar.
            columna(int): Indice de la columna a validar
    Retorna: False si falla alguna de las validaciones.
            True si se valida correctamente.
    """
    valido = True 
    
    # Verificar numero en fila
    for i in range(9):
        if matriz[fila][i] == numero:
            valido = False
            break  
    
    # Verificar numero en columna
    if valido:  
        for j in range(9):
            if matriz[j][columna] == numero:
                valido = False
                break
    
    # Verificar numero en subcuadricula
    if valido:  
        # filas y columnas de los numeros que inician las subcuadriculas
                                    # 0, 1, 2
        subcuadricula_fila_inicio = (fila // 3) * 3          # 0, 3, 6
                                        # 0, 1, 2
        subcuadricula_columna_inicio = (columna // 3) * 3    # 0, 3, 6
        
        # Recorremos la subcuadricula 3x3 para validar si el numero ya se encuentra dentro de esta
        for i in range(3): 
            for j in range(3): 
                if matriz[subcuadricula_fila_inicio + i][subcuadricula_columna_inicio + j] == numero:
                    valido = False
                    break
            if not valido:  
                break
    
    return valido  

# ----------------------

def ocultar_celdas(matriz:list[list[int]], porcentaje_a_ocultar:float = 0.2)->list[list]:
    """
    Esta funcion se encarga de ocultar de forma aleatoria distintos elementos de una matriz creando una copia de esta.
    Recibe: matriz[list[list[any]]]: Matriz a copiar para esconderle celdas.
            porcentaje[float]: Por defecto 0.2. Porcentaje de celdas a ocultar.
    Retorna: copia_tablero[list[list[any]]]: Copia de la matriz con celdas ocultas.
    """
    copia_tablero = copy.deepcopy(matriz)
    
    cantidad_celdas_a_ocultar = int(81 * porcentaje_a_ocultar) 
    #cantidad_celdas_a_ocultar = 1
    for _ in range(cantidad_celdas_a_ocultar):
        fila = random.randint(0,8)
        columna = random.randint(0,8)
        # Si la posición generada ya hay un " " volvemos a generar otra posicion
        while copia_tablero[fila][columna] == " ":
            fila = random.randint(0,8)
            columna = random.randint(0,8)
        # Limpiamos la posicion
        copia_tablero[fila][columna] = " "
    return copia_tablero

def verificar_victoria(sudoku:list[list], solucion:list[list])->bool:
    """
    Esta funcion se encarga de verificar si se completo el sudoku de manera correcta.
    Recibe: sudoku(list[list]): Matriz 9x9 resuelta por el usuario.
            solucion(list[list]): solucion del sudoku.
    Retorna: True si el sudoku está bien.
             False mientras el sudoku este mal o este incompleto.
    """
    bandera = True
    for fila in range(9):
        for columna in range(9):
            # Si en algun momento no coinciden los elementos de ambas matrices finalizamos el bucle
            if sudoku[fila][columna] != solucion[fila][columna]:
                bandera = False
                break
    return bandera

