from typing import List
from transaction import Transaction


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
