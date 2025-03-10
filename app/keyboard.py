from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пример кнопки")]],
    resize_keyboard=True
)

catalog = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Пример", callback_data="example")]]
)
