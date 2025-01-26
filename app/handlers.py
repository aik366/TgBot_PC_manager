from aiogram import Bot
from aiogram import F, Router
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, FSInputFile, Message, ReplyKeyboardRemove
from app.keyboards import inline_start_kb, inline_menu_kb, admin_kb, menu_kb
from datetime import datetime
import app.database as db
from random import randint
from config import MY_ID
from app.func import currency
import os

router = Router()


class Reg(StatesGroup):
    add_user = State()
    del_user = State()


class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        s = message.text.replace(",", ".").split()
        s2 = s[2].split(".")
        d_day = s2[0].isdigit() and 1 <= int(s2[0]) <= 31
        d_month = s2[0].isdigit() and 1 <= int(s2[0]) <= 12
        d_year = s2[0].isdigit() and 1900 <= int(s2[0]) <= datetime.now().year
        all_dmy = any([d_day, d_month, d_year])
        if len(s) == 3 and s[0].isalpha() and s[1].isalpha() and s[2].count('.') == 2 and all_dmy:
            return True
        return False


async def send_menu(chat_id, bot: Bot):
    await bot.send_animation(chat_id,
                             animation="https://i.pinimg.com/originals/08/e4/1c/08e41c2059323fad9b46ea6a18d1b8ef.gif",
                             caption="🎉Дни рождения", reply_markup=inline_start_kb)


async def menu_button(text, chat_id, bot: Bot):
    await bot.send_message(chat_id, text, reply_markup=inline_menu_kb)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в бота', reply_markup=menu_kb)


@router.message(Command('help'))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer('Вы нажали на кнопку помощи')
    await state.clear()


@router.message(Command('admin'))
async def cmd_admin(message: Message, state: FSMContext):
    if message.from_user.id != MY_ID:
        await message.answer('Вы не администратор', reply_markup=admin_kb)
        return
    await message.answer('Вы нажали на кнопку администратора', reply_markup=admin_kb)
    await state.clear()


@router.callback_query(F.data == "cancel")
async def add_cencel_data(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Действие отменено ✅")
    await state.clear()
    await call.answer()


@router.message(F.text == '❌Отмена')
async def add_cencel_text(message: Message, state: FSMContext):
    await message.answer("Действие отменено ✅")
    await state.clear()


@router.message(F.text == '🎉Дни рождения')
async def menu_dr(message: Message, state: FSMContext):
    await send_menu(message.chat.id, message.bot)
    await state.clear()


@router.message(F.text == "💵 Курсы валют")
async def cmd_kursi_valyut(message: Message, state: FSMContext):
    await message.answer(await currency())
    await state.clear()


@router.message(F.text == '🛠️Тест кнопка 1')
async def test_button1(message: Message, state: FSMContext):
    await message.answer("Кнопка 1 пока в разработке")
    await state.clear()


@router.message(F.text == '🛠️Тест кнопка 2')
async def test_button2(message: Message, state: FSMContext):
    await message.answer("Кнопка 2 пока в разработке")
    await state.clear()


@router.message(F.text == '💎Главное меню')
async def menu_main(message: Message, state: FSMContext):
    await message.answer("💎Главное меню", reply_markup=menu_kb)
    await state.clear()


@router.callback_query(F.data == "view_data")
async def add_user_viev(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f"{await db.db_select()}")
    await state.clear()
    await call.answer()


@router.callback_query(F.data == "gift")
async def file_open_images(call: CallbackQuery, state: FSMContext):
    img = FSInputFile(f'images/{randint(1, len(os.listdir("images")))}.jpg')
    await call.message.answer_photo(img)
    await state.clear()
    await call.answer()


@router.callback_query(F.data == "add_data")
async def add_user_data(call: CallbackQuery, state: FSMContext):
    await state.set_state(Reg.add_user)
    await call.message.answer('Введите Ф.И. и дату рождения\nФормате: дд.мм.гггг\nПример: 👇\nИванов Иван 30.01.2000')
    await call.answer()


@router.message(Reg.add_user, MyFilter(F.text))
async def add_user_reg(message: Message, state: FSMContext):
    await state.update_data(add_user=message.text)
    data_state = await state.get_data()
    if not await db.db_check(data_state['add_user']):
        await db.add_db(data_state['add_user'])
        await message.answer("Данные добавлены ✅")
    else:
        await message.answer("Такой запись уже есть")
    await state.clear()


@router.message(F.text == '🗑️Удалить данные')
async def delete_user(message: Message, state: FSMContext):
    await state.set_state(Reg.del_user)
    await message.answer('Введите Ф.И.\nПример: Иванов Иван')


@router.message(Reg.del_user)
async def delete_user_reg(message: Message, state: FSMContext):
    await state.update_data(del_user=message.text)
    data_state = await state.get_data()
    data_list = data_state['del_user'].split()
    await db.db_data_delete(data_list[0], data_list[1])
    await message.answer('Данные удалены')
    await state.clear()


@router.message(F.text == '33')
async def file_open(message: Message):
    with open("DATA/33.txt", "r") as file:
        f = file.read()
        await message.answer(f"{f}")


@router.message(F.text == 'log')
async def file_open_logo(message: Message):
    with open("DATA/logs.log", "r") as file:
        f = file.read()[-3000:]
        await message.answer(f"{f}")


@router.message(F.photo)
async def cmd_admin_photo(message: Message, bot: Bot):
    if message.from_user.id == MY_ID:
        file_name = f"images/{len(os.listdir('images')) + 1}.jpg"
        await bot.download(message.photo[-1], destination=file_name)
        await message.answer('Фото сохранено')


@router.callback_query(F.data == "menu")
async def cmd_menu(call: CallbackQuery):
    await send_menu(call.from_user.id, call.bot)
    await call.answer()


@router.callback_query(F.data == "main_menu")
async def cmd_menu_main(call: CallbackQuery, bot: Bot):
    await bot.send_message(call.from_user.id, "💎Главное меню", reply_markup=menu_kb)
    await call.answer()
