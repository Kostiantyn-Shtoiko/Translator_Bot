from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

# Loads variables from .env file
load_dotenv()

# Take the token from .env for security
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()