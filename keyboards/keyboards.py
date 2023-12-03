import os

from aiogram.utils.keyboard import KeyboardBuilder, KeyboardButton, InlineKeyboardButton
from database.database import get_subjects
from filters.callbackdatas import DelSubjCallbackData, DelThemeCallbackData
from filters.constants import (
    ADMIN, ADD_INFO, HOME, CANCEL, DELETE_INFO, DEL_SUBJ, DEL_THEME, DELLL
)


# def menu():
#     builder = KeyboardBuilder(KeyboardButton)
#
#     # db get subjects
#     subjects = get_subjects()
#     if len(subjects) == 0:
#         return
#     for subject in subjects:
#         builder.add(
#             *[
#                 KeyboardButton(text=subject[1])
#             ]
#         )
#     builder.adjust(2)
#
#     return builder.as_markup(resize_keyboard=True)


def admin_menu(id):
    builder = KeyboardBuilder(KeyboardButton)

    # db get subjects
    subjects = get_subjects()

    for subject in subjects:
        builder.add(
            *[
                KeyboardButton(text=subject[0])
            ]
        )

    superuser = os.getenv('ADMIN')
    if int(superuser) == id:
        builder.add(
            *[
                KeyboardButton(text=ADMIN)
            ]
        )

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


# cancel
def cancel():
    builder = KeyboardBuilder(KeyboardButton)
    builder.add(
        *[
            KeyboardButton(text=CANCEL)
        ]
    )
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


# admin panel
def admin_panel():
    builder = KeyboardBuilder(KeyboardButton)
    builder.add(
        *[
            KeyboardButton(text=ADD_INFO),
            KeyboardButton(text=DELETE_INFO),
            KeyboardButton(text=HOME)
        ]
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def del_kb():
    builder = KeyboardBuilder(KeyboardButton)
    builder.add(
        *[
            KeyboardButton(text=DEL_SUBJ),
            KeyboardButton(text=DEL_THEME),
            KeyboardButton(text=HOME)
        ]
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


# themes
def themes_kb(data):
    builder = KeyboardBuilder(KeyboardButton)
    for theme in data:
        builder.add(
            *[
                KeyboardButton(text=theme[0])
            ]
        )
    builder.add(
        *[
            KeyboardButton(text=HOME)
        ]
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def del_info_ikb(name):
    builder = KeyboardBuilder(InlineKeyboardButton)
    builder.add(
        *[
            InlineKeyboardButton(text=DELLL, callback_data=DelSubjCallbackData(name=name).pack())
        ]
    )

    return builder.as_markup(resize_keyboard=True)


def del_theme_ikb(name):
    builder = KeyboardBuilder(InlineKeyboardButton)
    builder.add(
        *[
            InlineKeyboardButton(text=DELLL, callback_data=DelThemeCallbackData(name=name).pack())
        ]
    )

    return builder.as_markup(resize_keyboard=True)


def subjects_kb(data):
    builder = KeyboardBuilder(KeyboardButton)
    for i in data:
        builder.add(
            *[
                KeyboardButton(text=i[0])
            ]
        )
    builder.add(
        *[
            KeyboardButton(text=HOME)
        ]
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)
