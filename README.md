
# EurekaIP Bot 🤖🌐

EurekaIP Bot es un bot de Telegram que te proporciona información detallada sobre la dirección IP que tu quieras. 

Desde ubicación geográfica, informes de reputación e incluso los torrents más recientes descargados por una IP. Utiliza varias APIs para obtener información detallada y actualizada.

## Uso 💻

1. Busca el bot en Telegram con @eureka_ip_bot o accede a través de https://t.me/eureka_ip_bot

2. Inicia una conversación con el bot con el comando /start.

## Funcionalidades 🧩

- **/ipinfo**: Obtiene información detallada sobre una dirección IP usando la API de [IPinfo](https://ipinfo.io/). 🕵️‍♂️
- **/threatintel**: Proporciona un reporte de amenazas y análisis de IPs utilizando varias fuentes externas. 💡
- **/torrents**: Muestra los torrents más recientes descargados por una IP específica utilizando el servicio [I Know What You Download](https://iknowwhatyoudownload.com/). 📥

## Tecnologías 🛠️

- Python 
- Telegram API 
- APIs externas:
  - [IPinfo](https://ipinfo.io/) 
  - [IPdata](https://ipdata.co/) 
  - [I Know What You Download](https://iknowwhatyoudownload.com/en/peer/) 


## Requisitos ⚙️

- Python 3.x
- Librerías necesarias:
  - `python-dotenv`
  - `requests`
  - `beautifulsoup4`
  - `python-telegram-bot`

## Instalación 🏗️

1. Clona este repo:

  ```bash
  git clone https://github.com/diegoiarm/eureka-ip-bot.git
  cd eureka-ip-bot
```

2. Crea un entorno virtual:

  ```bash
  python -m venv venv
  venv\Scripts\activate
``` 

3. Instala las dependencias

  ```bash
  pip install -r requirements.txt
```

4. Configura las variables de entorno. Crea un archivo .env con lo siguiente:

  ```bash
  TELEGRAM_BOT_TOKEN=xxxx
  IPINFO_ACCESS_TOKEN=xxxx
  IPDATA_API_KEY=xxxx
  CONTENT_API_KEY=xxxx
  SCRAPER_API_KEY=xxxx
```

5. Ejecuta el bot:

  ```bash
  python bot.py
``` 

## Despliegue 🚀

Te recomiendo desplegar el bot en plataformas como Render o Heroku. 


## Contribuciones 🤝
Las contribuciones son más que bienvenidas! :)
