import logging
import requests
import ipdata
import aiohttp
from bot import *
from config import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from tabulate import tabulate  # Para formatear la tabla


# Diccionario para almacenar las preferencias de idioma por usuario
user_languages = {}

# Función para mostrar el menú de selección de idioma
async def show_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data='en'),
            InlineKeyboardButton("Español 🇪🇸", callback_data='es')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="¡Bienvenido a EurekaIP Bot! 🤖\n"
             "Por favor, elige tu idioma: | Please choose your language: ",
        reply_markup=reply_markup
    )

# Función para mostrar el menú de cambio de idioma
async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data='en'),
            InlineKeyboardButton("Español 🇪🇸", callback_data='es')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Por favor, elige tu idioma: | Please choose your language: ",
        reply_markup=reply_markup
    )

# Función para manejar el comando /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_language_selection(update, context)

# Función para manejar el comando /language
async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await change_language(update, context)

# Función para manejar la selección de idioma
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()
    
    # Procesa la selección de idioma y almacena la preferencia
    if query.data == 'en':
        user_languages[user_id] = 'en'
        await query.edit_message_text(text="🇬🇧 You have successfully selected English.")

        # Mostrar lista de comandos en inglés
        commands_message = (
            "To continue, here you have the available commands 👇\n"
            "/start - Start the bot\n"
            "/ipinfo - Get information about an IP address\n"
            "/torrents - Get torrent downloads by IP\n"
            "/threats - Get threat intelligence for an IP\n"
            "/language - Change the language\n"
        )

        await context.bot.send_message(chat_id=user_id, text=commands_message)
        
    elif query.data == 'es':
        user_languages[user_id] = 'es'
        await query.edit_message_text(text="🇪🇸 Has seleccionado Español con éxito.")

        # Mostrar lista de comandos en español
        commands_message = (
            "Para continuar, aquí tienes los comandos disponibles 👇\n"
            "/start - Iniciar el bot\n"
            "/ipinfo - Obtener información sobre una dirección IP\n"
            "/torrents - Ver descargas de torrents por IP\n"
            "/threats - Obtener inteligencia de amenazas para una IP\n"
            "/language - Cambiar el idioma\n"
        )
        await context.bot.send_message(chat_id=user_id, text=commands_message)

# Función para manejar el comando /ipinfo
async def ipinfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'es')  # 'es' como idioma predeterminado

    if context.args:
        ip_address = context.args[0]
        details = handler.getDetails(ip_address)
        maps_link = f"https://www.google.com/maps?q={details.latitude},{details.longitude}"

        if language == 'en':
            message = (
                f"🌐 IP: {details.ip}\n"
                f"Here is the data I was able to gather about IP {details.ip}:\n"
                f"🏙️ City: {details.city}\n"
                f"🗺️ Region: {details.region}\n"
                f"🌍 Country: {details.country_name}\n"
                f"📮 Postal Code: {details.postal}\n"
                f"📍 Location: {details.loc} - {maps_link}\n"
                f"📏 Latitude: {details.latitude}\n"
                f"📐 Longitude: {details.longitude}\n"
                f"🏢 Organization: {details.org}\n"
            )
        else:  # Español
            message = (
                f"🌐 IP: {details.ip}\n"
                f"Estos son los datos que pude recopilar sobre la IP {details.ip}:\n"
                f"🏙️ Ciudad: {details.city}\n"
                f"🗺️ Región: {details.region}\n"
                f"🌍 País: {details.country_name}\n"
                f"📮 Código Postal: {details.postal}\n"
                f"📍 Ubicación: {details.loc} - {maps_link}\n"
                f"📏 Latitud: {details.latitude}\n"
                f"📐 Longitud: {details.longitude}\n"
                f"🏢 Organización: {details.org}\n"
            )
    else:
        if language == 'en':
            message = (
                "For security and privacy reasons, we cannot track your IP directly. \n"
                "\nWe suggest visiting https://2ip.io/ to find out your IP, then use the /ipinfo command followed by the IP you want to track. \n"
                "\nExample: /ipinfo 8.8.8.8"
            )
        else:  # Español
            message = (
                "Por políticas de seguridad y privacidad de Telegram, no podemos rastrear tu IP directamente. \n" 
                "\nTe sugerimos visitar https://2ip.io/ para conocer tu IP y luego, usar el comando /ipinfo seguido de la IP que deseas rastrear. \n"
                "\nEjemplo: /ipinfo 8.8.8.8"
            )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Función para manejar el comando /torrents
async def torrents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'es')  # 'es' como idioma predeterminado

    if context.args:
        imdb_ids = ','.join(context.args)  # Junta varios IMDB IDs en una sola cadena
        params = {'imdb': imdb_ids, 'key': CONTENT_API_KEY}
        
        try:
            response = requests.get(CONTENT_API_URL, params=params)
            logging.info("API Response Status Code: %d", response.status_code)  # Imprimir código de estado
            logging.info("API Response Content: %s", response.text)  # Imprimir contenido de la respuesta
            
            if response.status_code == 200:
                data = response.json()
                if 'contents' in data and data['contents']:
                    contents = data['contents']
                    if language == 'en':
                        message = "Downloaded torrents by IP:\n\n"
                        for content in contents:
                            message += f"Title: {content.get('name', 'N/A')}\n"
                            message += f"Total Peers: {content.get('totalPeers', 'N/A')}\n\n"
                    else:  # Español
                        message = "Torrents descargados por IP:\n\n"
                        for content in contents:
                            message += f"Título: {content.get('name', 'N/A')}\n"
                            message += f"Total de Peers: {content.get('totalPeers', 'N/A')}\n\n"
                else:
                    if language == 'en':
                        message = "No torrent data available for the specified IMDB IDs."
                    else:  # Español
                        message = "No hay datos de torrents disponibles para los IMDB IDs especificados."
            else:
                message = "Failed to retrieve data from the API. Please try again later."
                
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        
        except Exception as e:
            logging.error("Error fetching data from API: %s", str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred. Please try again later.")
    else:
        if language == 'en':
            message = "Please provide at least one IMDB ID to search for torrents.\n\nExample: /torrents 12345"
        else:  # Español
            message = "Por favor, proporciona al menos un ID de IMDB para buscar torrents.\n\nEjemplo: /torrents 12345"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def threatintel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'es')  # 'es' como idioma predeterminado

    if context.args:
        ip_address = context.args[0]
        try:
            response = requests.get(f"https://api.ipdata.co/{ip_address}/threat?api-key={ipdata.api_key}")
            response.raise_for_status()  # Esto generará una excepción para respuestas con status codes 4xx/5xx
            threat_data = response.json()

            # Construir la tabla de resultados con tabulate
            if language == 'en':
                message = (
                    f"🌐 IP: {ip_address}\n"
                    f"Here is the threat intelligence data I was able to gather:\n\n"
                    f"🧅 Is TOR?: {'✔️' if threat_data.get('is_tor', False) else '❌'}\n"
                    f"☁️ Is iCloud Relay?: {'✔️' if threat_data.get('is_icloud_relay', False) else '❌'}\n"
                    f"🛡️ Is Proxy?: {'✔️' if threat_data.get('is_proxy', False) else '❌'}\n"
                    f"🏢 Is Datacenter?: {'✔️' if threat_data.get('is_datacenter', False) else '❌'}\n"
                    f"👤 Is Anonymous?: {'✔️' if threat_data.get('is_anonymous', False) else '❌'}\n"
                    f"🚨 Is Known Attacker?: {'✔️' if threat_data.get('is_known_attacker', False) else '❌'}\n"
                    f"⚠️ Is Known Abuser?: {'✔️' if threat_data.get('is_known_abuser', False) else '❌'}\n"
                    f"☠️ Is Threat?: {'✔️' if threat_data.get('is_threat', False) else '❌'}\n"
                    f"🌍 Is Bogon?: {'✔️' if threat_data.get('is_bogon', False) else '❌'}\n"
                )
            else:
                message = (
                    f"🌐 IP: {ip_address}\n"
                    f"\nAquí tienes la información de inteligencia de amenazas que pude recopilar:\n\n"
                    f"🧅 ¿Es TOR?: {'✔️' if threat_data.get('is_tor', False) else '❌'}\n"
                    f"☁️ ¿Posee iCloud Relay?: {'✔️' if threat_data.get('is_icloud_relay', False) else '❌'}\n"
                    f"🛡️ ¿Es Proxy?: {'✔️' if threat_data.get('is_proxy', False) else '❌'}\n"
                    f"🏢 ¿Es Datacenter?: {'✔️' if threat_data.get('is_datacenter', False) else '❌'}\n"
                    f"👤 ¿Es Anónima?: {'✔️' if threat_data.get('is_anonymous', False) else '❌'}\n"
                    f"🚨 ¿Es un atacante conocido?: {'✔️' if threat_data.get('is_known_attacker', False) else '❌'}\n"
                    f"⚠️ ¿Es un abusador conocido?: {'✔️' if threat_data.get('is_known_abuser', False) else '❌'}\n"
                    f"☠️ ¿Es amenaza?: {'✔️' if threat_data.get('is_threat', False) else '❌'}\n"
                    f"🌍 ¿Es una Bogon IP?: {'✔️' if threat_data.get('is_bogon', False) else '❌'}\n"
                )

            blocklists = threat_data.get('blocklists', [])
            if blocklists:
                blocklist_info = "\n".join([f"📋 {bl['name']} ({bl['site']})" for bl in blocklists])
                message += f"\n🛑 Blocklists:\n{blocklist_info}"
            else:
                if language == 'en':
                    message += "\n🛑 Blocklists: No info found."
                else: 
                    message += "\n🛑 Blocklists: No se encontró información."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

        except requests.exceptions.RequestException as e:
            logging.error("Error fetching threat intelligence data: %s", str(e))
            if language == 'en':
                message = "An error occurred while retrieving threat intelligence data. Please try again later."
            else:  # Español
                message = "Ocurrió un error al recuperar la información de amenazas. Por favor, inténtalo de nuevo más tarde."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        if language == 'en':
            message = "Please provide an IP address to retrieve threat intelligence data.\n\nExample: /threatintel 8.8.8.8"
        else:  # Español
            message = "Por favor, proporciona una dirección IP para recuperar el reporte de amenazas.\n\nEjemplo: /threatintel 8.8.8.8"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
