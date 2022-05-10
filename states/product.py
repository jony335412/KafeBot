from aiogram.dispatcher.filters.state import StatesGroup, State

class Category(StatesGroup):
    title = State()

class Product(StatesGroup):
    title = State()
    description = State()
    price = State()
    image = State()
    cat_id = State()
