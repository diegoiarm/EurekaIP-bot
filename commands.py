import logging
import requests
import ipdata
import aiohttp
from bot import *
from config import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from tabulate import tabulate  # Para formatear la tabla
from bs4 import BeautifulSoup



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
def format_torrent_message(language, ip_address, torrents):
    header = """"""
    if language == 'en':
        header = f"Here are the torrents recently downloaded by {ip_address}:\n"
    else:  # Default to Spanish
        header = f"Aquí están los torrents descargados últimamente por {ip_address}:\n"

    return header + "\n".join(torrents)

async def torrents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'es')  # Idioma predeterminado 'es'

    if context.args:
        ip_address = context.args[0]
        url = f"https://iknowwhatyoudownload.com/en/peer/?ip={ip_address}"

        payload = { 
            'api_key': SCRAPER_API_KEY, 
            'url': url,
            'country_code': 'us'
        }

        try:
            # Realiza la solicitud HTTP a ScraperAPI
            response = requests.get('https://api.scraperapi.com/', params=payload)
            response.raise_for_status()

            # Parsear el contenido con BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscar la tabla de torrents con la clase correcta
            torrents_table = soup.find('table', {'class': 'table table-condensed table-striped'})
            
            if torrents_table:
                torrents = []
                for row in torrents_table.find_all('tr')[1:]:  # Omitir el encabezado
                    columns = row.find_all('td')

                    if len(columns) >= 5:
                        first_seen = columns[0].text.strip()
                        last_seen = columns[1].text.strip()
                        category = columns[2].text.strip()
                        title = columns[3].text.strip()
                        size = columns[4].text.strip()

                        if title and size and first_seen and last_seen:
                            if language == 'en':
                                torrents.append(f"\n🎬 {title} ({size}) ({category}) - First seen: {first_seen}, Last seen: {last_seen}")
                            else:  # Español
                                torrents.append(f"\n🎬 {title} ({size}) ({category}) - Primera vez visto: {first_seen}, Última vez visto: {last_seen}")
                
                if torrents:
                    message = format_torrent_message(language, ip_address, torrents)
                else:
                    message = "No torrents found for the given IP address." if language == 'en' else "No se encontraron torrents descargados para la IP proporcionada."
            else:
                message = "No data available on the page." if language == 'en' else "No se encontraron datos disponibles en la página."
        
        except requests.exceptions.RequestException as e:
            message = "An error occurred while accessing torrent data. Please try again later." if language == 'en' else "Ocurrió un error al acceder a los datos de torrents. Por favor, inténtalo de nuevo más tarde."

    else:
        if language == 'en':
            message = "Please provide an IP address to see downloaded torrents.\n\nExample: /torrents 8.8.8.8"
        else:
            message = "Por favor, proporciona una dirección IP para ver los torrents descargados.\n\nEjemplo: /torrents 8.8.8.8"

    if not message.strip():
        message = "Unknown error. Failed to generate the message." if language == 'en' else "Error desconocido. No se pudo generar el mensaje."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def threatintel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    language = user_languages.get(user_id, 'es')  # 'es' como idioma predeterminado

    if context.args:
        ip_address = context.args[0]
        try:
            response = requests.get(f"https://api.ipdata.co/{ip_address}/threat?api-key={ipdata.api_key}")
            response.raise_for_status()  # Esto va a generar una excepción para respuestas con status codes 4xx/5xx
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
            message = "Please provide an IP address to retrieve threat intelligence data.\n\nExample: /threats 8.8.8.8"
        else:  # Español
            message = "Por favor, proporciona una dirección IP para recuperar el reporte de amenazas.\n\nEjemplo: /threats 8.8.8.8"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
