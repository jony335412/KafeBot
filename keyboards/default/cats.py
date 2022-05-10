from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import db


all_cats = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
categories = db.select_all_cats()

for cat in categories:
    all_cats.insert(KeyboardButton(text=cat[1]))