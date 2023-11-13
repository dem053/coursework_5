from src.utils import get_employer_data, get_vacancies_data, make_cities_list
from src.config import config
from src.db_manager import DBManager




def main():
    employer_ids = [
        1740,
        15478,
        78638,
        68587,
        1666189,
        1789341,
        4010751,
        3672566,
        2723603,
        2000762
    ]
    key_word = 'Python'
    db_name = 'headhunter'
    params = config()

    # employers_data = get_employer_data(employer_ids)
    # vacancies_data = get_vacancies_data(employer_ids, key_word)
    # cities_data = make_cities_list(employers_data, vacancies_data)
    db = DBManager(db_name, params)
    # db.created_db()
    # db.insert_data(cities_data, employers_data, vacancies_data)
    print(db.get_companies_and_vacancies_count())
    print(len(db.get_all_vacancies()))
    print(db.get_avg_salary())
    print(len(db.get_vacancies_with_higher_salary()))
    print(len(db.get_vacancies_with_keyword('SQL%Java')))









if __name__ == '__main__':
    main()
