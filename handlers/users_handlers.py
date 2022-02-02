from aiogram import Dispatcher
from aiogram.types import Message

from create_bot import dp
from keyboards import start_kb


@dp.message_handler(commands="start")
async def start_menu(message: Message):
    await message.reply(text="рухайтесь по меню", reply_markup=start_kb)


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(start_menu, commands="start")
