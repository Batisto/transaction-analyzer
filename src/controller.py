from pathlib import Path
from typing import List

import pandas as pd

from src.reports import expenses_by_category, expenses_by_weekday
from src.services import calculate_piggybank


def generate_full_report(
    transactions: List,
    month: str,
    category: str,
    round_limit: 50.0,
    excel_filename: str = "reports.xlsx",
) -> Path:
    """
    Вызывает аналитические функции, сохраняет excel отчет и возвращает путь к файлу
    """

    data = [
        {
            "operation_date": t.operation_date,
            "category": t.category,
            "description": t.description,
            "amount": t.amount,
        }
        for t in transactions
    ]
    df = pd.DataFrame(data)

    expenses_by_category(df, category=category, month=month)
    expenses_by_weekday(df, month=month)

    savings = calculate_piggybank(df, month=month, round_limit=round_limit)

    output_dir = Path(__file__).resolve().parent / "output"
    output_path = output_dir / excel_filename

    return output_path
