import re
from abc import ABC, abstractmethod
from typing import Any, Tuple, Union


class Vacancy(ABC):
    """Абстрактный класс для работы с вакансиями"""

    __slots__ = ("id", "name", "salary_down", "salary_up", "salary_currency", "url", "requirement", "responsibility")

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __lt__(self, other) -> None:  # Больше или равно
        pass

    @abstractmethod
    def __le__(self, other) -> None:  # Больше или равно
        pass

    @abstractmethod
    def __gt__(self, other) -> None:  # Больше или равно
        pass

    @abstractmethod
    def __ge__(self, other) -> None:  # Больше или равно
        pass


class VacancyHHRU(Vacancy):
    """Класс для определения вакансии с ресурса HH.ru"""

    def __init__(self, vacancy_dict: dict) -> None:
        """Конструктор для определния основных атрибутов"""

        self.id = self.__validation_id(vacancy_dict)
        self.name = self.__validation_name(vacancy_dict)
        self.salary_down, self.salary_up = self.__validation_salary(vacancy_dict)
        self.salary_currency = self.__validation_salary_currency(vacancy_dict)
        self.url = self.__validation_url(vacancy_dict)
        self.requirement, self.responsibility = self.__validation_snippet(vacancy_dict)

    def __lt__(self, other: Vacancy) -> bool:
        """Метод для сравнения зарплаты (<)"""

        result = False
        if self.salary_down < other.salary_down:
            result = True
        return result

    def __le__(self, other: Vacancy) -> bool:
        """Метод для сравнения зарплаты (<=)"""

        result = False
        if self.salary_down <= other.salary_down:
            result = True
        return result

    def __gt__(self, other: Vacancy) -> bool:
        """Метод для сравнения зарплаты (>)"""

        result = False
        if self.salary_down > other.salary_down:
            result = True
        return result

    def __ge__(self, other: Vacancy) -> bool:
        """Метод для сравнения зарплаты (>=)"""

        result = False
        if self.salary_down >= other.salary_down:
            result = True
        return result

    def __validation_id(self, vacancy_dict: dict) -> str | None:
        """метод для валидации id вакансии"""

        if vacancy_dict.get("id"):
            id = vacancy_dict.get("id")
            if type(id) == str:
                return id
            raise TypeError("id must be str")

        raise ValueError("id not found")

    def __validation_name(self, vacancy_dict: dict) -> str | None:
        """Метод для валидации имени"""

        if vacancy_dict.get("name"):
            name = vacancy_dict.get("name")
            if type(name) == str:
                return name
            raise TypeError("name must be str")

        raise ValueError("name not detected")

    def __validation_salary(self, vacancy_dict: dict) -> tuple[int | None, int | None] | tuple[None, None]:
        """Метод для валидации зарплаты"""

        if vacancy_dict.get("salary"):
            salary_down = vacancy_dict.get("salary").get("from")
            salary_up = vacancy_dict.get("salary").get("to")
            # salary_currency = vacancy_dict.get("salary").get("currency")
            if type(salary_up) != int:  # and type(salary_down) == int:
                salary_up = None
            if type(salary_down) != int:
                salary_down = None
            return salary_down, salary_up
            # raise TypeError("salary must be int")

        return None, None

    def __validation_salary_currency(self, vacancy_dict: dict) -> str | None:
        """Метод для валидации валюты зарплаты"""

        if vacancy_dict.get("salary"):
            if vacancy_dict.get("salary").get("currency"):
                salary_currency = vacancy_dict.get("salary").get("currency")
                if type(salary_currency) == str:
                    return salary_currency
                raise TypeError("currency must be str")
        return None

    def __validation_url(self, vacancy_dict: dict) -> str | None:
        """Метод для валидации url вакансии"""

        pattern = re.compile(r"\bhttps?://.+\..+\b")
        matches = re.findall(pattern, vacancy_dict.get("alternate_url"))
        if matches:
            return matches[0]
        raise ValueError("url not detected")

    def __validation_snippet(self, vacancy_dict: dict) -> tuple[str | None, None | str] | tuple[None, None]:
        """Метод для валидации умений и обязанностей"""

        if vacancy_dict.get("snippet"):
            vacancy_requirement = vacancy_dict.get("snippet").get("requirement")
            vacancy_responsibility = vacancy_dict.get("snippet").get("responsibility")
            if type(vacancy_requirement) != str:  # and type(vacancy_responsibility) == str:
                vacancy_requirement = None
            if type(vacancy_responsibility) != str:
                vacancy_responsibility = None
            return vacancy_requirement, vacancy_responsibility
            # raise TypeError("requirement and responsibility must be str")

        raise ValueError("snippet nor detected")
