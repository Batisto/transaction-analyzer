from typing import List
from src.transaction import Transaction
from datetime import datetime


def calculate_round_up_savings(transactions: List[Transaction]) -> float:
    """
    Возвращает сумму накоплений по правилу округления:
    добивает до следующей сотни только те суммы, остаток которых при делении на 100 больше 50.
    """
    total_savings = 0.0
    for t in transactions:
        if t.amount < 0.0:
            amount_abs = abs(t.amount)
            reminder = amount_abs % 100
            if reminder > 50:
                total_savings += 100 - reminder
    return round(total_savings, 2)


def calculate_percent_to_savings(transactions: List[Transaction], percent: float) -> float:
    """
    Возвращает сумму накоплений по правилу процента:
    Откладывает от каждой траты указанный процент и возвращает всю накопившуюся сумму
    """
    total_savings = 0.0
    for t in transactions:
        if t.amount < 0.0:
            amount_abs = abs(t.amount)
            savings = amount_abs * percent / 100
            total_savings += savings
    return round(total_savings, 2)


def calculate_fixed_to_savings(transactions: List[Transaction], amount: float) -> float:
    """
    Возвращает сумму накоплений по правилу фиксированного числа:
    Откладывает от каждой траты указанную сумму и возвращает всю накопившуюся сумму
    """
    total_savings = 0.0
    for t in transactions:
        if t.amount < 0.0:
            total_savings += amount
    return round(total_savings, 2)


def calculate_piggybank(transactions: List[Transaction], month: str, round_limit: float = 50.0) -> float:
    """
    Возвращает сумму накоплений за указанный месяц по правилу округления.
    month — строка в формате 'YYYY-MM', например '2025-06'
    """
    filtered = [
        t for t in transactions
        if t.amount < 0.0 and t.operation_date.strftime("%Y-%m") == month
    ]
    return calculate_round_up_savings(filtered, limit=round_limit)


def investment_bank(month: str, transactions: List[dict], limit: int) -> float:
    """
    Рассчитывает сумму, которую можно было бы отложить в "инвесткопилку"
    по округлению трат в указанном месяце.
    """
    parsed_transactions = []
    for t in transactions:
        try:
            parsed_transactions.append(
                Transaction(
                    operation_date=datetime.strptime(t["operation_date"], "%Y-%m-%d"),
                    payment_date=datetime.strptime(t["payment_date"], "%Y-%m-%d"),
                    category=t["category"],
                    description=t["description"],
                    cashback=float(t.get("cashback", 0)),
                    amount=float(t["amount"]),
                    bonuses=float(t.get("bonuses", 0)),
                )
            )
        except Exception as e:
            continue

    filtered = [
        t for t in parsed_transactions if t.amount < 0 and t.operation_date.strftime("%Y-%m") == month
    ]

    return float(round(sum(
        (limit - (abs(t.amount) % limit)) if (abs(t.amount) % limit > 0) else 0
        for t in filtered
    ), 2))
