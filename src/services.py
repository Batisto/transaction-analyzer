from typing import List
from transaction import Transaction
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
