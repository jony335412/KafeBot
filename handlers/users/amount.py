from keyboards.default.cats import all_cats
from loader import dp, db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(state=Shop.amount)
async def get_amount(call: types.CallbackQuery, state: FSMContext):
    amount = call.data
    data = await state.get_data()
    title = data.get('title')
    price = data.get('price')
    user_id = data.get('user_id')
    await call.answer(f"{amount} ta {title} savatingizga qo'shildi", show_alert=True)
    await call.message.answer("Asosiy sahifa", reply_markup=all_cats)
    db.add_product_cart(tg_id=user_id, title=title, price=price, amount=amount)
    await call.message.delete()
    await Shop.category.set()