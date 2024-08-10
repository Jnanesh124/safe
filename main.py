import os
from pyrogram import Client
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve environment variables
bot_token = os.environ.get("BOT_TOKEN")
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

# Directory where plugins are stored
plugins = dict(
    root="plugins"
)

# Initialize the Pyrogram Client
Bot = Client(
    "URL-Shortner-Bot",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
    plugins=plugins,
    workers=50,
    sleep_threshold=10
)

# Start the bot
if __name__ == "__main__":
    Bot.run()
