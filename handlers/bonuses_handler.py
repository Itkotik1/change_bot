from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import Message
from data_base.database import get_db, update_coffees_count, check_for_free_coffee, get_or_create_bonus
from aiogram.filters import Command


bonuses_handler = Router()

# Хендлер для обработки команды /balance
@bonuses_handler.message(F.text == 'Бонусы')
async def balance_handler(message: Message):
    async with get_db() as session:
        free_coffee = await check_for_free_coffee(message.from_user.id, session=session)
        bonus = await get_or_create_bonus(message.from_user.id, session)
        if free_coffee:
            await message.reply("Поздравляем! Вы можете получить бесплатную чашку кофе.")
        else:
            await message.reply(f"Ваш баланс: {bonus.coffees_count} чашек кофе.")


