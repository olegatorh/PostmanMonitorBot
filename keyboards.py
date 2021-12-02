from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def setting_keyboard(user_setting_info):
    button1 = KeyboardButton(f'Auto sending: {bool(user_setting_info[0])}')
    button2 = KeyboardButton(f'Only errors: {bool(user_setting_info[1])}')
    button3 = KeyboardButton(f'Full pm info: {bool(user_setting_info[2])}')
    button4 = KeyboardButton(f'1c server info: {bool(user_setting_info[3])}')
    settings_keyboard = ReplyKeyboardMarkup().add(
        button1).add(button2).add(button3).add(button4)
    return settings_keyboard
