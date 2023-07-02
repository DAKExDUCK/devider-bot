from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)


def add_delete_button(kb: types.inline_keyboard = None):
    if kb is None:
        kb = InlineKeyboardMarkup()
    del_btn = InlineKeyboardButton('Delete', callback_data=f'delete')
    kb.add(del_btn)

    return kb


def phone_number_kb():
    btn_phone_number = KeyboardButton('Отправить номер телефона', request_contact=True)

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(btn_phone_number)

    return kb


def name_kb(name:str = None):
    if name is None:
        return None

    btn_phone_number = KeyboardButton(name, one_time_keyboard=True)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(btn_phone_number)

    return kb


def url_kb(name:str, url:str):
    btn = InlineKeyboardButton(name, url=url)

    kb = InlineKeyboardMarkup()
    kb.add(btn)

    return kb
