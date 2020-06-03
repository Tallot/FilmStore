import os
import settings 
import pytz
import sqlite3
from typing import Dict, List
from datetime import datetime

conn = sqlite3.connect(settings.DB_NAME)
cursor = conn.cursor()


def commit_txn(film_ids: List[int], user_id: int, total_cost: int): 
    film_ids_str = '|'.join([f'{item}' for item in film_ids])
    query_str = f'insert into transactions (film_ids, user_id, total_cost) values ("{film_ids_str}", {user_id}, {total_cost});'
    print(query_str)
    cursor.execute(query_str)
    conn.commit()


def get_user_films(user_id: int) -> List[int]:
    result = []
    cursor.execute(f'select (film_ids) from transactions where user_id={user_id}')
    rows = cursor.fetchall()
    for row in rows:
        result += row[0].split('|')

    return result


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime:
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.now(tz)
    return now


def _init_db():
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()

