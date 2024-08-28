import logging
import asyncio
from commands import *
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from tabulate import tabulate  # Para formatear la tabla

# Configuración del logging en consola
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

if __name__ == '__main__':
    application = ApplicationBuilder().token('7168525558:AAE9Lm4XmskUrN6hmr4mqNsZPV0hobv1GHo').build()

    # Manejadores de comandos
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('language', language_command))
    application.add_handler(CommandHandler('ipinfo', ipinfo_command))
    application.add_handler(CommandHandler('torrents', torrents_command))
    application.add_handler(CommandHandler('threats', threatintel_command))

    application.add_handler(CallbackQueryHandler(button_handler))

    # Ejecuta el bot
    logging.info("Starting bot...")
    asyncio.run(application.run_polling())

