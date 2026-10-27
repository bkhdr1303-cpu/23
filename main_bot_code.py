import asyncio
import logging
import os
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Logs configuration
logging.basicConfig(level=logging.INFO)

# Token configuration - from environment variable (Render) or local file
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    try:
        with open("token.txt", "r") as f:
            BOT_TOKEN = f.read().strip()
    except FileNotFoundError:
        pass

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN mavjud emas! Render Environment Variables yoki token.txt faylida ko'rsating.")

# Channel setup
CHANNEL_USERNAME = "@elontopildimi"

# Initialize Bot and Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Phones module inside main logic
PHONE_OPERATORS = {
    '90': 'Beeline', '91': 'Beeline',
    '93': 'Ucell', '94': 'Ucell',
    '97': 'Mobiuz', '88': 'Mobiuz',
    '99': 'Uztelecom', '95': 'Uztelecom', '77': 'Uztelecom',
    '33': 'Humans',
    '98': 'Perfectum'
}

def format_phone_number(phone_str: str) -> str:
    """Formats phone number and identifies provider."""
    digits = re.sub(r'\D', '', phone_str)
    if digits.startswith('998') and len(digits) == 12:
        code = digits[3:5]
        formatted = f"+998 ({code}) {digits[5:8]}-{digits[8:10]}-{digits[10:12]}"
        operator = PHONE_OPERATORS.get(code, "Noma'lum operator")
        return f"{formatted} ({operator})"
    elif len(digits) == 9:
        code = digits[:2]
        formatted = f"+998 ({code}) {digits[2:5]}-{digits[5:7]}-{digits[7:9]}"
        operator = PHONE_OPERATORS.get(code, "Noma'lum operator")
        return f"{formatted} ({operator})"
    return phone_str

@dp.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "Assalomu alaykum! Topildizmi botiga xush kelibsiz.\n\n"
        "Yo'qotilgan yoki topib olingan buymlar bo'yicha e'lon berishingiz mumkin."
    )
    await message.answer(welcome_text)

@dp.message(F.text)
async def handle_message(message: Message):
    # Extracts phone numbers in text and formats them
    text = message.text
    phone_matches = re.findall(r'(?:\+?998|0)?[\s-]?\(?\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}', text)
    
    if phone_matches:
        formatted_phones = [format_phone_number(p) for p in phone_matches]
        response = f"Topilgan raqamlar:\n" + "\n".join(formatted_phones)
        await message.reply(response)

async def main():
    logging.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())