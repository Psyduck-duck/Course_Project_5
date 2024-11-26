import json
import os.path

import psycopg2

from config import config
from data.__init__ import PATH_TO_DATA_DIRECTORY
from DB_worker import DBWorkerPostgresql
from src.API_system import ApiConnectionHHRU
from src.vacancies import VacancyHHRU


def main():
    "Вызывает слаженную работу всех функций"

    params = config()

    api_object = ApiConnectionHHRU()
    path_to_user_settings = os.path.join(PATH_TO_DATA_DIRECTORY, "user_settings.json")
    with open(path_to_user_settings) as file:
        api_object.employer_id_list = (json.load(file)).get("user_employer_id")

    print("Здравствуйте!")
    print("")
    db_name = ""
    special_simbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "[", "]", "{", "}", "/", "|", " "]
    while not db_name:
        db_name = input("Введите имя базы данных (существующие - для подключения, новое - для создания): ")
        for word in db_name:
            if word in special_simbols:
                db_name = None
    database_object = DBWorkerPostgresql(db_name, params)
    print("")
    try:
        database_object.get_all_vacancies()
    except ValueError:
        print(f"База данных не существует")
    print("")

    create_answer = ""
    while not create_answer:
        create_answer = input("Желаете создать/ пересоздать (с утерей данных) базу данных? ").lower()

        if create_answer not in ["yes", "y", "да", "no", "n", "нет"]:
            create_answer = None

    if create_answer in ["yes", "y", "да"]:
        database_object.create_database()
        print("")
        print(f"База данный {db_name} успешно создана")

    delete_answer = ""
    while not delete_answer:
        print("")
        delete_answer = input("Желаете удалить данные из таблиц? ")

        if delete_answer not in ["yes", "y", "да", "no", "n", "нет"]:
            delete_answer = None

    if delete_answer in ["yes", "y", "да"]:
        database_object.delete_data_from_database("vacancies")
        database_object.delete_data_from_database("employers")
        print("")
        print(f"Данные успешно удалены")

    save_data_answer = ""
    while not save_data_answer:
        print("")
        save_data_answer = input("Желаете добавить новые данные? ")

        if save_data_answer not in ["yes", "y", "да", "no", "n", "нет"]:
            save_data_answer = None

    if save_data_answer in ["yes", "y", "да"]:
        vacancies_list = api_object.get_vacancy_data("", 100)
        vacancies_objects_list = [VacancyHHRU(vacancy) for vacancy in vacancies_list]
        database_object.save_data_to_database(vacancies_objects_list)
        print("")
        print(f"Данные успешно добавлены")

    employers_vacancies_count_answer = ""
    while not employers_vacancies_count_answer:
        print("")
        employers_vacancies_count_answer = input("Желаете просмотреть кол-во вакансий на работодателя? ")

        if employers_vacancies_count_answer not in ["yes", "y", "да", "no", "n", "нет"]:
            employers_vacancies_count_answer = None

    if employers_vacancies_count_answer in ["yes", "y", "да"]:
        employers_vacancies_count = database_object.get_companies_and_vacancies_count()
        for employer in employers_vacancies_count:
            print(employer)

    get_all_vacancies_answer = ""
    while not get_all_vacancies_answer:
        print("")
        get_all_vacancies_answer = input("Желаете просмотреть все вакансии? ")

        if get_all_vacancies_answer not in ["yes", "y", "да", "no", "n", "нет"]:
            get_all_vacancies_answer = None

    if employers_vacancies_count_answer in ["yes", "y", "да"]:
        vacancies_list = database_object.get_all_vacancies()
        print("")
        for vacancy in vacancies_list:
            print(vacancy)

    avg_salary_answer = ""
    while not avg_salary_answer:
        print("")
        avg_salary_answer = input("Желаете посмотреть среднюю зарплату по вакансиям? ")
        if avg_salary_answer not in ["yes", "y", "да", "no", "n", "нет"]:
            avg_salary_answer = None

    if avg_salary_answer in ["yes", "y", "да"]:
        avg_salary = database_object.get_avg_salary()
        print("")
        print(avg_salary)

    vacancies_list_upper_avg_answer = ""
    while not vacancies_list_upper_avg_answer:
        print("")
        vacancies_list_upper_avg_answer = input("Желаете просмотреть все вакансии, зарплата которых выше средней? ")

        if vacancies_list_upper_avg_answer not in ["yes", "y", "да", "no", "n", "нет"]:
            vacancies_list_upper_avg_answer = None

    if vacancies_list_upper_avg_answer in ["yes", "y", "да"]:
        vacancies_list_upper_avg = database_object.get_vacancies_with_higher_salary()
        for vacancy in vacancies_list_upper_avg:
            print("")
            print(vacancy)

    vacancies_from_target_answer = ""
    while not vacancies_from_target_answer:
        print("")
        vacancies_from_target_answer = input("Желаете просмотреть все вакансии по ключевым словам в названии? ")

        if vacancies_from_target_answer not in ["yes", "y", "да", "no", "n", "нет"]:
            vacancies_from_target_answer = None

    if vacancies_from_target_answer in ["yes", "y", "да"]:
        print("")
        target_wodrs = input("Введите ключевые слова через ', ': ")
        target_words_list = target_wodrs.split(", ")
        vacancies_list_from_target = database_object.get_vacancies_with_keyword(target_words_list)
        for vacancy in vacancies_list_from_target:
            print(vacancy)
