from pathlib import Path
from parsers.parser_excel import parse_excel
from export.excel_exporter import generate_report

def get_user_input(prompt: str) -> str:
    user_input = input(prompt).strip()
    if not user_input:
        print("Ввод не должен быть пустым")
        return get_user_input(prompt)
    return user_input


def choice_saving_method():
    print("\nВыберите способ накопления:")
    print("1. Округление до сотен")
    print("2. Фиксированная сумма с каждой траты")
    print("3. Процент от каждой траты")

    while True:
        choice = input("Введите номер (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print("⚠️ Некорректный выбор. Попробуйте снова.")


def main():
    print('Добро пожаловать в программу "Анализатор транзакций!"')

    file_path = get_user_input("Укажите путь к Excel-файлу (например, ../input/operations.xlsx):")

    try:
        print("Загружаем данные...")
        transactions = parse_excel(file_path)
        print(f"Загружено {len(transactions)} транзакций")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return  # Выходим из программы, если не удалось загрузить данные

    saving_choice = choice_saving_method()

    fixed_amount = 50.0
    percent = 5.0

    if saving_choice == "2":
        while True:
            try:
                fixed_amount = float(get_user_input("🔢 Укажите фиксированную сумму накопления с каждой траты (по умолчанию 50 ₽): "))
                break
            except ValueError:
                print("⚠️ Неверный формат числа. Используется значение по умолчанию: 50 ₽")
                fixed_amount = 50.0
                break
    elif saving_choice == "3":
        while True:
            try:
                percent = float(get_user_input("🔢 Укажите процент накопления от каждой траты (по умолчанию 5%): "))
                break
            except ValueError:
                print("⚠️ Неверный формат числа. Используется значение по умолчанию: 5%")
                percent = 5.0
                break

    print("📄 Генерируем отчёт...")

    if saving_choice == "1":
        generate_report(transactions, "report.xlsx", fixed_amount=0.0, percent=0.0)
    elif saving_choice == "2":
        generate_report(transactions, "report.xlsx", fixed_amount=fixed_amount, percent=0.0)
    elif saving_choice == "3":
        generate_report(transactions, "report.xlsx", fixed_amount=0.0, percent=percent)

    print("✨ Отчёт успешно создан!")


if __name__ == "__main__":
    main()