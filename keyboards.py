from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

api_create_or_cancel_kb = InlineKeyboardMarkup().row(
    InlineKeyboardButton(text='create', callback_data='api_create'),
    InlineKeyboardButton(text='cancel', callback_data='api_cancel'),
)

edit_or_delete_api = InlineKeyboardMarkup().row(
    InlineKeyboardButton(text='edit', callback_data='api_edit'),
    InlineKeyboardButton(text='delete', callback_data='api_delete'),
)


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('create new api'),
            KeyboardButton('check all api'),
        ]
    ],
    resize_keyboard=True, one_time_keyboard=True
)


def edit_api_kb(*api_data):
    print(api_data)
    return InlineKeyboardMarkup(row_width=1).add(
            KeyboardButton(f'change_name', callback_data='change_'),
    )
