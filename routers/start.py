import os
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from filters.constants import (
    START_TEXT, HOME, MAIN_MENU
)
from keyboards.keyboards import admin_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        await message.answer(text=START_TEXT, reply_markup=admin_menu(message.from_user.id))
    else:
        await message.answer(text=START_TEXT, reply_markup=admin_menu(message.from_user.id))


@router.message(F.text == HOME)
async def home_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=MAIN_MENU, reply_markup=admin_menu(message.from_user.id))
