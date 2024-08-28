import ipinfo
import ipdata

# API de IPinfo
ACCESS_TOKEN = '19106b4af4f276'
handler = ipinfo.getHandler(ACCESS_TOKEN)

# API de ipdata
ipdata.api_key = "3721ef6fc6c0f07a667bb989780a0ef2586e1f3d4458639b1f725cf9"

# API de Content API (Torrents)
API_KEY = 'a515bddeba444ea593b6fbf7f69aff59'
CONTENT_API_URL = 'https://api.antitor.com/content/downloads'
