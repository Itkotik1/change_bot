from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime
import keyboards.reply_kb as rp
from data_base.database import is_user_in_database
from data_base.database import get_db
from data_base.models import User
from sqlalchemy.exc import IntegrityError
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery
class RegistrationStates(StatesGroup):
    name = State()
    birth_date = State()
    phone_number = State()

# Создаем роутер для обработки сообщений
registration_router = Router()


# Запрашиваем имя пользователя
@registration_router.message(F.text == "Регистрация")
async def register(message: types.Message, state: FSMContext):
    async with get_db() as session:
        if await is_user_in_database(message.from_user.id, session):
            await message.answer("Пользователь уже зарегистрирован.")
        else:
            await state.set_state(RegistrationStates.name)
            await message.answer('Отлично! Для начала расскажите мне Ваше имя. 😊')


@registration_router.message(RegistrationStates.name)
async def register_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegistrationStates.birth_date)
    await message.answer('Прекрасное имя, Иван! Теперь, пожалуйста, укажите Вашу дату рождения. \n'
                         'Формат ввода: ДД.ММ.ГГГГ.')


@registration_router.message(RegistrationStates.birth_date)
async def process_birthdate(message: types.Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        await state.update_data(birth_date=birth_date)  # Обновляем данные в состоянии
        await message.answer(f"Спасибо за предоставленную информацию, {message.from_user.first_name}.\n"
                             f"И наконец, оставьте, пожалуйста, Ваш контактный номер телефона.")
        await state.set_state(RegistrationStates.phone_number)
        await message.answer('Отправьте ваш номер телефона', reply_markup=rp.get_number)
    except ValueError:
        await message.answer(f"Неверная дата рождения. Попробуйте снова ввести дату в формате ДД.ММ.ГГГГ")


# Обрабатываем введенный номер телефона
@registration_router.message(RegistrationStates.phone_number, F.contact)
async def register_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    data = await state.get_data()
    # Получаем данные из состояния
    name = data.get('name')
    birth_date = data.get('birth_date')
    phone_number = data.get('phone_number')

    # Сохраняем данные в базу данных
    async with get_db() as db_session:
        async with db_session.begin():
            new_user = User(id=message.from_user.id, name=name, birth_date=birth_date, phone_number=phone_number)
            db_session.add(new_user)
            await db_session.commit()

    await message.answer("Регистрация завершена! Спасибо!",
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()