import pytest

from src.vacancies import VacancyHHRU


@pytest.fixture
def some_vacancy_dict():
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
    }


def test_VacancyHHRU(some_vacancy_dict):
    object = VacancyHHRU(some_vacancy_dict)
    assert object.id == "1"
    assert object.name == "test"
    assert object.salary_down == 1
    assert object.salary_up == 2
    assert object.salary_currency == "test"
    assert object.url == "https://test.ru"
    assert object.requirement == "test"
    assert object.responsibility == "test"


def test_VacancyHHRU_invalid_id(some_vacancy_dict):
    some_vacancy_dict["id"] = 1
    with pytest.raises(TypeError):
        VacancyHHRU(some_vacancy_dict)
    some_vacancy_dict["id"] = None
    with pytest.raises(ValueError):
        VacancyHHRU(some_vacancy_dict)


def test_VacancyHHRU_invalid_name(some_vacancy_dict):

    some_vacancy_dict["name"] = None
    with pytest.raises(ValueError):
        VacancyHHRU(some_vacancy_dict)
    some_vacancy_dict["name"] = 123
    with pytest.raises(TypeError):
        VacancyHHRU(some_vacancy_dict)


def test_VacancyHHRU_None_salary(some_vacancy_dict):

    some_vacancy_dict["salary"] = None
    object_2 = VacancyHHRU(some_vacancy_dict)
    assert object_2.salary_down == None
    assert object_2.salary_up == None
    assert object_2.salary_currency == None


def test_VacancyHHRU_invalid_salary(some_vacancy_dict):

    some_vacancy_dict["salary"]["from"] = "1"
    # with pytest.raises(TypeError):
    #     VacancyHHRU(some_vacancy_dict)
    object = VacancyHHRU(some_vacancy_dict)
    assert object.salary_down == None
    some_vacancy_dict["salary"]["from"] = 1

    some_vacancy_dict["salary"]["to"] = "2"
    # with pytest.raises(TypeError):
    #     VacancyHHRU(some_vacancy_dict)
    object_1 = VacancyHHRU(some_vacancy_dict)
    assert object_1.salary_up == None
    some_vacancy_dict["salary"]["to"] = 2

    some_vacancy_dict["salary"]["currency"] = 123
    with pytest.raises(TypeError):
        VacancyHHRU(some_vacancy_dict)


def test_VacancyHHRU_invalid_url(some_vacancy_dict):

    some_vacancy_dict["alternate_url"] = "htp//hh.ru"
    with pytest.raises(ValueError):
        VacancyHHRU(some_vacancy_dict)


def test_VacancyHHRU_invalid_snippet(some_vacancy_dict):

    some_vacancy_dict["snippet"]["requirement"] = 123
    # with pytest.raises(TypeError):
    #     VacancyHHRU(some_vacancy_dict)
    object = VacancyHHRU(some_vacancy_dict)
    assert object.requirement == None
    some_vacancy_dict["snippet"]["requirement"] = "test"

    some_vacancy_dict["snippet"]["responsibility"] = 123
    # with pytest.raises(TypeError):
    #     VacancyHHRU(some_vacancy_dict)
    object = VacancyHHRU(some_vacancy_dict)
    assert object.responsibility == None
    some_vacancy_dict["snippet"]["responsibility"] = "test"

    some_vacancy_dict["snippet"] = None
    with pytest.raises(ValueError):
        VacancyHHRU(some_vacancy_dict)


def test_vacancy_math_funcs():
    object_1 = VacancyHHRU(
        {
            "id": "1",
            "name": "test",
            "salary": {
                "from": 1,
                "to": 2,
                "currency": "test",
            },
            "alternate_url": "https://test.ru",
            "snippet": {"requirement": "test", "responsibility": "test"},
        }
    )
    object_2 = VacancyHHRU(
        {
            "id": "1",
            "name": "test",
            "salary": {
                "from": 1,
                "to": 3,
                "currency": "test",
            },
            "alternate_url": "https://test.ru",
            "snippet": {"requirement": "test", "responsibility": "test"},
        }
    )
    object_3 = VacancyHHRU(
        {
            "id": "1",
            "name": "test",
            "salary": {
                "from": 3,
                "to": 5,
                "currency": "test",
            },
            "alternate_url": "https://test.ru",
            "snippet": {"requirement": "test", "responsibility": "test"},
        }
    )

    assert object_1 <= object_2
    assert object_1 < object_3
    assert object_3 > object_2
    assert object_2 >= object_1
