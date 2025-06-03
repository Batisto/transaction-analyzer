import json
from pathlib import Path
from parsers.parser_excel import parse_excel
from transaction import Transaction
from datetime import datetime


def run_analysis(file_path: str, datetime_str: str) -> str:
    try:
        transaction: list[Transaction] = parse_excel(file_path)
    except Exception as e:
        return json.dumps({"error": f"Ошибка при загрузке файла: {str(e)}"})

    result = {
        "datetime": datetime_str,
        "total_transactions": len(transaction),
        "total_income": round(sum(t.amount for t in transaction if t.amount > 0), 2),
        "total_expenses": round(sum(t.amount for t in transaction if t.amount < 0), 2),
        "total_cashback": round(sum(t.cashback for t in transaction), 2)
    }

    return json.dumps(result, ensure_ascii=False, indent=4)
