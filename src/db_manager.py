import psycopg2


class DBManager:
    """Класс для подключения и работе с базой данных"""

    def __init__(self, db_name: str, params: dict):
        """Конструктор сохраняет имя Базы данных и параметры для подключения"""

        self.name = db_name
        self.params = params

    @staticmethod
    def connect_db(name, params):
        """Подключение к базе данных"""
        conn = psycopg2.connect(dbname=name, **params)
        conn.autocommit = True
        return conn, conn.cursor()

    def created_db(self):
        conn, cur = self.connect_db('postgres', self.params)
        cur.execute(f"DROP DATABASE IF EXISTS {self.name}")
        cur.execute(f"CREATE DATABASE {self.name}")
        cur.close()
        conn.close()
        conn, cur = self.connect_db(self.name, self.params)
        cur.execute("""
                    CREATE TABLE cities (
                        city_id INT PRIMARY KEY,
                        city_name VARCHAR(50)
                        )
                """)
        cur.execute("""
                    CREATE TABLE employers (
                        employer_id INT PRIMARY KEY,
                        employer_name VARCHAR(255),
                        description TEXT,
                        city_id INTEGER REFERENCES cities (city_id)
                        )
                """)
        cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id INT PRIMARY KEY,
                        vacancy_name VARCHAR(255) NOT NULL,
                        vacancy_url VARCHAR(255),
                        employer_id INTEGER REFERENCES employers(employer_id),
                        requirement TEXT,
                        salary_from INT,
                        salary_to INT,
                        salary_max INT,
                        currency VARCHAR(4),
                        city_id INT REFERENCES cities (city_id)
                        )
                """)
        cur.close()
        conn.close()

    def insert_data(self, cities_data, employers_data, vacancies_data):
        """Метод заполнения базы данных переданными значениями"""

        conn, cur = self.connect_db(self.name, self.params)
        for id, city in cities_data.items():
            cur.execute("INSERT INTO cities (city_id, city_name) VALUES (%s, %s)", (id, city))
        for employer in employers_data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, description, city_id)
                VALUES (%s, %s, %s, %s)
                """,
                employer[0:4]
            )
        for vacancy in vacancies_data:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_url, employer_id, requirement, salary_from,
                salary_to, salary_max, currency, city_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                vacancy[0:10]
            )
        cur.close()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        conn, cur = self.connect_db(self.name, self.params)
        cur.execute("""SELECT employer_name, COUNT(vacancies.vacancy_id) as count_vacancies FROM employers INNER JOIN 
        vacancies USING(employer_id) GROUP BY employer_name ORDER BY count_vacancies DESC""")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на
        вакансию"""
        conn, cur = self.connect_db(self.name, self.params)
        cur.execute("""SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url FROM vacancies INNER 
        JOIN employers USING (employer_id) ORDER by salary_max""")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def get_avg_salary(self) -> float:
        """отдает средню заработную плату (avg (salary_max)) по вакансиям с указанной заработной платой"""

        conn, cur = self.connect_db(self.name, self.params)
        cur.execute("""SELECT AVG(salary_max) as salary_avg FROM vacancies WHERE salary_max <>0""")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        salary_avg = float(rows[0][0])
        return salary_avg

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        conn, cur = self.connect_db(self.name, self.params)
        cur.execute("""SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url
        FROM vacancies INNER JOIN employers USING (employer_id)
        WHERE salary_max > (SELECT AVG(salary_max) FROM vacancies WHERE salary_max<>0)
        ORDER by salary_max""")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def get_vacancies_with_keyword(self, keyword: str):
        """получает список всех вакансий, у которых в названии или описании есть ключевое слово"""

        conn, cur = self.connect_db(self.name, self.params)
        keyword = str(keyword)
        cur.execute(f"""SELECT employer_name, vacancy_name, requirement, salary_from, salary_to, vacancy_url, city_name
        FROM vacancies
        INNER JOIN cities USING (city_id)
        INNER JOIN employers USING (employer_id)
        WHERE vacancy_name LIKE '%{keyword}%' OR requirement LIKE '%{keyword}%'
        ORDER by salary_max""")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows





