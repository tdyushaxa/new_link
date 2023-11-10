from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




rek = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Reklama uchun", url="https://t.me/shaxsiy_loyihalar"),
        ]
    ]
)

cencelbtn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bekor qilish.")
        ]
    ],
    resize_keyboard=True
)

adminpanelbtn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Statistika"),
            KeyboardButton(text="📤 Tarqatish"),
        ],
        [
            KeyboardButton(text="Xabar yuborish")
        ],
        [
            KeyboardButton(text="➕ Ilova qo'shish"),
            KeyboardButton(text="✅ Majburiy obuna")
        ],
        [
            KeyboardButton(text="Active")
        ]
    ],
    resize_keyboard=True
)

sendor = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="send"),
            InlineKeyboardButton(text="❌", callback_data="sendx")
        ]
    ]
)

typepost = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="TEXT", callback_data="text"),
            InlineKeyboardButton(text="PHOTO", callback_data="photo")
        ]
    ]
)

keyboard_admin_obuna = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Qo'shish", callback_data="kanal_qoshish"),
            InlineKeyboardButton(text="➖ Olib tashlash", callback_data="kanal_olib_tashlash"),
        ]
    ]
)



agree = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ha'),
            KeyboardButton(text="Yo'q"),
        ],
    ],
    resize_keyboard=True
)


reklama_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Photo'),
            KeyboardButton(text='Text'),
        ],
    ],
    resize_keyboard=True
)
