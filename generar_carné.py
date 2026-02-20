import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

#Config

RUTA_EXCEL = "excel/carnet 2026 estudiantes.xlsx"
HOJA = 0 #HOJA DE EXCEL EN LA QUE LEERÁ
PLANTILLA_PNG = "plantilla/Carnet Estudiantil 2026.png"
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

# Fuente (si no tienes, dejamos default)
RUTA_FUENTE = None  # ejemplo: "fuentes/arial.ttf"
TAM_FUENTE = 28

#FUNCION RECORTAR FOTO EN CIRCULO

def recortarFoto(imagen: Image.Image, size: int) -> Image.Image:
    """
    Recorta la imagen en un círculo con transparencia
    Devuelve una imagen RGBA size x size.
    """

    img = imagen.convert("RGBA")
    
    # Recorte cuadrado centrado
    w, h = img.size
    lado = min(w, h)
    left = (w - lado) // 2
    top = (h - lado) // 2
    img = img.crop((left, top, left + lado, top + lado))

    # Redimensionar
    img = img.resize((size, size), Image.LANCZOS)

    # Crear máscara circular
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)

     # Aplicar máscara
    resultado = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    resultado.paste(img, (0, 0), mask)
    return resultado


def cargar_fuente(size: int) -> ImageFont.ImageFont:
    if RUTA_FUENTE and os.path.exists(RUTA_FUENTE):
        return ImageFont.truetype(RUTA_FUENTE, size)
    return ImageFont.load_default()


def obtener_ruta_foto(carnet: str) -> str | None:
    """
    Busca foto del estudiante en la carpeta de fotos por múltiples extensiones.
    """
    posibles = [
        f"{carnet}.jpg", f"{carnet}.jpeg", f"{carnet}.png",
        f"{carnet}.JPG", f"{carnet}.JPEG", f"{carnet}.PNG",
    ]
    for nombre in posibles:
        ruta = os.path.join(CARPETA_FOTOS, nombre)
        if os.path.exists(ruta):
            return ruta
    return None


def generar_carnet(fila: dict):
    """
    Genera un carnet PNG en la carpeta salida.
    """
    os.makedirs(SALIDA, exist_ok=True)

    carnet_val = fila["Carnet"]
    if pd.isna(carnet_val):
        print("[AVISO] Fila sin Carnet, se omite.")
    return

    # Si viene como número tipo 20250001.0, lo convertimos a int
    if isinstance(carnet_val, (int, float)) and float(carnet_val).is_integer():
        carnet_id = str(int(carnet_val))
    else:
        carnet_id = str(carnet_val).strip()

    nombres = str(fila.get("Nombres", "")).strip()
    apellidos = str(fila.get("Apellidos", "")).strip()
    carrera = str(fila.get("Carrera", "")).strip()

    nombre_completo = f"{nombres} {apellidos}".strip()

    # Cargar plantilla
    base = Image.open(PLANTILLA_PNG).convert("RGBA")

    # Insertar foto circular
    ruta_foto = obtener_ruta_foto(carnet_id)
    if ruta_foto:
        foto = Image.open(ruta_foto)
        foto_circ = recortarFoto(foto, FOTO_TAM)
        base.paste(foto_circ, (FOTO_X, FOTO_Y), foto_circ)
    else:
        print(f"[AVISO] No se encontró foto para: {carnet_id}")

    # Dibujar textos
    draw = ImageDraw.Draw(base)
    font = cargar_fuente(TAM_FUENTE)

    draw.text((TXT_NOMBRE_X, TXT_NOMBRE_Y), nombre_completo, font=font, fill=(0, 0, 0, 255))
    draw.text((TXT_CARRERA_X, TXT_CARRERA_Y), carrera, font=font, fill=(0, 0, 0, 255))
    draw.text((TXT_CARNET_X, TXT_CARNET_Y), f"Carnet: {carnet_id}", font=font, fill=(0, 0, 0, 255))

    # Guardar
    salida_png = os.path.join(SALIDA, f"{carnet_id}.png")
    base.save(salida_png, "PNG")
    print(f"[OK] Generado: {salida_png}")


def main():
    # Leer Excel
    df = pd.read_excel(RUTA_EXCEL, sheet_name=HOJA)

    # Validación mínima de columnas
    requeridas = ["Carnet", "Nombres", "Apellidos", "Carrera"]
    faltan = [c for c in requeridas if c not in df.columns]
    if faltan:
        raise ValueError(f"Faltan columnas en Excel: {faltan}. Columnas detectadas: {list(df.columns)}")

    # Convertir a dict y generar carnets
    for _, row in df.iterrows():
        generar_carnet(row.to_dict())


if __name__ == "__main__":
    main()