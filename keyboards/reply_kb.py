from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='FAQ')],
                                     [KeyboardButton(text='Меню'),
                                     KeyboardButton(text='Сайт')],
                                     [KeyboardButton(text='Бонусы')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправь номер',
                                                        request_contact=True)]],
                               resize_keyboard=True)

admin_panel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начислить бонусы')],
                                     [KeyboardButton(text='Сделать рассылку'), KeyboardButton(text='Помощь')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

register_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Регистрация")]],
                                      resize_keyboard=True)