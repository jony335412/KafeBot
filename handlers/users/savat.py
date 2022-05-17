from loader import dp, db
from aiogram import types
from states.product import Shop
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext


@dp.message_handler(state=Shop.category, text="Savat")
async def get_produc(message: types.Message):
    cart = db.get_current_products(tg_id=message.from_user.id)
    all = InlineKeyboardMarkup(row_width=1)
    if len(cart) != 0:
        msg = "Sizning savatingizda:\n\n"
        for c in cart:
            msg += f"{c[2]} ✖️ {c[-1]} = {int(c[-1]) * int(c[-2])} so'm\n"
            all.insert(InlineKeyboardButton(text=f"❌ {c[2]} ❌", callback_data=f"{c[2]}:{c[1]}"))
        all.insert(InlineKeyboardButton(text="Boshatish", callback_data="clean"))
        all.insert(InlineKeyboardButton(text="Buyurtma berish", callback_data="order"))
    else:
        msg = "Sizning savatingiz bo'sh buni to'girlashni imkoni bor"
    all.add(InlineKeyboardButton(text="Orqaga", callback_data="back"))
    await message.answer(msg, reply_markup=all)
    await Shop.delete.set()


@dp.callback_query_handler(text="savat", state=Shop.amount)
async def get_savat(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    user_id = data.get('user_id')
    cart = db.get_current_products(tg_id=user_id)
    all = InlineKeyboardMarkup(row_width=1)
    if len(cart) != 0:
        msg = "Sizning savatingizda:\n\n"
        for c in cart:
            msg += f"{c[2]} ✖️ {c[-1]} = {int(c[-1]) * int(c[-2])} so'm\n"
            all.insert(InlineKeyboardButton(text=f"❌ {c[2]} ❌", callback_data=f"{c[2]}:{c[1]}"))
        all.insert(InlineKeyboardButton(text="Boshatish", callback_data="clean"))
        all.insert(InlineKeyboardButton(text="Buyurtma berish", callback_data="order"))
    else:
        msg = "Sizning savatingiz bo'sh buni to'girlashni imkoni bor"
    all.add(InlineKeyboardButton(text="Orqaga", callback_data="back"))
    await call.message.answer(msg, reply_markup=all)
    await Shop.delete.set()