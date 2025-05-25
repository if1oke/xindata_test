import sqlite3

import pandas as pd

DB_PATH = "freelancers.db"
TABLE_NAME = "freelancers"


def execute_query(sql: str, db_path: str = DB_PATH) -> pd.DataFrame:
    """
    Выполняет SQL-запрос и возвращает результат в виде DataFrame.

    :param sql: текст SQL-запроса
    :param db_path: путь до SQLite базы
    :return: pandas.DataFrame с результатами
    """
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    except Exception as e:
        raise RuntimeError(f"Ошибка при выполнении SQL-запроса: {e}")
    finally:
        conn.close()


def test_query(limit: int = 5):
    """
    Для тестирования: SELECT * FROM freelancers LIMIT n
    """
    sql = f"SELECT * FROM {TABLE_NAME} LIMIT {limit};"
    df = execute_query(sql)
    print(df.head())


if __name__ == "__main__":
    test_query()
