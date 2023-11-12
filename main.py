from src.utils import get_employer_data, get_vacancies_data


def main():
    hh_url = "https://api.hh.ru/vacancies"
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
    employer_data = get_employer_data(employer_ids)
    vacancies_data = get_vacancies_data(employer_ids)



if __name__ == '__main__':
    main()
