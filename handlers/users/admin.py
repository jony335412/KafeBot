import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from states.product import Category, Product
from aiogram.dispatcher import FSMContext
from datetime import datetime


@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       

@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="@BekoDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")


@dp.message_handler(commands=['category'], user_id=ADMINS)
async def add_category(message: types.Message):
    await message.answer("Qo'shmoqchi bo'lgan kategoriyangiz nomini kiriting")
    await Category.title.set()


@dp.message_handler(state=Category.title, user_id=ADMINS)
async def add_cat(message: types.Message, state: FSMContext):
    category = message.text
    await message.answer(f"{category} bazaga qo'shildi")
    db.add_category_title(title=str(category))
    await state.finish()


@dp.message_handler(commands=['product'], user_id=ADMINS)
async def add_product(message: types.Message):
    await message.answer("Qo'shmoqchi bo'lgan mahsulotingiz nomini kiriting")
    await Product.title.set()


@dp.message_handler(state=Product.title, user_id=ADMINS)
async def get_name(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data(
        {'title': title}
    )
    await message.answer("Batafsil malumot kiriting")
    await Product.next()

@dp.message_handler(state=Product.description, user_id=ADMINS)
async def get_desc(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {'description': description}
    )
    await message.answer("Mahsulot narxini kiriting (so'mda)")
    await Product.next()


@dp.message_handler(state=Product.price, user_id=ADMINS)
async def get_price(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data(
        {'price': price}
    )
    await message.answer("Mahsulot rasmini jo'nating")
    await Product.next()

@dp.message_handler(content_types=['photo'], state=Product.image, user_id=ADMINS)
async def get_image(message: types.Message, state: FSMContext):
    image = message.photo[-1].file_id
    await state.update_data(
        {'image': image}
    )
    cats = db.select_all_cats()
    s = ""
    for cat in cats:
        s += f"{cat[0]}. {cat[1]}\n"
    await message.answer(f"Mahsulot kategoriya raqamini kiriting\n\n{s}")
    await Product.next()


@dp.message_handler(state=Product.cat_id, user_id=ADMINS)
async def get_cat(message: types.Message, state: FSMContext):
    cat_id = int(message.text)
    data = await state.get_data()
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    image = data.get('image')
    date_1 = datetime.now()
    db.add_products(title=title, description=description, price=price, image=image, date=date_1, cat_id=cat_id)
    await message.answer(f"{title} mahsulotingiz muvaffaqiyatli qo'shildi")
    await state.finish()


@dp.message_handler(commands=['allproducts'], user_id=ADMINS)
async def get_all_prods(message: types.Message):
    prods = db.select_all_prods()
    for prod in prods:
        await message.answer_photo(photo=prod[4], caption=f"Nomi: {prod[1]}\nMa'lumot: {prod[2]}\nNarx: {prod[3]}\nSana: {prod[5]}")
    

