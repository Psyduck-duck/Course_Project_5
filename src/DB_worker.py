import psycopg2

from abc import ABC, abstractmethod


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE {database_name.lower()}")
    except:
        pass
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name.lower(), **params)

    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR
            )
        ''')

    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                salary_down INTEGER,
                salary_up INTEGER,
                salary_currency VARCHAR,
                requirement VARCHAR,
                responsibility VARCHAR,
                employer_id INTEGER REFERENCES employers(employer_id)
            )
        ''')

    conn.commit()
    conn.close()


# class DBWorker(ABC):
#     """Абстрактный класс для работы с базой данных"""
#
#     @abstractmethod
#     def __init__(self) -> None:
#         pass
#
#     @abstractmethod
#     def create_db(self, db_name, params):
#         pass
#
#     # @abstractmethod
#     # def add_data_to_db(self, data):
#
#
#
# class DBWorkerPostgresql(DBWorker):
#     "Классс для работы с базой данных в postgresql"
#
#     def __init__(self, object: object) -> None:
#         """Конструктор для определения основных атрибутов"""
