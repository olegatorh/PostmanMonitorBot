import asyncio
import email
import imaplib
import json
import logging

from imbox import Imbox
from aiogram import Bot, Dispatcher, executor, types
import sqlite3

from keyboards import setting_keyboard
from database import check_user, change_user_settings, get_all_users
from postmanInfo import return_data, run_monitor

API_TOKEN = '1846805595:AAHm8YcP4VIFtzL7B5-C02eQzlbSb8nwYa8'
con = sqlite3.connect('../bot.db')
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
old_response = []
sem = asyncio.Semaphore(1)


@dp.message_handler()
async def change_settings(message: types.Message):
    if message.text == "Auto sending: False":
        change_user_settings("auto_sending", True, message["from"].id)
        await message.reply("your settings changed", reply_markup=setting_keyboard(check_user(message)))
    if message.text == "Auto sending: True":
        change_user_settings("auto_sending", False, message["from"].id)
        await message.reply("your settings changed", reply_markup=setting_keyboard(check_user(message)))
    if message.text == "Only errors: True":
        change_user_settings("only_errors", False, message["from"].id)
        await message.reply("your settings changed", reply_markup=setting_keyboard(check_user(message)))
    if message.text == "Only errors: False":
        change_user_settings("only_errors", True, message["from"].id)
        await message.reply("your settings changed", reply_markup=setting_keyboard(check_user(message)))
    if message.text == "Full pm info: False":
        change_user_settings("full_info", True, message["from"].id)
        await message.reply("your settings changed", reply_markup=setting_keyboard(check_user(message)))
    if message.text == "Full pm info: True":
        change_user_settings("full_info", False, message["from"].id)
        await message.reply("your settings changed", reply_markup=setting_keyboard(check_user(message)))
    if message.text == "1c server info: True":
        change_user_settings("server_update_info", False, message["from"].id)
        await message.reply("your settings changed", reply_markup=setting_keyboard(check_user(message)))
    if message.text == "1c server info: False":
        change_user_settings("server_update_info", True, message["from"].id)
        await message.reply("your settings changed", reply_markup=setting_keyboard(check_user(message)))
    if message.text == "wasd":
        await message.reply("choose your settings", reply_markup=setting_keyboard(check_user(message)))


@dp.message_handler(commands=['settings'])
async def get_users(message: types.Message):
    await message.reply("choose your settings", reply_markup=setting_keyboard(check_user(message)))


async def postman_mailing():
    print("start postman")
    users = get_all_users()
    response = run_monitor()
    for i in users:
        if i[4] == 1 and i[5] == 1 and response['run']["info"]["status"] == "failed" and response is not None:
            await bot.send_message(i[1], return_data(response, i))
            print("sleep")
        if i[4] == 1 and i[5] == 0 and response is not None:
            await bot.send_message(i[1], return_data(response, i))
            print("sleep")
        if response is None:
            await bot.send_message(i[1], "something wrong we will try")
    print("пошта спить")
    await asyncio.sleep(3600)


async def email_mailing():
    print("start mail")
    print(old_response)
    users = get_all_users()
    one_c = await mail_onec_errors()
    if one_c is not None:
        print("шось нове")
        for i in users:
            if i[7] == 1:
                await bot.send_message(i[1], *one_c)
        await asyncio.sleep(1000)
    else:
        print("нічого нового")
        await asyncio.sleep(1000)


async def mail_onec_errors():
    global old_response
    with Imbox('imap.gmail.com',
               username='olegPetrob22@gmail.com',
               password='olegSuper57',
               ssl=True,
               ssl_context=None,
               starttls=False) as imbox:
        inbox_messages_from = imbox.messages(sent_from='Oleh.Pron@meest.com')
        for uid, message in inbox_messages_from:
            if message.body["plain"] == old_response:
                return None
            else:
                old_response += message.body["plain"]
                return *message.body["plain"],


async def main_loop():
    while True:
        await postman_mailing()
        await email_mailing()
        if False:
            telegram_chat.send_message('Something happened')
        pass


def callback_function(update, context):
    telegram_chat.send_message('Test')


async def main_telegram():
    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main_telegram(), name="Telegram listen task")
        loop.create_task(main_loop(), name="Main loop")
        loop.run_forever()
    finally:
        log.info("Shutting down ...")
        log.info("Updater running " + str(updater.running))
        updater.stop()
        pending = asyncio.all_tasks(loop=loop)
        for task in pending:
            task.cancel()

        loop.stop()
        loop.close()
