import requests
import xml.etree.ElementTree as ET
import unicodedata
import datetime
import asyncio
from telegram import Bot
import os
import re
from dotenv import load_dotenv

# === Cargar variables de entorno ===
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "@avisos_oposiciones_informaticaa"  # Cambia si usas otro canal

# === Palabras clave para filtrar ===
PALABRAS_INFORMATICA = [
    "informatica", "informatico", "informática", "informático"
]

# === Normalizar texto (acentos fuera) ===
def normaliza(s: str) -> str:
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode().lower()

# === Revisar si el título menciona "convocatoria" ===
def es_convocatoria(titulo: str) -> bool:
    titulo_norm = normaliza(titulo)
    return "convocatoria" in titulo_norm

# === Analiza HTML para buscar lugar, especialidad e informática ===
def analizar_convocatoria_html(url: str) -> dict:
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        texto = normaliza(response.text)

        # Detectar si es de informática
        es_informatica = any(pal in texto for pal in PALABRAS_INFORMATICA)

        # Buscar lugar
        lugar_match = re.search(r"(ayuntamiento|universidad|ministerio)[\w\s,.\-]{0,50}", texto)
        lugar = lugar_match.group(0).strip() if lugar_match else "No identificado"

        # Buscar especialidad
        especialidad_match = re.search(r"especialidad[\w\s,.\-]{0,50}", texto)
        especialidad = especialidad_match.group(0).strip() if especialidad_match else "No especificada"

        return {
            "es_informatica": es_informatica,
            "lugar": lugar,
            "especialidad": especialidad,
        }

    except Exception as e:
        print(f"⚠️ Error leyendo HTML de {url}: {e}")
        return {
            "es_informatica": False,
            "lugar": "Error",
            "especialidad": "Error"
        }

# === Buscar convocatorias informáticas en el BOE ===
def filtra_convocatorias_con_informatica(root) -> list:
    resultados = []
    for item in root.findall(".//item"):
        titulo = item.findtext("titulo", default="")
        url_html = item.findtext("url_html", default="")
        url_pdf = item.findtext("url_pdf", default="")

        if es_convocatoria(titulo) and url_html:
            print(f"🔍 Revisando: {titulo}")
            datos = analizar_convocatoria_html(url_html)
            if datos["es_informatica"]:
                print(f"✅ Coincidencia: {titulo}")
                resultados.append({
                    "titulo": titulo,
                    "url_html": url_html,
                    "url_pdf": url_pdf,
                    "lugar": datos["lugar"],
                    "especialidad": datos["especialidad"],
                })
    return resultados

# === Obtener XML del BOE ===
def obtener_xml_fecha(fecha: str):
    url = f'https://www.boe.es/datosabiertos/api/boe/sumario/{fecha}'
    headers = {"Accept": "application/xml"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None
    try:
        return ET.fromstring(resp.content)
    except:
        return None

# === Enviar mensaje a Telegram ===
async def enviar_mensaje_telegram_async(texto: str):
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=texto,
            parse_mode="HTML",
            disable_web_page_preview=False
        )
        print("✅ Mensaje enviado correctamente al canal.")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")

def enviar_mensaje_telegram(texto: str):
    asyncio.run(enviar_mensaje_telegram_async(texto))

# === MAIN ===
def main():
    hoy = datetime.date.today()
    fecha_str = "20250718"

    #echa_str = hoy.strftime('%Y%m%d')

    root = obtener_xml_fecha(fecha_str)
    if root is None:
        print(f"⚠️ No se pudo obtener el BOE del {fecha_str}")
        return

    resultados = filtra_convocatorias_con_informatica(root)

    if resultados:
        print(f"📅 BOE del {fecha_str}: {len(resultados)} resultado(s) encontrado(s)")
        for o in resultados:
            mensaje = (
                f"<b>📅 BOE del {fecha_str}</b>\n"
                f"<b>📌 {o['titulo']}</b>\n"
                f"📍 <b>Lugar:</b> {o['lugar']}\n"
                f"🧠 <b>Especialidad:</b> {o['especialidad']}\n"
                f"<a href='{o['url_html']}'>🔗 Ver en BOE</a>\n"
                f"<a href='{o['url_pdf']}'>📄 PDF</a>"
            )
            enviar_mensaje_telegram(mensaje)
    else:
        mensaje = (
            f"<b>📅 BOE del {fecha_str}</b>\n"
            f"❌ No se encontraron convocatorias de informática publicadas hoy."
        )
        print(mensaje)
        enviar_mensaje_telegram(mensaje)

if __name__ == '__main__':
    main()
