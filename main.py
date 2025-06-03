from parsers.parser_excel import parse_excel
from controller import generate_full_report


def get_user_input(prompt: str, default: str = "") -> str:
    value = input(f"{prompt}{f' (по умолчанию: {default})' if default else ''}: ").strip()
    return value if value else default


def main():
    print("Добро пожаловать в Анализатор транзакций")

    file_path = get_user_input("Укажите путь к Excel-файлу", "../input/data.xlsx")
    category = get_user_input("Введите категорию для анализа", "Продукты")
    month = get_user_input("Введите месяц в формате YYYY-MM", "2025-06")

    try:
        round_limit = float(get_user_input("Введите лимит округления (например, 50)", "50"))
    except ValueError:
        print("Введено некорректное значение, используется значение по умолчанию: 50")
        round_limit = 50.0

    try:
        transactions = parse_excel(file_path)
        print(f"Загружено транзакций: {len(transactions)}")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return

    output_path = generate_full_report(
        transactions=transactions,
        month=month,
        category=category,
        round_limit=round_limit,
        excel_filename="report.xlsx"
    )

    print(f"Отчёт успешно сохранён в: {output_path}")


if __name__ == "__main__":
    main()
