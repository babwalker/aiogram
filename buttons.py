from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button = [
    [InlineKeyboardButton(text="вводный урок", callback_data="introductory_lesson"),
    InlineKeyboardButton(text="пройти задание", callback_data="task_lesson")],
]

lesson_button = InlineKeyboardMarkup(inline_keyboard=button)