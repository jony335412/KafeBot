from loader import dp, db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext
from keyboards.inline.amount import numbers


@dp.message_handler(state=Shop.product)
async def get_prod(message: types.Message, state: FSMContext):
    prod_name = message.text
    data = await state.get_data()
    cat_id = data.get('cat_id')
    info = db.get_product_title_id(title=prod_name, cat_id=cat_id)
    await state.update_data(
        {'title': str(info[1]), 'price': info[3], 'user_id': message.from_user.id}
    )
    await message.answer_photo(photo=info[4], caption=f"<b>{info[1]}</b>\n\nBatafsil: {info[2]}\nNarxi: {info[3]} so'm\n", reply_markup=numbers)
    await Shop.next()