import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

#Config

RUTA_EXCEL = "excel/carnet 2026 estudiantes.xlsx"
HOJA = 0 #HOJA DE EXCEL EN LA QUE LEERÁ
PLANTILLA_PNG = "plantilla/Carnet Estuantil 2026.png"
CARPETA_FOTOS = "fotos"
SALIDA = "salida"

#AJUSTAR COORDENADAS A LA PLANTILLA
# X, Y ESQUINA SUPERIOR IZQUIERDA DE LA FOTO

FOTO_X = 80
FOTO_Y = 120
FOTO_TAM = 260

#AJUSTAR COORDENADAS DE TEXTO
TXT_NOMBRE_X =380
TXT_NOMBRE_Y = 140

TXT_CARRERA_X = 380
TXT_CARRERA_Y = 200

TXT_CARNET_X = 380
TXT_CARNET_Y = 260

#FUNCION RECORTAR FOTO EN CIRCULO

def recortarFoto(imagen: Image.Image, size: int) -> Image.Image:
    """
    Recorta la imagen en un círculo con transparencia
    Devuelve una imagen RGBA size x size.
    """