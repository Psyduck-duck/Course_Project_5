import pytest

from src.DB_worker import DBWorkerPostgresql

from src.vacancies import VacancyHHRU

from config import config

params = config()

@pytest.fixture
def some_vacancy_dict_1():
    return {
        "id": "1",
        "name": "test",
        "salary": {
            "from": 1,
            "to": 2,
            "currency": "test",
        },
        "alternate_url": "https://test.ru",
        "snippet": {"requirement": "test", "responsibility": "test"},
        "employer": {"id": 1, "name": "name_1"},
    }

@pytest.fixture
def some_vacancy_dict_2():
    return {
        "id": "2",
        "name": "test",
        "salary": {
            "from": 1,
            "to": 2,
            "currency": "test",
        },
        "alternate_url": "https://test_2.ru",
        "snippet": {"requirement": "test", "responsibility": "test"},
        "employer": {"id": 2, "name": "name_2"},
    }

@pytest.fixture
def vacancy_object_1(some_vacancy_dict_1):
    return VacancyHHRU(some_vacancy_dict_1)

@pytest.fixture
def vacancy_object_2(some_vacancy_dict_2):
    return VacancyHHRU(some_vacancy_dict_2)

def test_create_database():

    database_object = DBWorkerPostgresql("test", params)
    database_object.create_database()
    database_object.delete_data_from_database("employers")
    result = database_object.get_all_vacancies()
    assert result == []

def test_save_data_to_database(vacancy_object_1, vacancy_object_2):

    database_object = DBWorkerPostgresql("test", params)
    database_object.save_data_to_database([vacancy_object_1, vacancy_object_2])

    result_companies_and_vacancies_count_method = database_object.get_companies_and_vacancies_count()
    assert result_companies_and_vacancies_count_method == [("name_2", 1), ("name_1", 1)]




