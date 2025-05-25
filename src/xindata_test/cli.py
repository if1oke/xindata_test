import json

import rich
import rich.table
import typer

from xindata_test.llm_engine import answer_from_result, prompt_to_sql
from xindata_test.query_executor import execute_query

app = typer.Typer()


@app.command()
def ask(
    question: str = typer.Argument(..., help="Вопрос"),
    format: str = typer.Option("table", help="Вывода: table | json | md"),
    debug: bool = typer.Option(False, help="Показать сгенерированный SQL"),
) -> None:
    """
    Задай вопрос об аналитике фрилансеров. Пример:
    python -m freelance_qa "Какой процент экспертов выполнил < 100 проектов?"
    
    param: question: вопрос
    param: format: формат вывода
    param: debug: показывать дополнительную информацию
    """
    typer.echo("🔎 Формулируем SQL-запрос...")
    sql = prompt_to_sql(question)

    if debug:
        typer.echo("\n[debug] Сгенерированный SQL:")
        rich.print(f"[bold yellow]{sql}[/bold yellow]\n")

    try:
        df = execute_query(sql)
    except Exception as e:
        rich.print(f"[bold red]❌ Ошибка выполнения запроса:[/bold red] {e}")
        raise typer.Exit(1)

    result = df.to_dict(orient="records")

    # Вывод результата
    if format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif format == "md":
        print(df.to_markdown(index=False))
    else:
        table = rich.table.Table(show_header=True, header_style="bold cyan")
        for col in df.columns:
            table.add_column(col)
        for row in df.itertuples(index=False):
            table.add_row(*map(str, row))
        rich.print(table)

    # Пояснение
    answer = answer_from_result(question, result, sql)
    typer.echo(f"\n💡 Ответ:\n{answer}")


def main():
    app()


if __name__ == "__main__":
    main()
