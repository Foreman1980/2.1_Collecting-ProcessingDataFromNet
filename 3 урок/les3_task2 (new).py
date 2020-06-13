from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vacancies = db.vacancies

# input_salary = int(input('Введите желаемую зарплату (руб.) - '))
input_salary = 100000


def vacancies_search(salary: int):
    for vacancy in vacancies.find({'$or': [{'salary.currency': {'$eq': 'руб.'},
                                            '$or': [{'salary.salary_min': {'$gte': salary}},
                                                    {'salary.salary_max': {'$gte': salary}}]},
                                           {'salary.currency': {'$eq': 'USD'},
                                            '$or': [
                                                {'salary.salary_min': {'$gte': salary / pars_ruble_exchange_rate()}},
                                                {'salary.salary_max': {
                                                    '$gte': salary / pars_ruble_exchange_rate()}}]}]}):
        pprint(vacancy)


def pars_ruble_exchange_rate() -> float:
    return float(70)


if __name__ == '__main__':
    vacancies_search(input_salary)
