import logging
import os
from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from database.database import set_info, get_subjects, get_theme, del_subjects, del_themes
from filters.callbackdatas import DelSubjCallbackData, DelThemeCallbackData
from filters.constants import (
    ADMIN, ADMIN_TEXT, INPUT_SUBJECT, ADD_INFO, INPUT_THEME, CANCEL,
    INPUT_PIC, INPUT_INFO, ERR_ADD, SUCC_ADD_INFO,
    DELETE_INFO, ADMIN_DEL, DEL_SUBJ, DEL_SUBJ_TEXT, DELL, SUCC_DEL_INFO, DEL_THEME, SUBJECTS_SELECT, DEL_THEME_TEXT,
    DELL_TH
)
from keyboards.keyboards import admin_panel, cancel, admin_menu, del_kb, del_info_ikb, subjects_kb, del_theme_ikb

router = Router()


class Info(StatesGroup):
    subject = State()
    theme = State()
    pic = State()
    info = State()


class DelTheme(StatesGroup):
    subj = State()
    theme = State()


@router.message(F.text == ADMIN)
async def admin(message: types.Message):
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        await message.answer(text=ADMIN_TEXT, reply_markup=admin_panel())


# add subject
@router.message(F.text == ADD_INFO)
async def add_subject(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Info.subject)
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        await message.answer(text=INPUT_SUBJECT, reply_markup=cancel())


@router.message(F.text == CANCEL)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Bekor qilindi.",
        reply_markup=admin_menu(message.from_user.id)
    )


@router.message(Info.subject)
async def add_theme(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(Info.theme)
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        await message.answer(text=INPUT_THEME, reply_markup=cancel())


@router.message(Info.theme)
async def add_pic(message: types.Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await state.set_state(Info.pic)
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        await message.answer(text=INPUT_PIC, reply_markup=cancel())


@router.message(Info.pic)
async def add_pic(message: types.Message, state: FSMContext):
    await state.update_data(pic=message.photo[0].file_id)
    await state.set_state(Info.info)
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        await message.answer(text=INPUT_INFO, reply_markup=cancel())


@router.message(Info.info)
async def add_info(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text)
    data = await state.get_data()
    await state.clear()

    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        res = await set_info(data=data)
        if res:
            await message.answer(text=SUCC_ADD_INFO, reply_markup=admin_menu(message.from_user.id))
        else:
            await message.answer(text=ERR_ADD, reply_markup=admin_menu(message.from_user.id))


# delete
@router.message(F.text == DELETE_INFO)
async def delete_info(message: types.Message):
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        await message.answer(text=ADMIN_DEL, reply_markup=del_kb())


@router.message(F.text == DEL_SUBJ)
async def delete_sub(message: types.Message):
    superuser = os.getenv('ADMIN')
    subjects = get_subjects()
    if str(message.from_user.id) in superuser:
        await message.answer(text=DEL_SUBJ_TEXT)
        for subject in subjects:
            await message.answer(text=DELL.format(fan=subject[0]), reply_markup=del_info_ikb(subject[0]))


@router.message(F.text == DEL_THEME)
async def delete_theme_sbj(message: types.Message, state: FSMContext):
    await state.set_state(DelTheme.subj)
    superuser = os.getenv('ADMIN')
    subjects = get_subjects()
    if str(message.from_user.id) in superuser:
        await message.answer(text=SUBJECTS_SELECT, reply_markup=subjects_kb(subjects))


@router.message(DelTheme.subj)
async def delete_theme(message: types.Message, state: FSMContext):
    await state.set_state(DelTheme.theme)
    superuser = os.getenv('ADMIN')
    themes = get_theme(message.text)
    if str(message.from_user.id) in superuser:
        await message.answer(text=DEL_THEME_TEXT)
        for theme in themes:
            await message.answer(text=DELL_TH.format(mavzu=theme[0]), reply_markup=del_theme_ikb(theme[0]))
    await state.clear()


# callback datas
@router.callback_query(DelSubjCallbackData.filter())
async def dell_subj_callback(query: types.CallbackQuery, callback_data: CallbackData):
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        dell = del_subjects(callback_data.name)
        if dell:
            await query.message.answer(text=SUCC_DEL_INFO)
        else:
            await query.message.answer(text=ERR_ADD)


@router.callback_query(DelThemeCallbackData.filter())
async def dell_theme_callback(query: types.CallbackQuery, callback_data: CallbackData):
    superuser = os.getenv('ADMIN')
    if str(message.from_user.id) in superuser:
        dell = del_themes(callback_data.name)
        if dell:
            await query.message.answer(text=SUCC_DEL_INFO)
        else:
            await query.message.answer(text=ERR_ADD)


@router.message()
async def dont_know(message: types.Message):
    await message.answer(text="Kechirasiz sizni tushunmayabman 😕")