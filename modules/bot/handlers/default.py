from itertools import cycle

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from modules.bot.keyboards.default import name_kb, phone_number_kb, url_kb
from modules.db import DB

from config import admin_chats, admin_chats_tmp
from ...logger import log, logger


class Form(StatesGroup):
    wait_name = State()
    wait_phone_number = State()
    wait_city = State()
    wait_mail = State()

@log
async def start(message: types.Message, state: FSMContext):
    if not DB.exists(message.from_user.id):
        text = (
            "Салем!\n" 
            "Добро пожаловать на воркшоп по созданию дохода на крипте. " 
            "Сейчас мы распределим тебя в команду и назначим куратора✅"
        )
        await message.reply(text)

        text = "Как вас зовут?"
        msg = await message.answer(text, reply_markup=name_kb(message.from_user.full_name))
        
        await Form.wait_name.set()
        async with state.proxy() as data:
            data['msg'] = msg
    else:
        text = (
            "Тебе уже выдали приглашение!"
        )
        await message.answer(text)


async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    text = "В каком городе ты находишься?"
    msg = await message.answer(text)

    await Form.wait_city.set()
    async with state.proxy() as data:
        await message.delete()
        await data['msg'].delete()
        data['msg'] = msg


async def set_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text.capitalize()
    text = "Теперь отправь мне свою почту"
    msg = await message.answer(text)
    
    await Form.wait_mail.set()
    async with state.proxy() as data:
        await message.delete()
        await data['msg'].delete()
        data['msg'] = msg


async def set_mail(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mail'] = message.text

    text = "Какой твой номер телефона? (WhatsApp)"
    msg = await message.answer(text, reply_markup=phone_number_kb())
    
    await Form.wait_phone_number.set()
    async with state.proxy() as data:
        await message.delete()
        await data['msg'].delete()
        data['msg'] = msg


async def set_phone_number(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            phone_number = message.contact['phone_number'] if message.contact else message.text
            id = message.from_user.id
            username = message.from_user.username
            name = data['name']
            city = data['city']
            mail = data['mail']
            chat = next(admin_chats)
            group = admin_chats_tmp.index(chat) + 1
            DB.insert_new(int(id), str(username), str(name), str(city), str(mail), str(phone_number), int(group))

        invite_url = await message.bot.create_chat_invite_link(chat, member_limit=1, name=f"{name}@{username}")
        text = (f"Мы приглашаем тебя в группу, будь вежливым и не стесняйся задавать вопросы\)")
            
        msg = await message.answer(text, parse_mode=types.ParseMode.MARKDOWN_V2, reply_markup=url_kb("Войти в группу", invite_url.invite_link))
        async with state.proxy() as data:
            await message.delete()
            await data['msg'].delete()
            data['msg'] = msg
    except Exception as exc:
        logger.error(str(exc), exc_info=True)

def register_handlers_default(dp: Dispatcher):
    dp.register_message_handler(
        start,
        commands="start",
        state="*"
    )
    dp.register_message_handler(
        set_name,
        content_types=['text'],
        state=Form.wait_name
    )
    dp.register_message_handler(
        set_city,
        content_types=['text'],
        state=Form.wait_city
    )
    dp.register_message_handler(
        set_mail,
        content_types=['text'],
        state=Form.wait_mail
    )
    dp.register_message_handler(
        set_phone_number,
        content_types=['text', 'contact'],
        state=Form.wait_phone_number
    )
