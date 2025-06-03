from functools import wraps
from pathlib import Path
from transaction import Transaction
from filters.category_filter import filter_by_category
from filters.weekday_filter import filter_by_weekday
from services.services import calculate_fixed_to_savings, calculate_percent_to_savings, calculate_round_up_savings
import pandas as pd
from typing import List
from functools import wraps


def save_to_excel(sheet_name: str, file_name:str = "reports.xlsx"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            if not isinstance(df, pd.DataFrame):
                raise TypeError("Функция должна возвращать DataFrame")

            output_path = Path(__file__).resolve().parent.parent / "output" / file_name

            with pd.ExcelWriter(output_path, engine="openpyxl", mode="a" if output_path.exists() else 'w') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            return df
        return wrapper
    return decorator


def generate_report(
    transactions: List[Transaction],
    filename: str,
    fixed_amount: float = 50.0,
    percent: float = 5.0
):
    output_path = Path(__file__).parent.parent / "output" / filename

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        #Лист "транзакции"
        data = [
            {
                "Дата": t.operation_date.strftime("%d.%m.%Y"),
                "Категория": t.category,
                "Описание": t.description,
                "Сумма": t.amount
            }
            for t in transactions
        ]
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name="Транзакции", index=False)


        #Лист "Сводка"
        total_transactions = len(transactions)
        total_expenses = round(sum(t.amount for t in transactions if t.amount < 0), 2)
        total_income = round(sum(t.amount for t in transactions if t.amount > 0), 2)
        total_cashback = round(sum(t.cashback for t in transactions), 2)
        total_savings = 0.0

        all_dates = [t.operation_date.date() for t in transactions]
        start_date = min(all_dates).strftime("%d.%m.%Y")
        end_date = max(all_dates).strftime("%d.%m.%Y")
        period = f'{start_date} - {end_date}'

        summary_data = {
            "Показатель": [
                "Кол-во транзакций",
                "Общая сумма расходов",
                "Общая сумма доходов",
                "Всего кэшбэка",
                "Сумма накоплений (копилка)",
                "Период"
            ],
            "Значение": [
                total_transactions,
                f"{abs(total_expenses):,.2f} ₽",
                f"{total_income:,.2f} ₽",
                f"{total_cashback:,.2f} ₽",
                f"{total_savings:,.2f} ₽",
                period
            ]
        }

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name="Сводка", index=False)


        #Лист "Категории"
        categories = set(t.category for t in transactions if t.amount < 0)
        category_totals = {
            cat: round(
                sum(t.amount for t in filter_by_category(transactions, cat) if t.amount < 0),
                2
            )
            for cat in categories
        }

        category_data = {
            "Категория": list(category_totals.keys()),
            "Сумма расходов (₽)": [abs(v) for v in category_totals.values()]
        }

        category_df = pd.DataFrame(category_data)
        category_df.to_excel(writer, sheet_name="Категории", index=False)


        #Лист Будни/Выходные

        weekday_transactions = filter_by_weekday(transactions, weekday=True)
        weekend_transactions = filter_by_weekday(transactions, weekday=False)

        total_weekday = round(sum(t.amount for t in weekday_transactions if t.amount < 0), 2)
        total_weekend = round(sum(t.amount for t in weekend_transactions if t.amount < 0), 2)

        weekday_data = {
            "Тип дня": ["Будни", "Выходные"],
            "Сумма расходов (₽)": [abs(total_weekday), abs(total_weekend)]
        }

        weekday_df = pd.DataFrame(weekday_data)
        weekday_df.to_excel(writer, sheet_name="Будни_Выходные", index=False)

        #Лист "Копилка"
        savings_round = calculate_round_up_savings(transactions)
        savings_fixed = calculate_fixed_to_savings(transactions, amount=fixed_amount)
        savings_percent = calculate_percent_to_savings(transactions, percent=percent)

        piggybank_data = {
            "Способ накопления": [
                "Округление до сотен",
                "Фиксированная сумма",
                "Процент от каждой траты"
            ],
            "Параметр": [
                "—",
                f"{fixed_amount} ₽ с каждой",
                f"{percent}%"
            ],
            "Сумма накоплений (₽)": [
                round(savings_round, 2),
                round(savings_fixed, 2),
                round(savings_percent, 2)
            ]
        }

        piggybank_df = pd.DataFrame(piggybank_data)
        piggybank_df.to_excel(writer, sheet_name="Копилка", index=False)

    return output_path
