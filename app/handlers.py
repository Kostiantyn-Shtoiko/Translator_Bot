from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from translate import Translator
from langdetect import detect
import app.keyboards as kb

router = Router()

# Dictionary to store the language chosen by the user
user_language = {}

#[list of translations]
user_history = {}

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

# Processing the /history command
@router.message(F.text == "/history")
async def show_history(message: Message):
    user_id = message.from_user.id
    history = user_history.get(user_id)

    # If there is no history, notify the user
    if not history:
        await message.answer("📭 Your translation history is empty.")
        return

    # Forming the text with the latest translations
    text = "🕓 Recent translations:\n\n"
    for item in history:
        text += (
            f"🔹 Original: `{item['original']}` ({item['from']} → {item['to']})\n"
            f"➡️ Translated: `{item['translated']}`\n\n"
        )

    await message.answer(text, parse_mode="Markdown")

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

        # word storage history
        user_history.setdefault(user_id, []).append({
            "from": lang_from,
            "to": lang_to,
            "original": message.text,
            "translated": translated
        })

        #  We only keep the last 5 translations:
        if len(user_history[user_id]) > 5:
            user_history[user_id] = user_history[user_id][-5:]

    except Exception as e:
        await message.answer(f"⚠ Translation error: {e}")

# Processing a separate button for Russian (surprise mode)
@router.callback_query(F.data == "ru")
async def info_callback(callback: CallbackQuery):
    with open("text/hymn.txt", "r", encoding="utf-8") as file:
        large_text = file.read()

    await callback.message.answer(large_text)
    await callback.answer()
