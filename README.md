# 🤖 Bot de Oposiciones Informática BOE

[![GitHub Actions](https://github.com/XXnikoDarkXX/BotsTelegram/actions/workflows/bot.yml/badge.svg)](https://github.com/XXnikoDarkXX/BotsTelegram/actions)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)

Bot que consulta el BOE español cada día y avisa en Telegram cuando se publican nuevas **oposiciones de informática**.  
Ideal para estar al día de los procesos selectivos sin tener que revisar manualmente el BOE.

---

## 🚀 ¿Qué hace este bot?

- Consulta diariamente el [BOE](https://www.boe.es/) usando su API.
- Filtra anuncios de oposiciones relacionados con informática.
- Envía automáticamente los avisos a un canal de Telegram.

---

## 📦 Requisitos

- Python **3.13** (recomendado usar entorno virtual)
- Un bot de Telegram creado en [@BotFather](https://t.me/BotFather)
- Un canal de Telegram donde quieras recibir los avisos (el bot debe ser **administrador** del canal)

---

## 🛠️ Instalación y uso local

1. **Clona este repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/tu-repo.git
    cd tu-repo
    ```

2. **Crea un entorno virtual (opcional pero recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate    # En Linux/Mac
    .\venv\Scripts\activate     # En Windows
    ```

3. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configura tu token de bot:**
    - Crea un archivo `.env` en la raíz del proyecto:
        ```
        BOT_TOKEN=tu_token_del_bot_de_telegram
        ```
    - (El `CHAT_ID` está configurado en el código, pero puedes parametrizarlo si lo necesitas.)

5. **Ejecuta el bot manualmente:**
    ```bash
    python main.py
    ```

---

## ☁️ Ejecución automática con GitHub Actions

1. **Guarda tu token de bot como secreto en GitHub:**
   - Ve a `Settings > Secrets and variables > Actions` y añade un secreto llamado `BOT_TOKEN`.

2. **El workflow de Actions (`.github/workflows/bot.yml`) ya está listo** para:
    - Ejecutarse automáticamente cada día a las 09:00 (hora peninsular española).
    - O lanzarse manualmente desde la pestaña Actions de GitHub.

3. **¡No subas nunca tu `.env` ni el token a tu repo!**

---

## 💬 Notas y personalización

- El canal de Telegram está fijado en el código (`CHAT_ID = "@avisos_oposiciones_informaticaa"`).  
  Si quieres que el bot avise en otro canal, **añade el bot como administrador** y cambia esa variable.
- Puedes adaptar las palabras clave (`PALABRAS_INFORMATICA` y `PALABRAS_SELECCION`) para otros temas o cuerpos.

---

## 📝 Ejemplo de mensaje en Telegram

📅 BOE del 20250711
📌 Cuerpo de Técnicos Superiores de Sistemas Informáticos
🔗 Ver en BOE
📄 PDF

yaml
Copiar
Editar

---

## 🤝 Contribuir

¡Se aceptan pull requests!  
Puedes mejorar el filtrado, los mensajes o adaptar el bot a otros ámbitos del BOE.

---

## 🛡️ Seguridad

**El token del bot nunca debe estar en el código ni en los logs.**  
Se recomienda siempre usar variables de entorno y GitHub Secrets.

---

## 🧑‍💻 Autor

- [XXnikoDarkXX](https://github.com/XXnikoDarkXX)

---

## 📜 Licencia

MIT

---
