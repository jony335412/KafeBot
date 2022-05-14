from loader import dp, db
from aiogram import types
from states.product import Shop
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.message_handler(state=Shop.category, text="Savat")
async def get_produc(message: types.Message):
    msg = "Sizning savatingizda:\n\n"
    cart = db.get_current_products(tg_id=message.from_user.id)
    all = InlineKeyboardMarkup(row_width=1)
    for c in cart:
        msg += f"{c[2]} ✖️ {c[-1]} = {int(c[-1]) * int(c[-2])} so'm\n"
        all.insert(InlineKeyboardButton(text=f"❌ {c[2]} ❌", callback_data=f"{c[2]}:{c[1]}"))
    await message.answer(msg, reply_markup=all)
    await Shop.delete.set()