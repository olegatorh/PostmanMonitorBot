from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from create_bot import dp
from database import add_api_to_database, get_all_api, delete_api
from keyboards import api_create_or_cancel_kb, edit_or_delete_api, edit_api_kb


class API(StatesGroup):
    api_name = State()
    api_url = State()
    api_notation = State()


class ApiEditStuff(StatesGroup):
    edit_api_name = State()
    edit_api_url = State()
    edit_api_notation = State()



#                                                                                cancel api creating anywhere
# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
# async def cancel_handler(message: Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply("OK")


@dp.message_handler(text="create new api")
async def create_new_api(message: Message):
    await message.answer('set name of your api')
    await API.api_name.set()


@dp.message_handler(text="check all api")
async def check_all_api(message: Message):
    response = get_all_api()
    [await message.answer(
        f"{i[1]} \n\nid: {i[0]};\napi name: {i[1]};\napi url: {i[2]};\napi notation: {i[3]};\n\ncreated: {i[4]};",
        reply_markup=edit_or_delete_api) for i in response]


@dp.message_handler(state=API.api_name)
async def api_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_name'] = message.text
    await message.answer(f'ok, API name: {message.text}, now set api url')
    await API.next()


@dp.message_handler(state=API.api_url)
async def api_url(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_url'] = message.text
    await message.answer(f'ok, API url: {message.text}, now set api notation')
    await API.next()


@dp.message_handler(state=API.api_notation)
async def api_notation(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['api_notation'] = message.text
    data = await state.get_data()
    await message.answer("check are everything is ok")
    await message.answer(
        f'\n API name: {data["api_name"]};\n API url: {data["api_url"]};\n API notation: {data["api_notation"]};\n')
    await message.answer("if all is right click ok or cancel", reply_markup=api_create_or_cancel_kb)


@dp.callback_query_handler(text=["api_delete", "api_edit"])
async def check_api_callback(callback_query: CallbackQuery):
    if callback_query.data == "api_delete":
        await API.next()
        delete_api(callback_query.message.text.split(' ')[0])
        await callback_query.message.answer(f"{callback_query.message.text.split(' ')[0]} deleted!")
    if callback_query.data == "api_edit":
        await callback_query.message.answer(callback_query.message.text, reply_markup=edit_api_kb)


@dp.callback_query_handler(text=["edit_api_name", "edit_api_delete", "edit_api_notation"])
async def edit_api(callback_query: CallbackQuery):
    if callback_query.data == "edit_api_name":
        await API.state =
    if callback_query.data == "edit_api_delete":
        await API.next()
    if callback_query.data == "edit_api_notation":
        await API.next()


@dp.message_handler(state=ApiEditStuff.edit_api_name)
async def edit_api_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_api_name'] = message.text
    data = await state.get_data()
    print(f"edit_api_name: {data}")


@dp.message_handler(state=ApiEditStuff.edit_api_url)
async def edit_api_url(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_api_url'] = message.text
    data = await state.get_data()
    print(f"edit_api_url: {data}")


@dp.message_handler(state=ApiEditStuff.edit_api_notation)
async def edit_api_notation(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_api_notation'] = message.text
    data = await state.get_data()
    print(f"edit_api_notation: {data}")


@dp.callback_query_handler(text=["api_cancel", "api_create"], state="*")
async def process_callback_api(callback_query: CallbackQuery, state: FSMContext):
    current_state = await state.get_data()
    if callback_query.data == "api_create":
        if current_state is None:
            await callback_query.message.answer("try again create new api, /new_api")
            return
        new_api = add_api_to_database(current_state)
        await state.finish()
        await callback_query.message.answer(new_api) if type(new_api) == str else (
            await callback_query.message.answer("OK, added")
            , await callback_query.message.answer(
                f"New API\n\nid: {new_api[0]};\napi name: {new_api[1]};\napi url: {new_api[2]};\napi notation: {new_api[3]};\n\ncreated: {new_api[4]};"))

    if callback_query.data == "api_cancel":
        if current_state is None:
            await callback_query.message.answer("try again create new api, /new_api")
            return
        await state.finish()
        await callback_query.message.answer("OK, cancel")


def register_handlers_api(dp: Dispatcher):
    dp.register_message_handler(create_new_api, text='new_api')
    dp.register_message_handler(api_name, state=API.api_name)
    dp.register_message_handler(api_url, state=API.api_url)
    dp.register_message_handler(api_notation, state=API.api_notation)
    dp.register_message_handler(process_callback_api, text=["api_cancel", "api_create"], state="*")
    dp.register_message_handler(process_callback_api, text=["api_cancel", "api_create"], state="*")
    dp.register_message_handler(check_api_callback, text=["api_delete", "api_edit"])
