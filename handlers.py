from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import Text
from films import films
from films import Films
from users import users

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('Хочу посмотреть фильм, посоветуй!')


async def get_random_film(message: types.Message):
    await message.answer(Films.beautify(films.df.sample(1).iloc[0]), parse_mode='HTML')


async def start(message: types.Message):
    users.add_user(message.from_user.id)
    await message.answer('Добро пожаловать!\nТеперь вы подписаны на новости по баскетболу', parse_mode='HTML',
                         reply_markup=keyboard)
