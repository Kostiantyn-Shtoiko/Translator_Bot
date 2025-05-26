import asyncio
from config import bot, dp
from app.handlers import router

#Basic asynchronous function to run the bot
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

# Entry point to the program
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot disabled')
