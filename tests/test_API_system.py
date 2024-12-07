from unittest.mock import patch

import pytest

from src.API_system import ApiConnection, ApiConnectionHHRU


@pytest.fixture
def some_object():
    return ApiConnectionHHRU()


def test_ApiConnectionHHRU(some_object):
    assert isinstance(some_object, ApiConnection) == True


@patch("src.API_system.requests.get")
def test_ApiConnectionHHRU_get_vacancy_data(mock_get):
    example_obj = ApiConnectionHHRU()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"items": "1"}
    result = list("1" * 20)
    assert example_obj.get_vacancy_data("test", 1) == result


@patch("src.API_system.requests.get")
def test_ApiConnectionHHRU_get_vacancy_data_invalid_status_code(mock_get):
    example_obj = ApiConnectionHHRU()
    mock_get.return_value.status_code = 500
    # mock_get.return_value.json.return_value = {"items": "1"}
    # result = list("1" * 20)
    with pytest.raises(ValueError):
        example_obj.get_vacancy_data("test", 1)


@patch("src.API_system.requests.get")
def test_employer_id_list(mock_get):
    example_obj = ApiConnectionHHRU()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"items": "1"}
    example_obj.employer_id_list = [1, 2, 3]
    assert example_obj.employer_id_list == [1, 2, 3]
    example_obj.employer_id_list = [1, 2]
    assert example_obj.employer_id_list == [1, 2]
    del example_obj.employer_id_list
    assert example_obj.employer_id_list == []
