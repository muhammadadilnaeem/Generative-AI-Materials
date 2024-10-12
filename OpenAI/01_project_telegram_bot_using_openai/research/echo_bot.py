
# # Import libraries
# import os
# import logging
# from dotenv import load_dotenv
# from aiogram import Bot,Dispatcher,types

# # Set up API Keys
# load_dotenv()
# TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")

# # Configure Logging 
# logging.basicConfig(level=logging.INFO)

# # Initialize the bot and the dispatcher
# bot = Bot(token=TELEGRAM_BOT_TOKEN)
# dp = Dispatcher(bot)

# # Set up Telegram Bot
# @dp.message_handler(commands=['start', 'help'])
# async def command_start_handler(message: types.Message):
#     """
#     This handler receives messages with `/start` or  `/help `command
#     """
#     await message.reply("Hi\nI am Echo Bot!\nPowered by Adil.")

# # To handle messages
# @dp.message_handler()
# async def echo(message: types.Message):
#     """
#     This will retrun echo
#     """
#     await message.answer(message.text)

# # Run the bot
# if __name__ == "__main__":
#     executor.start_polling(dp, skip_updates=True)

# Import libraries
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import BotCommand
from aiogram import F

# Set up API Keys
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure Logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and the dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Set up Telegram Bot
@dp.message(F.text.in_(['start', 'help']))
async def command_start_handler(message: types.Message):
    """
    This handler receives messages with `/start` or `/help` command
    """
    await message.reply("Hi\nI am Echo Bot!\nPowered by Adil.")

# To handle messages
@dp.message(F.text)
async def echo(message: types.Message):
    """
    This will return echo
    """
    await message.answer(message.text)

# Set bot commands
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/help", description="Help information")
    ]
    await bot.set_my_commands(commands)

# Main function to run the bot
async def main():
    # Set bot commands
    await set_commands(bot)

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
