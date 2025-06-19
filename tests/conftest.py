from datetime import datetime

import pytest

from src.transaction import Transaction


@pytest.fixture
def sample_transactions():
    return [
        Transaction(
            datetime(2025, 6, 1),
            datetime(2025, 6, 1),
            "Продукты",
            "Оплата картой 1234",
            12.0,
            -1200.0,
            0.0,
        ),
        Transaction(
            datetime(2025, 6, 2),
            datetime(2025, 6, 2),
            "Зарплата",
            "Зачисление",
            0.0,
            40000.0,
            0.0,
        ),
        Transaction(
            datetime(2025, 6, 3),
            datetime(2025, 6, 3),
            "Супермаркеты",
            "Магазин 5678",
            32.0,
            -3200.0,
            0.0,
        ),
        Transaction(
            datetime(2025, 6, 4),
            datetime(2025, 6, 4),
            "Кафе",
            "Кофейня 5678",
            3.5,
            -350.0,
            0.0,
        ),
    ]
