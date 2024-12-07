from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import Message
from aiogram.types import FSInputFile

import config
from data_base.database import get_db, update_coffees_count, check_for_free_coffee, get_or_create_bonus
from aiogram.filters import Command
from data_base.models import Base, User, Bonus
from sqlalchemy.future import select
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN
from data_base.models import Base, User, Bonus



admin_handlers = Router()

bot = Bot(config.BOT_TOKEN)
class BuyState(StatesGroup):
    phone = State()


input_file = FSInputFile('img/help.jpg')

async def get_users():
    async with get_db() as session:
        # Используем execute для выполнения запроса
        result = await session.execute(select(User.id))

        # Преобразуем результат в список
        users = result.scalars().all()

    return users

# Функция для отправки сообщения пользователям
async def send_message(user_id, message_text):
    try:
        await bot.send_message(chat_id=user_id, text=message_text)
        print(f"Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        print(f"Произошла ошибка при отправке сообщения пользователю {user_id}: {e}")

# Команда для запуска рассылки
@admin_handlers.message(F.text == "Сделать рассылку")
async def start_sending(message: types.Message):
    if message.from_user.id == config.ADMIN:  # Замените АДМИН_ID на ID вашего аккаунта
        await message.answer("Введите текст сообщения для рассылки:")
        @admin_handlers.message()
        async def handle_message_input(msg: types.Message):
            if msg.from_user.id ==config.ADMIN:
                message_text = msg.text
                users_to_send = await get_users()  # Получаем список пользователей из БД
                for user in users_to_send:
                    await send_message(user, message_text)
                await msg.answer("Рассылка завершена!")
            else:
                await msg.answer("У вас нет прав для выполнения этой команды.")
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

async def get_user_by_phone(phone_number: str):
    """Получает пользователя по номеру телефона"""
    async with get_db() as session:
        result = await session.execute(select(User).where(User.phone_number == phone_number))
        user = result.scalar_one_or_none()
        return user




@admin_handlers.message(F.text == "Начислить бонусы")
async def buy_start_handler(message: Message, state: FSMContext):
    await state.set_state(BuyState.phone)
    await message.reply("Пожалуйста, введите номер телефона пользователя:")

# Хендлер для получения номера телефона
@admin_handlers.message(BuyState.phone)
async def buy_process_phone_handler(message: Message, state: FSMContext):
    phone_number = message.text.strip()
    user = await get_user_by_phone(phone_number)  # Обратите внимание на await перед вызовом функции
    if not user:
        await message.reply(f"Пользователь с номером {phone_number} не найден.")
        await state.clear()  # Используем clear вместо finish, так как finish устарел
        return

    async with get_db() as session:
        await update_coffees_count(user.id, session=session)  # Передаем user.id вместо message.from_user.id
        free_coffee = await check_for_free_coffee(user.id, session=session)
        if free_coffee:
            await message.reply("Поздравляем! Вы можете сделать бесплатную чашку кофе.")
        else:
            await message.reply("Начисление бонусов прошло успешно, не забудьте пожелать хорошего дня!.")

    await state.clear()

@admin_handlers.message(F.text == "Помощь")
async def admin_help(message: types.Message):
    await message.answer_photo(input_file)


