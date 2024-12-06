import pygame
from funciones import *

reset = cargar_imagen("img/reset.webp", (80, 80))
volver = cargar_imagen("img/volver.png", (80, 80))
reset_white = cargar_imagen("img/reset_white.png", (80, 80))
volver_white = cargar_imagen("img/volver_white.png", (80, 80))
error = cargar_imagen("img/error.png", (70, 70))
sudoku_icon = cargar_imagen("img/icon.png")
config = cargar_imagen("img/config.webp")


reset_rect = reset.get_rect()
reset_rect.topleft = (1100, 100) 

volver_rect = volver.get_rect()
volver_rect.topleft = (1100, 550)

volver_white_rect = volver_white.get_rect()
volver_rect.topleft = (1100, 550)

volver_white_config_rect = volver_white.get_rect()
volver_white_config_rect.topleft = (1175, 600)

volver_config_rect = volver.get_rect()
volver_config_rect.topleft = (1175, 600)


DICCIONARIO_IMAGENES = [
    {
        "nombre": "reset",
        "surface": reset,   # La imagen en sí cargada con pygame
        "surface_rect": reset_rect,  # El objeto rectangulo de la imagen
        "url": "img/reset.webp",
        "posicion_x": 1100,  # Para posicionar la imagen en blit
        "posicion_y": 100,   # Para posicionar la imagen en blit
    },
    {
        "nombre": "reset_white",
        "surface": reset_white,
        "surface_rect": reset_rect,
        "url": "img/reset.webp",
        "posicion_x": 1100,
        "posicion_y": 100,
    },
    {
        "nombre": "volver",
        "surface": volver,
        "surface_rect": volver_rect,
        "url": "img/volver.png",
        "posicion_x": 1100,
        "posicion_y": 550,
    },
    {
        "nombre": "volver_white",
        "surface": volver_white,
        "surface_rect": volver_rect,
        "url": "img/volver_white.png",
        "posicion_x": 1100,
        "posicion_y": 550,
    },
    {
        "nombre": "volver_white_config",
        "surface": volver_white,
        "surface_rect": volver_white_config_rect,
        "url": "img/volver_white.png",
        "posicion_x": 1175,
        "posicion_y": 600,
    },
    {
        "nombre": "volver_config",
        "surface": volver,
        "surface_rect": volver_config_rect,
        "url": "img/volver.png",
        "posicion_x": 1175,
        "posicion_y": 600,
    },
    {
        "nombre": "error",
        "surface": error,
        "surface_rect": None,
        "url": "img/error.png",
        "posicion_x": 500,
        "posicion_y": 20,
    }, 
]