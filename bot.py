from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters.builtin import Text
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types.bot_command import BotCommand
import asyncio
from config import TOKEN
from handlers import start, get_random_film
from newsSoup import news, newsDF
from users import users



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def send_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command='/start', description='Начать работу с ботом')
        ]
    )


async def parser():
    while True:
        await asyncio.sleep(10)
        df = news.update()
        for index, n in df.iterrows():
            message = newsDF.beautify(n)
            for user in users.get_user_list():
                try:
                    await bot.send_message(user, message, parse_mode="HTML")
                except BotBlocked:
                    users.delete_user(user)
            await asyncio.sleep(5)


async def main():
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(get_random_film, commands='get_random_film')
    dp.register_message_handler(get_random_film, Text(equals='Хочу посмотреть фильм, посоветуй!',
                                                               ignore_case=True))
    await send_commands(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(parser())

    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
