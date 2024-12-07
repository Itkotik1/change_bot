from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Кофе", callback_data="drink"),
        InlineKeyboardButton(text="Выпечка", callback_data="bakery")
    ],
    [
        InlineKeyboardButton(text="Сезонное меню", callback_data="sezon")
    ]
])