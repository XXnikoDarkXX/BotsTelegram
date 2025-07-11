import requests
import xml.etree.ElementTree as ET
import unicodedata
import datetime
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv
load_dotenv()
# === CONFIGURACIÓN ===

PALABRAS_INFORMATICA = [
    "informatica", "informatico", "informática", "informático"
]

PALABRAS_SELECCION = [
    "oposicion", "proceso selectivo", "aspirantes", "cuerpo", "ingreso", "funcionario"
]

# Telegram


BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "@avisos_oposiciones_informaticaa"

# =====================

def normaliza(s: str) -> str:
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode().lower()

def filtra_oposiciones(root) -> list:
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

# --- FUNCIONES ASÍNCRONAS PARA TELEGRAM ---

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

# --- MAIN ---

def main():
    hoy = datetime.date.today()
    fecha_str = hoy.strftime('%Y%m%d')

    resultados = procesar_fecha(fecha_str)

    if resultados:
        print(f"📅 BOE del {fecha_str}: {len(resultados)} resultado(s) encontrado(s)")
        for o in resultados:
            mensaje = (
                f"<b>📅 BOE del {fecha_str}</b>\n"
                f"<b>📌 {o['titulo']}</b>\n"
                f"<a href='{o['url_html']}'>🔗 Ver en BOE</a>\n"
                f"<a href='{o['url_pdf']}'>📄 PDF</a>"
            )
            print(f"Enviando mensaje al canal:\n{mensaje}\n")
            enviar_mensaje_telegram(mensaje)
    else:
        mensaje = (
            f"<b>📅 BOE del {fecha_str}</b>\n"
            f"❌ No se encontraron oposiciones de informática publicadas hoy."
        )
        print(mensaje)
        enviar_mensaje_telegram(mensaje)

if __name__ == '__main__':
    main()
