import os
from dotenv import load_dotenv
import ipinfo
import ipdata

# Cargar variables de entorno
load_dotenv()

# Bot Token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# API de IPinfo
IPINFO_TOKEN = os.getenv('IPINFO_ACCESS_TOKEN')
handler = ipinfo.getHandler(IPINFO_TOKEN)

# API de ipdata
IPDATA_KEY = os.getenv('IPDATA_API_KEY')
ipdata.api_key = IPDATA_KEY

# API de Content API (Torrents)
CONTENT_API_KEY = os.getenv('CONTENT_API_KEY')
CONTENT_API_URL = 'https://api.antitor.com/content/downloads'

# ScraperAPI
SCRAPER_API_KEY = os.getenv('SCRAPER_API_KEY')
