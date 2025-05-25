from datetime import datetime
from typing import List
from transaction import Transaction


def is_weekday(date: datetime) -> bool:
    """
    Проверяет, является ли дата будним днем
    """
    return date.weekday() < 5

def filter_by_weekday(transactions: List[Transaction], weekday: bool) -> List[Transaction]:
    """
    Фильтрует транзакции по типу дня: будний или выходной
    Если weekday - True: возвращает транзакции за будни
    Если weekday - False: возвращает транзакции за выходные
    """
    return [t for t in transactions if is_weekday(t.operation_date) == weekday]