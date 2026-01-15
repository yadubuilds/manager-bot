from pyrogram import Client
from core.config import Config
from bot.panel import register_panel
from bot.update import register_update


app = Client(
    "control-bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

register_panel(app)
print("Control bot started")
app.run()
