import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

bot_token = os.environ.get("BOT_TOKEN")
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
blogger_api_url = os.environ.get("BLOGGER_API_URL")  # Fetch BLOGGER_API_URL

plugins = dict(
    root="plugins"
)

Bot = Client(
    "URL-Shortner-Bot",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
    plugins=plugins,
    workers=50,
    sleep_threshold=10
)

Bot.run()
