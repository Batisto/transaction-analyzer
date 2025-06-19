import pandas as pd
from dataclasses import asdict
from src.reports import raw_expenses_by_category, raw_expenses_by_weekday


def test_expenses_by_category(sample_transactions):
    # Преобразуем список объектов Transaction в список словарей
    df = pd.DataFrame([asdict(t) for t in sample_transactions])

    # Вызываем чистую функцию без сохранения
    result = raw_expenses_by_category(df, category="Продукты", month="2025-06")

    # Проверки
    assert not result.empty, "Результат должен быть непустым"
    assert "category" in result.columns, "В результатах должна быть колонка 'category'"
    assert (result['category'] == "Продукты").all(), "Все строки должны относиться к категории 'Продукты'"


def test_expenses_by_weekday(sample_transactions):
    # Преобразуем список объектов Transaction в DataFrame
    df = pd.DataFrame([asdict(t) for t in sample_transactions])

    # Вызываем тестируемую функцию
    result = raw_expenses_by_weekday(df, month="2025-06")

    # Проверки
    assert not result.empty, "Результат должен быть непустым"
    assert "weekday_name" in result.columns, "В результатах должна быть колонка 'weekday_name'"
    assert "Сумма расходов (₽)" in result.columns, "В результатах должна быть колонка 'Сумма расходов (₽)'"
    assert (result["Сумма расходов (₽)"] > 0).all(), "Суммы расходов должны быть положительными"
    assert result["weekday_name"].isin([
        "Понедельник", "Вторник", "Среда", "Четверг",
        "Пятница", "Суббота", "Воскресенье"
    ]).all(), "В результатах должны быть корректные названия дней недели"
