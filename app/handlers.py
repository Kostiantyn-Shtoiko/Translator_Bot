from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from translate import Translator
from langdetect import detect
import app.keyboards as kb

router = Router()
# Dictionary to store the language chosen by the user
user_language = {}

# Start command /start
@router.message(CommandStart())
async def cmd_start(message: Message):
     await message.answer("🔤 Welcome to the translation bot", reply_markup=kb.home)

# Handling the "Start" button press
@router.callback_query(F.data == "start")
async def info_callback(callback: CallbackQuery):
    await callback.message.answer("🌍 Choose a language to translate:", reply_markup=kb.choose_language)

# Processing the "About us" button
@router.callback_query(F.data == "about_us")
async def info_callback(callback: CallbackQuery):
    with open("text/about_us.txt", "r", encoding="utf-8") as file:
        large_text = file.read()

    await callback.message.answer(large_text)
    await callback.answer()

# Обробка кнопки "Help"
@router.callback_query(F.data == "help")
async def info_callback(callback: CallbackQuery):
    with open("text/help.txt", "r", encoding="utf-8") as file:
        large_text = file.read()

    await callback.message.answer(large_text)
    await callback.answer()

# User selects translation language
@router.callback_query(lambda c: c.data.startswith("to_"))
async def choose_target_language(call: CallbackQuery):
    user_id = call.from_user.id
    user_language[user_id] = call.data[3:]  # Зберігаємо вибрану мову
    await call.message.answer("✍ Send text for translation!")
    await call.answer()

# Translate messages if a language is already selected
@router.message(lambda message: message.from_user.id in user_language)
async def translate_message(message: Message):
    user_id = message.from_user.id
    lang_to = user_language[user_id]

    # Automatic language detection
    try:
        lang_from = detect(message.text)
        translator = Translator(from_lang=lang_from, to_lang=lang_to)
        translated = translator.translate(message.text)

        await message.answer(f"🌐 *Detected language:* `{lang_from}`\n📖 *Translation:* \n`{translated }`", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"⚠ Translation error: {e}")

# Processing a separate button for Russian (surprise mode)
@router.callback_query(F.data == "ru")
async def info_callback(callback: CallbackQuery):
    with open("text/hymn.txt", "r", encoding="utf-8") as file:
        large_text = file.read()

    await callback.message.answer(large_text)
    await callback.answer()
