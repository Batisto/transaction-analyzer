import pandas as pd
from export.excel_exporter import save_to_excel


@save_to_excel(sheet_name="Категория")
def expenses_by_category(df: pd.DataFrame, category: str, month: str) -> pd.DataFrame:
    """
    Возвращает DataFrame с расходами по заданной категории и месяцу.
    Параметры:
        df — исходный DataFrame с транзакциями
        category — категория для фильтрации
        month — строка формата 'YYYY-MM'
    """
    # Преобразуем даты к строкам формата 'YYYY-MM' для фильтрации по месяцу
    df['operation_month'] = df['operation_date'].dt.strftime('%Y-%m')

    filtered = df[
        (df['category'] == category) &
        (df['amount'] < 0) &
        (df['operation_month'] == month)
    ]

    return filtered.drop(columns=['operation_month'])


@save_to_excel(sheet_name="Будни_Выходные")
def expenses_by_weekday(df: pd.DataFrame, month: str) -> pd.DataFrame:
    """
    Возвращает DataFrame с суммой расходов по дням недели за указанный месяц.
    """
    # Преобразуем даты в формат YYYY-MM для фильтрации по месяцу
    df['operation_month'] = df['operation_date'].dt.strftime('%Y-%m')

    # Фильтрация по месяцу и только по расходам
    filtered = df[(df['operation_month'] == month) & (df['amount'] < 0)]

    # Получаем день недели (0 = Пн, 6 = Вс)
    filtered['weekday'] = filtered['operation_date'].dt.dayofweek

    # Названия дней недели для читаемости
    weekday_map = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }
    filtered['weekday_name'] = filtered['weekday'].map(weekday_map)

    # Группируем и считаем сумму расходов
    result = filtered.groupby('weekday_name')['amount'].sum().abs().reset_index()
    result.rename(columns={'amount': 'Сумма расходов (₽)'}, inplace=True)

    return result