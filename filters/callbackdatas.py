from aiogram.filters.callback_data import CallbackData


class DelSubjCallbackData(CallbackData, prefix='del_subj'):
    name: str


class DelThemeCallbackData(CallbackData, prefix='del_theme'):
    name: str
