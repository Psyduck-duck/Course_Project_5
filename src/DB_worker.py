from typing import List, Tuple, Any

import psycopg2

from abc import ABC, abstractmethod
from vacancies import VacancyHHRU


# def create_database(database_name: str, params: dict):
#     """Создание базы данных и таблиц для сохранения данных о каналах и видео."""
#
#     conn = psycopg2.connect(dbname="postgres", **params)
#     conn.autocommit = True
#     cur = conn.cursor()
#
#     try:
#         cur.execute(f"DROP DATABASE {database_name.lower()}")
#     except:
#         pass
#     cur.execute(f"CREATE DATABASE {database_name}")
#
#     cur.close()
#     conn.close()
#
#     conn = psycopg2.connect(dbname=database_name.lower(), **params)
#
#     with conn.cursor() as cur:
#         cur.execute('''
#             CREATE TABLE employers (
#                 employer_id INTEGER PRIMARY KEY,
#                 name VARCHAR
#             )
#         ''')
#
#     with conn.cursor() as cur:
#         cur.execute('''
#             CREATE TABLE vacancies (
#                 vacancy_id SERIAL PRIMARY KEY,
#                 name VARCHAR NOT NULL,
#                 salary_down INTEGER,
#                 salary_up INTEGER,
#                 salary_currency VARCHAR,
#                 requirement VARCHAR,
#                 responsibility VARCHAR,
#                 employer_id INTEGER REFERENCES employers(employer_id)
#             )
#         ''')
#
#     conn.commit()
#     conn.close()


class DBWorker(ABC):
    """Абстрактный класс для работы с базой данных"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_database(self):
        pass

    @abstractmethod
    def save_data_to_database(self, vacancy_object):
        pass


class DBWorkerPostgresql(DBWorker):
    "Классс для работы с базой данных в postgresql"

    def __init__(self, db_name: str, params: dict) -> None:
        """Конструктор для определения основных атрибутов"""

        self.__db_name = db_name
        self.__params = params
        self.__vacancies_id_list = []
        self.__employers_id_list = []

    def create_database(self):
        """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {self.__db_name.lower()}")
        cur.execute(f"CREATE DATABASE {self.__db_name}")

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=self.__db_name.lower(), **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    name VARCHAR
                )
            """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    salary_down INTEGER,
                    salary_up INTEGER,
                    salary_currency VARCHAR,
                    requirement VARCHAR,
                    responsibility VARCHAR,
                    url VARCHAR,
                    employer_id INTEGER REFERENCES employers(employer_id) ON DELETE CASCADE
                )
            """
            )

        conn.commit()
        conn.close()

    def save_data_to_database(self, vacancy_objects_list: list[VacancyHHRU]) -> None:
        """Метод для добавления данных (списка объектов класса Vacancy в таблицы БД"""

        conn = psycopg2.connect(dbname=self.__db_name.lower(), **self.__params)

        with conn.cursor() as cur:
            cur.execute("SELECT vacancy_id FROM vacancies")
            vacancies_id_list = cur.fetchall()
            for vacancy in vacancies_id_list:
                if vacancy[0] not in self.__vacancies_id_list:
                    self.__vacancies_id_list.append(vacancy[0])

            cur.execute("SELECT employer_id FROM employers")
            employer_id_list = cur.fetchall()
            for employer_id in employer_id_list:
                if employer_id[0] not in self.__employers_id_list:
                    self.__employers_id_list.append(employer_id[0])

        conn.commit()

        with conn.cursor() as cur:
            for vacancy in vacancy_objects_list:
                if vacancy.employer_id not in self.__employers_id_list:
                    try:
                        cur.execute(
                            """
                            INSERT INTO employers (employer_id, name)
                            VALUES (%s, %s)
                            """,
                            (vacancy.employer_id, vacancy.employer_name),
                        )
                    except Exception as error:
                        print(f"Error: {error}")
                    self.__employers_id_list.append(vacancy.employer_id)

                if int(vacancy.id) not in self.__vacancies_id_list:
                    try:
                        cur.execute(
                            """
                            INSERT INTO vacancies (vacancy_id, name, salary_down, salary_up, salary_currency, requirement, responsibility, url, employer_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                vacancy.id,
                                vacancy.name,
                                vacancy.salary_down,
                                vacancy.salary_up,
                                vacancy.salary_currency,
                                vacancy.requirement,
                                vacancy.responsibility,
                                vacancy.url,
                                vacancy.employer_id,
                            ),
                        )
                    except Exception as error:
                        print(f"Error: {error}")

                    self.__vacancies_id_list.append(int(vacancy.id))

        conn.commit()
        conn.close()

    def delete_data_from_database(self, table_name: str) -> None:
        """Метод для удаления данных из таблицы"""

        conn = psycopg2.connect(dbname=self.__db_name.lower(), **self.__params)

        with conn.cursor() as cur:

            if table_name in ["vacancies", "employers"]:
                cur.execute(f"DELETE FROM {table_name}")
            else:
                raise ValueError(f"Table {table_name} not found")

        if table_name == "vacancies":
            self.__vacancies_id_list = list()
        elif table_name == "employers":
            self.__employers_id_list = list()
            self.__vacancies_id_list = list()

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """получает список всех компаний и количество вакансий у каждой компании"""

        conn = psycopg2.connect(dbname=self.__db_name.lower(), **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.name, COUNT(*) FROM vacancies
                    INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                    GROUP BY employers.name
                    ORDER BY COUNT(*) DESC
                    """
            )
            employers_vacancies_count = cur.fetchall()

        conn.commit()
        conn.close()

        return employers_vacancies_count

    def get_all_vacancies(self) -> list[tuple]:
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""

        conn = psycopg2.connect(dbname=self.__db_name.lower(), **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.name AS employer_name, vacancies.name, salary_down, salary_up, salary_currency, url FROM vacancies
                    INNER JOIN employers USING (employer_id)"""
            )

            vacancies_list = cur.fetchall()

        conn.commit()
        conn.close()

        return vacancies_list

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""

        conn = psycopg2.connect(dbname=self.__db_name.lower(), **self.__params)

        with conn.cursor() as cur:
            cur.execute(" SELECT AVG(salary_down) AS avg_salary FROM vacancies")

            avg_salary_tuple = cur.fetchall()
            avg_salary = round(avg_salary_tuple[0][0], 2)

        conn.commit()
        conn.close()

        return avg_salary

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        avg_salary = self.get_avg_salary()

        conn = psycopg2.connect(dbname=self.__db_name.lower(), **self.__params)

        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies
                            WHERE salary_down > {avg_salary}
                            """
                        )

            vacancies_list_upper_avg = cur.fetchall()

        conn.commit()
        conn.close()

        return vacancies_list_upper_avg
