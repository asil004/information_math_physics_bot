import asyncio
import sqlite3 as sq

db = sq.connect(r'C:\Users\USER\Desktop\information_math_physics_bot\information.db')
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS information("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "subject TEXT,"
                "theme TEXT,"
                "picid INTEGER,"
                "info TEXT"
                ")")
    db.commit()


def get_subjects():
    obj = cur.execute("SELECT subject FROM information GROUP BY subject").fetchall()
    return obj


def get_info(theme):
    obj = cur.execute("SELECT * FROM information WHERE theme = ?", (theme,)).fetchall()
    return obj


def del_subjects(name):
    cur.execute("DELETE FROM information WHERE subject = ?", (name,))
    db.commit()
    if cur:
        return True
    else:
        return False


def del_themes(name):
    cur.execute("DELETE FROM information WHERE theme = ?", (name,))
    db.commit()
    if cur:
        return True
    else:
        return False


def get_theme(subject):
    obj = cur.execute("SELECT theme FROM information WHERE subject = ?", (subject,)).fetchall()
    return obj


def get_themes_only():
    obj = cur.execute("SELECT theme FROM information", ).fetchall()
    return obj


async def set_info(data):
    cur.execute("INSERT INTO information (subject, theme, picid, info) VALUES (?, ?, ?, ?)",
                (data['subject'], data['theme'], data['pic'], data['info']))
    db.commit()
    if cur.rowcount > 0:
        return True
    else:
        return False


async def close():
    db.close()


if __name__ == '__main__':
    data = {'subject': 'fdg', 'theme': 'dfg',
            'pic': 'AgACAgIAAxkBAANLZWuW19zTxv_jVSzqCc3iW8ATy6QAAifRMRsLnGBLh8lwWxxppsgBAAMCAANzAAMzBA', 'info': 'sdfs'}
    print(asyncio.run(get_subjects()))
