import json
from pathlib import Path
from transaction import Transaction


def transactions_to_json(transactions: list[Transaction], filename: str) -> Path:
    """
    Преобразует список транзакций в JSON-файл и сохраняет в файл
    """
    output_path = Path(__file__).resolve().parent.parent / "output" / filename

    data = {
        "transactions":[
            {
                "operation_date": t.operation_date.strftime("%Y-%m-%d"),  # дата в строку
                "payment_date": t.payment_date.strftime("%Y-%m-%d"),
                "category": t.category,
                "description": t.description,
                "cashback": t.cashback,
                "amount": t.amount,
                "bonuses": t.bonuses
            }
            for t in transactions
        ]
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return output_path
