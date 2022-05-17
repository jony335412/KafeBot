from loader import dp, db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.default.cats import all_cats


@dp.callback_query_handler(text="clean", state=Shop.delete)
async def clean_cart(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    user_id = data.get('user_id')
    print(user_id)
    db.clear_cart(tg_id=user_id)
    await call.answer("Savat bo'shatildi")
    await call.message.answer("Asosiy sahifadasiz kerakli kategoriyani tanlang", reply_markup=all_cats)
    await Shop.category.set()

@dp.callback_query_handler(state=Shop.delete)
async def delete_products(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    title, tg_id = call.data.split(":")
    db.delete_current_product(tg_id=tg_id, title=title)
    await call.answer(f"{title} savatdan o'chirildi")
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
    await call.message.edit_text(msg, reply_markup=all)
    await Shop.delete.set()
