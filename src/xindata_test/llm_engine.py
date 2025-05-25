import os
from typing import Dict, List

from openai import OpenAI

from xindata_test import constants
from xindata_test.query_executor import execute_query

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def prompt_to_sql(user_question: str) -> str:
    """
    Выполняет запрос на формирование SQL через LLM

    :param user_question: текст пользовательского запроса
    :return: строка с sql запросом
    """
    response = client.chat.completions.create(
        model=constants.MODEL,
        messages=[
            {"role": "system", "content": constants.SYSTEM_SQL_GEN},
            {"role": "user", "content": user_question},
        ],
        temperature=0.2,
    )
    sql = response.choices[0].message.content.strip()
    return sql


def answer_from_result(user_question: str, result: List[Dict], sql: str) -> str:
    """
    Формирует и отправляет запрос на формирование ответа в LLM
    исходя из результата выполнения запроса и исходного SQL

    :param user_question: текст пользовательского запроса
    :param result: результат выполнения SQL запроса
    :param sql: исходный SQL запрос
    :return: строка с ответом
    """
    content = f"Вопрос: {user_question}\n\nРезультат запроса:\n{result}"
    response = client.chat.completions.create(
        model=constants.MODEL,
        messages=[
            {"role": "system", "content": constants.SYSTEM_ANSWER_GEN + sql},
            {"role": "user", "content": content},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def test_prompt_to_sql(question: str) -> None:
    """
    Выполняет тестовый запрос на формирование SQL через LLM

    :param question: текст пользовательского запроса
    """
    res = prompt_to_sql(question)
    print(res)


def test_answer_from_result(question: str) -> None:
    """
    Выполняет тестовый запрос на формирование ответа через LLM
    с указанием исходного SQL запроса

    :param question: текст пользовательского запроса
    """
    sql = """
    SELECT Client_Region, SUM(Earnings_USD) AS Total_Earnings
    FROM freelancers
    GROUP BY Client_Region
    ORDER BY Total_Earnings DESC
    LIMIT 5;
    """

    data = execute_query(sql)
    res = answer_from_result(question, data, sql)
    print(res)


if __name__ == "__main__":
    test_prompt_to_sql("Нужен топ 5 регионов, которые платят больше всех")
    test_answer_from_result("Нужен топ 5 регионов, которые платят больше всех")
