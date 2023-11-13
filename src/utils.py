from typing import Any
import requests, json


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
            'text': key_word,
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
    vacancies_data = created_vac_data(vacancies)
    return vacancies_data


def created_vac_data(vacancies: list[list]):
    """Нормализует данные о вакансиях для загрузки в DB"""
    vacancies_data = []
    for v in vacancies:
        v_id = v['id']
        name = v['name']
        v_url = v['alternate_url']
        employer_id = v['employer']['id']
        requirement = v['snippet']['requirement']
        if requirement:
            requirement = v['snippet']['requirement'].replace('<highlighttext>', '').replace('</highlighttext>', '')
        if v['salary'] is not None:
            salary_from = get_salary(v['salary']['from'])
            salary_to = get_salary(v['salary']['to'])
            currency = v['salary']['currency']
        else:
            salary_from = 0
            salary_to = 0
            currency = None
        salary_max = max(salary_to, salary_from)
        city_id = v['area']['id']
        city_name = v['area']['name']
        vacancy = [v_id, name, v_url, employer_id, requirement, salary_from, salary_to, salary_max, currency, city_id,
                   city_name]
        vacancies_data.append(vacancy)
    return vacancies_data


def get_salary(salary):
    """Нормализует з/п, если None равно 0"""

    if salary:
        salary = int(float(salary))
    else:
        salary = 0
    return salary


def make_cities_list(employers_data, vacancies_data):
    cities = {}
    for emp in employers_data:
        if cities.get(emp[3]) is None:
            cities[emp[3]] = emp[4]
    for vac in vacancies_data:
        if cities.get(vac[9]) is None:
            cities[vac[9]] = vac[10]
    return cities
