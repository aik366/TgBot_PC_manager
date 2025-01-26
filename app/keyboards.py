from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

menu_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🎉Дни рождения'),
                                         KeyboardButton(text='💵 Курсы валют')],
                                        [KeyboardButton(text='🛠️Тест кнопка 1'),
                                         KeyboardButton(text='🛠️Тест кнопка 2')]
                                        ], resize_keyboard=True)

admin_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🗑️Удалить ID'),
                                          KeyboardButton(text='🗑️Удалить данные'), ],
                                         [KeyboardButton(text='Данные по ID'),
                                          KeyboardButton(text='❌Отмена')], ], resize_keyboard=True)

inline_start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🆕Добавить данные", callback_data="add_data"),
     InlineKeyboardButton(text="👁️Просмотр данных", callback_data="view_data")],
    [InlineKeyboardButton(text="🎁Открытки", callback_data="gift"),
     InlineKeyboardButton(text="❌Отмена", callback_data="cancel")],])

inline_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎉Меню ДР", callback_data="menu"),
     InlineKeyboardButton(text="💎Главное меню", callback_data="main_menu")]])
