import os
import asyncio
from aiogram import F, Router, Dispatcher, types
from aiogram.enums import ChatAction
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import config
from keyboards import reply_kb as rp
from keyboards import inline_kb as ink
# from data_base.models import Admin
from data_base.database import get_db
from data_base.database import is_user_in_database
from config import ADMIN

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_tg_id = message.from_user.id

    if user_tg_id == config.ADMIN:
        await message.answer(f"Здравствуйте, Администратор!", reply_markup=rp.admin_panel)
    else:
        await message.answer("Здравствуй, мой милый друг! Это самый милый бот-помощник кофейни-пекарни Перемена!")
        async with get_db() as session:
            if await is_user_in_database(message.from_user.id, session):
                await message.answer("Что тебя интересует?", reply_markup=rp.main())
            else:
                await message.answer('Я вижу, что ты ещё не зарегестрирован и не учавствуешь в нашей программе лояльности, давай это исправим)',reply_markup=rp.register_button)


@start_router.message(Command('menu'))
async def cmd_catalog(message: types.Message):
    user_tg_id = message.from_user.id

    if user_tg_id == config.ADMIN:
        await message.answer(f"Действия для администратора", reply_markup=rp.admin_panel)
    else:
        await message.answer(f'Выберите интересующий вас раздел 👇', reply_markup=rp.main)

