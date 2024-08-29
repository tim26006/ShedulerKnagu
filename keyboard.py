
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


reply_kb1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Начать отправлять расписание")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

reply_kb2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🕐 16:00"),
         KeyboardButton(text="🕐 18:00"),
            KeyboardButton(text="🕐 19:00")


         ]

    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

