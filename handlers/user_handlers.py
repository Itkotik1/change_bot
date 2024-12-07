import os
import asyncio
from aiogram import F, Router, Dispatcher, types
from aiogram.enums import ChatAction
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.types import FSInputFile

import config
from keyboards import reply_kb as rp
from keyboards import inline_kb as ink
from data_base.database import get_db
from data_base.database import is_user_in_database
from config import ADMIN

user_router = Router()

input_file = FSInputFile('img/help.jpg')

@user_router.message(F.text == 'FAQ')
async def about(message: types.Message):
    await message.answer('Название: Кофейня-пекарня "Перемена"\n'
                         'Телефон: 8999999999\n'
                         'Адрес: ул. Рязанский проспект 99A\n'
                         'Время работы: 9:00-20:00\n')

@user_router.message(F.text == 'Сайт')
async def show_website(message: types.Message):
    website_url = "https://onepricecoffee.com/"
    await message.answer(f"Вот ссылка на наш уютный-кофейный сайт: {website_url}")

@user_router.message(F.text == 'Меню')
async def menu(message: types.Message):
    await message.answer('Сделайте выбор: ', reply_markup=ink.menu)

@user_router.callback_query(F.text.in_(['drink', 'bakery', 'sezon']))
async def handle_menu(callback_query: CallbackQuery):
    data = callback_query.data

    if data == 'drink':
        await callback_query.answer('Вы выбрали кофе!')

    elif data == 'bakery':
        await callback_query.answer('Вы выбрали выпечку!.')
    elif data == 'sezon':
        await callback_query.answer('Вы выбрали сезонное меню!')