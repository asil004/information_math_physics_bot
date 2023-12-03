from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database.database import get_subjects, get_theme, get_info, get_themes_only
from filters.constants import THEMES, INFO
from keyboards.keyboards import themes_kb

router = Router()


# state
class InputInfo(StatesGroup):
    theme = State()


@router.message()
async def get_themes(message: types.Message, state: FSMContext):
    subjects = get_subjects()
    themes = get_themes_only()
    if any(message.text in tpl for tpl in subjects):
        themes = get_theme(message.text)
        await message.answer(text=THEMES, reply_markup=themes_kb(themes))
    elif any(message.text in tpl for tpl in themes):
        info = get_info(message.text)
        await state.clear()
        for i in info:
            await message.answer_photo(photo=i[3], caption=INFO.format(fan=i[1], mavzu=i[2], info=i[4]),
                                       parse_mode="MARKDOWN")
