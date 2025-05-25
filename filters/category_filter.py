from typing import List
from transaction import Transaction


def filter_by_category(transactions: List[Transaction], category: list) -> List[Transaction]:
    """
    Фильтрует транзакции по категориям
    """
    return [t for t in transactions if t.category == category]