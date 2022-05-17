from loader import dp, db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext
from keyboards.default.cats import all_cats
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


@dp.message_handler(text="Orqaga", state=Shop.product)
async def home(message: types.Message):
    await message.answer("Asosiy sahifadasiz kerakli kategoriyani tanlang", reply_markup=all_cats)
    await Shop.category.set()


@dp.callback_query_handler(text="back", state=Shop.amount)
async def get2_products(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    cat_id = data.get('cat_id')
    categoriya = data.get('categoriya')
    products = db.get_product_cat_id(cat_id=cat_id)
    prod = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    for p in products:
        prod.insert(KeyboardButton(text=str(p[0])))
    prod.add(KeyboardButton(text="Orqaga"))
    await call.message.answer(f"{categoriya} kategoriyasidagi mahsulotlar", reply_markup=prod)
    await Shop.product.set()


@dp.callback_query_handler(text='back', state=Shop.delete)
async def main_m(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Asosiy sahifadasiz kerakli kategoriyani tanlang", reply_markup=all_cats)
    await Shop.category.set()


@dp.callback_query_handler(text="main", state=Shop.amount)
async def main_menu(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Asosiy sahifadasiz kerakli kategoriyani tanlang", reply_markup=all_cats)
    await Shop.category.set()