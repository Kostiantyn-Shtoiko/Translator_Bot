import asyncio
from config import bot, dp
from app.handlers import router
from aiogram.types import BotCommand

#Basic asynchronous function to run the bot
async def main():
    dp.include_router(router)
    await set_bot_commands(bot)
    await dp.start_polling(bot)

async def set_bot_commands(bot: bot):
    commands = [
        BotCommand(command="/start", description="opens the main menu with a language selection 🌍"),
        BotCommand(command="/translate", description="you will get a short guide on how to use the bot 🆘"),
        BotCommand(command="/history", description="Shows Only the last 5 translations 🧠"),
    ]
    await bot.set_my_commands(commands)

# Entry point to the program
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot disabled')
