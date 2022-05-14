from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

numbers = InlineKeyboardMarkup()
for i in range(1, 10):
    numbers.insert(InlineKeyboardButton(text=f"+{i}", callback_data=str(i)))
numbers.insert(InlineKeyboardButton(text="Savat", callback_data="savat"))
numbers.insert(InlineKeyboardButton(text="Orqaga", callback_data="back"))
numbers.insert(InlineKeyboardButton(text="Bosh menyu", callback_data="main"))
