import pandas as pd
from src.excel_exporter import save_to_excel


def raw_expenses_by_category(df: pd.DataFrame, category: str, month: str) -> pd.DataFrame:
    """
    Возвращает DataFrame с расходами по заданной категории и месяцу.
    """
    df['operation_month'] = df['operation_date'].dt.strftime('%Y-%m')

    filtered = df[
        (df['category'] == category) &
        (df['amount'] < 0) &
        (df['operation_month'] == month)
    ]

    return filtered.drop(columns=['operation_month'])


def raw_expenses_by_weekday(df: pd.DataFrame, month: str) -> pd.DataFrame:
    """
    Возвращает DataFrame с суммой расходов по дням недели за указанный месяц.
    """
    df['operation_month'] = df['operation_date'].dt.strftime('%Y-%m')

    filtered = df[(df['operation_month'] == month) & (df['amount'] < 0)]
    filtered['weekday'] = filtered['operation_date'].dt.dayofweek

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

    result = filtered.groupby('weekday_name')['amount'].sum().abs().reset_index()
    result.rename(columns={'amount': 'Сумма расходов (₽)'}, inplace=True)

    return result


expenses_by_category = save_to_excel(sheet_name="Категория")(raw_expenses_by_category)
expenses_by_weekday = save_to_excel(sheet_name="Будни_Выходные")(raw_expenses_by_weekday)