from loader import dp, db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.callback_query_handler(state=Shop.delete)
async def delete_products(call: types.CallbackQuery, state: FSMContext):
    msg = "Sizning savatingizda:\n\n"
    data = await state.get_data()
    user_id = data.get('user_id')
    title, tg_id = call.data.split(":")
    db.delete_current_product(tg_id=tg_id, title=title)
    await call.answer(f"{title} savatdan o'chirildi")
    cart = db.get_current_products(tg_id=user_id)
    all = InlineKeyboardMarkup(row_width=1)
    for c in cart:
        msg += f"{c[2]} ✖️ {c[-1]} = {int(c[-1]) * int(c[-2])} so'm\n"
        all.insert(InlineKeyboardButton(text=f"❌ {c[2]} ❌", callback_data=f"{c[2]}:{c[1]}"))
    await call.message.edit_text(msg, reply_markup=all)
    await Shop.delete.set()
