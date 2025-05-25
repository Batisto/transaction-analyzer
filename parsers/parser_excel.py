import pandas as pd
from transaction import Transaction

def parse_excel(file_path: str) -> list[Transaction]:
    """
    Парсит excel файл и возвращает список транзакций
    """

    df = pd.read_excel(file_path)

    column_mapping = {
        "Дата операции": "operation_date",
        "Дата платежа": "payment_date",
        "Категория": "category",
        "Описание": "description",
        "Кэшбэк": "cashback",
        "Сумма операции": "amount",
        "Бонусы (включая кэшбэк)": "bonuses"
    }
    df.rename(columns=column_mapping, inplace=True)

    required_columns = ["operation_date", "payment_date", "category", "description", "cashback", "amount", "bonuses"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Отсутствует необходимый столбец: {col}")

    df["operation_date"] = pd.to_datetime(df["operation_date"], format="mixed")
    df["payment_date"] = pd.to_datetime(df["payment_date"], format="mixed")

    df[["cashback", "amount", "bonuses"]] = df[["cashback", "amount", "bonuses"]].fillna(0)

    transactions = []

    for _, row in df.iterrows():
        transaction = Transaction(
            operation_date=row["operation_date"],
            payment_date=row["payment_date"],
            category=row["category"] if pd.notna(row["category"]) else "Другое",
            description=row["description"] if pd.notna(row["description"]) else "Нет описания",
            cashback=row["cashback"],
            amount=row["amount"],
            bonuses=row["bonuses"]
        )

        transactions.append(transaction)

    return transactions
