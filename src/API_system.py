from abc import ABC, abstractmethod

import requests
import json
import pandas as pd
import time


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
        }
        self.__search_target = None
        self.__vacancies = []
        self.__is_connecting = False
        self.employer_id_list = []

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
            while self.__headers.get("page") != 20:
                response = requests.get(self.__url, self.__headers)
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__headers["page"] += 1

        else:
            raise ValueError("Connection status is False")

        return self.__vacancies


object = ApiConnectionHHRU()
object.connect()
vacancy_data = object.get_vacancy_data('Python', 100)
for vacancy in vacancy_data:
    print(vacancy['employer'])






def getEmployers():
    req = requests.get('https://api.hh.ru/employers')
    data = req.content.decode()
    req.close()
    count_of_employers = json.loads(data)['found']
    employers = []
    i = 0
    j = count_of_employers
    while i < j:
        req = requests.get('https://api.hh.ru/employers/' + str(i + 1))
        data = req.content.decode()
        req.close()
        jsObj = json.loads(data)
        try:
            employers.append([jsObj['id'], jsObj['name']])
            i += 1
            print([jsObj['id'], jsObj['name']])
        except:
            i += 1
            j += 1
        # if i % 200 == 0:
        #     time.sleep(0.2)
    return employers


# employers = getEmployers()

