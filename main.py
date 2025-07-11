import requests
import xml.etree.ElementTree as ET
import unicodedata
import datetime

# === CONFIGURACIÓN ===

PALABRAS_INFORMATICA = [
    "informatica", "informatico", "informática", "informático"
]

PALABRAS_SELECCION = [
    "oposicion", "proceso selectivo", "aspirantes", "cuerpo", "ingreso", "funcionario"
]

# =====================

def normaliza(s: str) -> str:
    """Quita acentos y pasa a minúsculas ASCII."""
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode().lower()

def filtra_oposiciones(root) -> list:
    """Filtra títulos del BOE con coincidencias relevantes."""
    resultados = []

    for item in root.findall(".//item"):
        titulo = item.findtext("titulo", default="")
        url_html = item.findtext("url_html", default="")
        url_pdf = item.findtext("url_pdf", default="")

        titulo_norm = normaliza(titulo)

        tiene_informatica = any(pal in titulo_norm for pal in PALABRAS_INFORMATICA)
        tiene_selectivo = any(pal in titulo_norm for pal in PALABRAS_SELECCION)

        if tiene_informatica and tiene_selectivo:
            resultados.append({
                "titulo": titulo,
                "url_html": url_html,
                "url_pdf": url_pdf,
            })

    return resultados

def procesar_fecha(fecha: str):
    url = f'https://www.boe.es/datosabiertos/api/boe/sumario/{fecha}'
    headers = {"Accept": "application/xml"}
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        return None

    try:
        root = ET.fromstring(resp.content)
    except:
        return None

    return filtra_oposiciones(root)

def main():
    hoy = datetime.date.today()
    fecha_str = hoy.strftime('%Y%m%d')

    resultados = procesar_fecha(fecha_str)
    if resultados:
        print(f"\n📅 BOE del {fecha_str}:")
        for o in resultados:
            print(f"- {o['titulo']}")
            print(f"    HTML: {o['url_html']}")
            print(f"    PDF:  {o['url_pdf']}\n")
    else:
        print(f"No se encontraron oposiciones de informática en el BOE del {fecha_str}.")

if __name__ == '__main__':
    main()
