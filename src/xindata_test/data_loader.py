import os
import sqlite3

import pandas as pd


def load_data_to_sqlite(
    csv_path: str = "notebooks/enriched_freelancer_data.csv",
    db_path: str = "freelancers.db",
    table_name: str = "freelancers",
) -> None:
    """
    Загружает обогащённый CSV в SQLite базу.

    :param csv_path: путь до CSV с данными
    :param db_path: путь до SQLite-файла
    :param table_name: название таблицы в БД
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV файл не найден: {csv_path}")

    df = pd.read_csv(csv_path)

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print("Данные загружены в SQLite!")


if __name__ == "__main__":
    load_data_to_sqlite()
