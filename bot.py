import logging
import asyncio
from commands import *
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from tabulate import tabulate  # Para formatear la tabla
from config import BOT_TOKEN

# Configuración del logging en consola
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    logging.info("Iniciando configuración del bot...")

    # Manejadores de comandos
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('language', language_command))
    application.add_handler(CommandHandler('ipinfo', ipinfo_command))
    application.add_handler(CommandHandler('torrents', torrents_command))
    application.add_handler(CommandHandler('threats', threatintel_command))

    application.add_handler(CallbackQueryHandler(button_handler))

    # Ejecuta el bot
    logging.info("Bot configurado correctamente")
    logging.info("Comandos registrados: start, language, ipinfo, torrents, threats")
    logging.info("Iniciando el bot...")
    
    try:
        asyncio.run(application.run_polling())
        logging.info("¡Bot ejecutándose correctamente!")
    except Exception as e:
        logging.error(f"Error al iniciar el bot: {str(e)}")

