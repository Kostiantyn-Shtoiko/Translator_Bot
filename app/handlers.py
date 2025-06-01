from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from translate import Translator
from langdetect import detect
from database import save_translation
import app.keyboards as kb
from app.keyboards import history_menu
from database import get_user_history
from datetime import datetime
import os

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

# Handling the "Back" button press
@router.callback_query(F.data == "back")
async def info_callback(callback: CallbackQuery):
    await callback.message.answer("🔤 Welcome to the translation bot", reply_markup=kb.home)

# Processing the "About us" button
@router.callback_query(F.data == "about_us")
async def info_callback(callback: CallbackQuery):
    with open("text/about_us.txt", "r", encoding="utf-8") as file:
        large_text = file.read()


    await callback.message.answer(large_text, reply_markup=kb.back_to_home)
    await callback.answer()

# Handling the "Help" button
@router.callback_query(F.data == "help")
async def info_callback(callback: CallbackQuery):
    with open("text/help.txt", "r", encoding="utf-8") as file:
        large_text = file.read()

    await callback.message.answer(large_text, reply_markup=kb.back_to_home)
    await callback.answer()

#History button handling
@router.callback_query(F.data == "history_menu")
async def open_history_menu(callback: CallbackQuery):
    await callback.message.answer("🔧 Choose an action with a story:", reply_markup=history_menu)
    await callback.answer()

# Handling the "last_5" button
@router.callback_query(F.data == "last_5")
async def show_last_5(callback: CallbackQuery):
    user_id = callback.from_user.id
    history = user_history.get(user_id)

    if not history:
        await callback.message.answer("📭 The translation history is empty.", reply_markup=kb.back_to_home)
        await callback.answer()
        return

    last_five = history[-5:]
    text = "🕔 Latest translations:\n\n"

    for item in last_five:
        text += f"🔸 `{item['original']}` ({item['from']} → {item['to']})\n➡️ `{item['translated']}`\n\n"

    await callback.message.answer(text, parse_mode="Markdown", reply_markup=kb.back_to_home)
    await callback.answer()

# History clearing processing
@router.callback_query(F.data == "clear_history")
async def clear_user_history(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id in user_history:
        user_history[user_id] = []  # clearing the translation list
        await callback.message.answer("🧹 Your translation history has been successfully cleared.", reply_markup=kb.back_to_home)
    else:
        await callback.message.answer("📭 You have no history to clean up.", reply_markup=kb.back_to_home)

    await callback.answer()

#View all translation history
@router.callback_query(F.data == "all_history")
async def show_all_history(callback: CallbackQuery):
    user_id = callback.from_user.id
    history = user_history.get(user_id)

    if not history:
        await callback.message.answer("📭 You don't have any translations yet.", reply_markup=kb.back_to_home)
        await callback.answer()
        return

    text = "📚 All translation history:\n\n"
    for item in history:
        text += f"🔸 `{item['original']}` ({item['from']} → {item['to']})\n➡️ `{item['translated']}`\n🗓 {item.get('date', '—')}\n\n"

    # Telegram limits messages to 4096 characters
    for chunk in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        await callback.message.answer(chunk, parse_mode="Markdown", reply_markup=kb.back_to_home)

    await callback.answer()

# export_history
@router.callback_query(F.data == "export_history")
async def export_translation_history(callback: CallbackQuery):
    user_id = callback.from_user.id
    history = user_history.get(user_id)

    if not history:
        await callback.message.answer("📭 There are no translations to export.", reply_markup=kb.back_to_home)
        await callback.answer()
        return

    text = "📤 Translation History\n\n"
    for item in history:
        text += (
            f"Original: {item['original']}\n"
            f"Translated: {item['translated']}\n"
            f"From: {item['from']} → To: {item['to']}\n"
            f"Date: {item.get('date', '—')}\n\n"
        )

    # Save to a temporary file
    filename = f"history_{user_id}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    # We send the file
    await callback.message.answer_document(types.FSInputFile(filename), caption="📝 Here is your translation history file.", reply_markup=kb.back_to_home)
    await callback.answer()

    # Deleting the file after sending
    os.remove(filename)


# Processing the /history command
@router.message(F.text == "/history")
async def show_history(message: Message):
    user_id = message.from_user.id
    history = get_user_history(user_id)

    if not history:
        await message.answer("📭 The translation history is empty.", reply_markup=kb.back_to_home)
        return

    text = "🕓 Latest translations:\n\n"
    for original, translated, lang_from, lang_to, date in history:
        text += (
            f"📅 {date}\n"
            f"🔸 `{original}` ({lang_from} → {lang_to})\n"
            f"➡️ `{translated}`\n\n"
        )

    await message.answer(text, parse_mode="Markdown", reply_markup=kb.back_to_home)

# User selects translation language
@router.callback_query(lambda c: c.data.startswith("to_"))
async def choose_target_language(call: CallbackQuery):
    user_id = call.from_user.id
    user_language[user_id] = call.data[3:]
    await call.message.answer("✍ Send text for translation!", reply_markup=kb.back_to_home)
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

        await message.answer(f"🌐 *Detected language:* `{lang_from}`\n"
                             f"📖 *Translation:* \n`{translated }`",
                             parse_mode="Markdown",
                             reply_markup=kb.back_to_home)

        # word storage history
        user_history.setdefault(user_id, []).append({
            "original": message.text,
            "translated": translated,
            "from": lang_from,
            "to": lang_to,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        #  We only keep the last 5 translations:
        if len(user_history[user_id]) > 5:
            user_history[user_id] = user_history[user_id][-5:]

        save_translation(
            user_id=user_id,
            original=message.text,
            translated=translated,
            lang_from=lang_from,
            lang_to=lang_to
        )

    except Exception as e:
        await message.answer(f"⚠ Translation error: {e}", reply_markup=kb.back_to_home)

# Processing a separate button for Russian (surprise mode)
@router.callback_query(F.data == "ru")
async def info_callback(callback: CallbackQuery):
    with open("text/hymn.txt", "r", encoding="utf-8") as file:
        large_text = file.read()

    await callback.message.answer(large_text, reply_markup=kb.back_to_home)
    await callback.answer()
