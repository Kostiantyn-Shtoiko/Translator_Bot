from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Translation language selector keyboard (language selector)
choose_language = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇲", callback_data="to_en"),
            InlineKeyboardButton(text="🇺🇦", callback_data="to_uk")
        ],
        [
            InlineKeyboardButton(text="🇩🇪", callback_data="to_de"),
            InlineKeyboardButton(text="🇨🇵", callback_data="to_fr")
        ],
        [
            InlineKeyboardButton(text="🇭🇷", callback_data="to_hr"),
            InlineKeyboardButton(text="🇮🇹", callback_data="to_it"),
        ],
        [
            InlineKeyboardButton(text="🇵🇱", callback_data="to_pl"),
            InlineKeyboardButton(text="🇳🇱", callback_data="to_nl"),
        ],
        [
            InlineKeyboardButton(text="🇵🇹", callback_data="to_pt"),
            InlineKeyboardButton(text="🇹🇷", callback_data="to_tr"),
        ],
# Special button with a joke/position regarding Russian
        [
            InlineKeyboardButton(text="💩 🇷🇺 💩", callback_data="ru")
        ],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
    ]
)
# Main menu
home = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="▶️ Start", callback_data="start"),
            InlineKeyboardButton(text="❓ Help", callback_data="help")
        ],
        [
            InlineKeyboardButton(text="🕓 History", callback_data="history_menu")
        ],
        [
            InlineKeyboardButton(text="About us ©️", callback_data="about_us")
        ]
    ]
)
# Creation history menu
history_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔹 The last 5", callback_data="last_5")],
        [InlineKeyboardButton(text="📜 The whole story", callback_data="all_history")],
        [InlineKeyboardButton(text="🧹 Clean up", callback_data="clear_history")],
        [InlineKeyboardButton(text="📤 Export", callback_data="export_history")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
    ]
)

back_to_home = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
    ]
)
