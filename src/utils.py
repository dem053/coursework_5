from typing import Any
import requests, json, os


def get_employer_data(employer_ids: list) -> list[list[str, Any]]:
    """Получает данные с HH.ru о работадателях из списка employer_ids"""
    companies = []
    for i in employer_ids:
        hh_url = f'https://api.hh.ru/employers/{str(i)}'
        response = requests.get(hh_url)
        company = response.json()
        companies.append(
            [company['id'], company['name'], company['description'], company['area']['id'], company['area']['name']])
    return companies


def get_vacancies_data(employer_ids: list, key_word: str) -> list[list[str, Any]]:
    """
    Получает данные с HH.ru о вакансиях компаний, указанных в списке employer_ids
    и содержащих слово key_word
    """
    hh_url = "https://api.hh.ru/vacancies"
    vacancies = []
    page = 0
    while True:
        params = {
            'text': 'python',
            'area': 113,
            'page': page,
            'per_page': 100,
            'employer_id': employer_ids
        }
        response = requests.get(hh_url, params=params)
        vacancies.extend(response.json()['items'])
        if page == response.json()['pages']:
            break
        page += 1



    return []
