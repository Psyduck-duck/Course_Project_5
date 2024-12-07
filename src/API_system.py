from abc import ABC, abstractmethod

import requests


class ApiConnection(ABC):
    """Абстрактный класс для работы с api ресурсами"""

    @abstractmethod
    def __init__(self) -> None:
        """Коструктор для определения основных параметров"""
        pass

    @abstractmethod
    def connect(self) -> None:
        """Метод для определения подключения к сервисам"""
        pass

    @abstractmethod
    def get_vacancy_data(self, search_text: str) -> None:
        """Метод для получения информации по вакансиям"""
        pass


class ApiConnectionHHRU(ApiConnection):
    """Класс для работы с API сервисами HH.ru"""

    def __init__(self) -> None:
        """Конструктор для определения ключевых параметров для работы с API"""

        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {
            "text": None,
            "search_field": "name",
            "page": 0,
            "per_page": 100,
            "only_with_salary": False,
            "period": None,
            "employer_id": [],
        }
        self.__search_target = None
        self.__vacancies = []
        self.__is_connecting = False
        self.__employer_id_list = []

    @property
    def employer_id_list(self):
        return self.__employer_id_list

    @employer_id_list.setter
    def employer_id_list(self, id_list: list[int]) -> None:
        self.__employer_id_list = id_list

    @employer_id_list.deleter
    def employer_id_list(self) -> None:
        self.__employer_id_list = []

    def connect(self) -> None:
        pass

    def __connect_HHRU(self) -> None:
        """метод для определения установки связи c API HH.ru"""
        response = requests.get("https://api.hh.ru", self.__headers)
        if response.status_code != 200:
            raise ValueError("Check URL or headers")
        self.__is_connecting = True

    def get_vacancy_data(self, search_text: str, per_page: int) -> list:
        """Метод для получения вакансий"""

        self.__connect_HHRU()
        if self.__is_connecting:
            self.__headers["text"] = search_text
            self.__headers["per_page"] = per_page
            self.__headers["employer_id"] = self.__employer_id_list
            while self.__headers.get("page") != 20:
                response = requests.get(self.__url, self.__headers)
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__headers["page"] += 1

        else:
            raise ValueError("Connection status is False")

        return self.__vacancies
