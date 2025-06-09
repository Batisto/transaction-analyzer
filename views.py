import os
from asyncio import timeout

from dotenv import load_dotenv

load_dotenv()

import json
from pathlib import Path
from string import digits
from parsers.parser_excel import parse_excel
from transaction import Transaction
from datetime import datetime
from typing import List, Dict, Any
from transaction import Transaction
import requests
import time


def get_greeting(hour: int) -> str:
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_user_settings() -> Dict[str, Any]:
    settings_path = Path(__file__).resolve().parent.parent / "user_settings.json"
    with open(settings_path, encoding="utf-8") as f:
        return json.load(f)


def home_page_view(transactions: List[Transaction], datetime_str: str) -> str:
    dt = datetime.strftime(datetime_str, "Y%-m%-d% %H-%M-%S")
    greetings = get_greeting(dt.hour)

    cards_dict = {}
    for t in transactions:
        if not t.description or not t.description.strip():
            continue
        digits = ''.join(filter(str.isdigit, t.description))[-4:]
        if len(digits) < 4:
            continue
        if digits not in cards_dict:
            cards_dict[digits] = {
                "total_spent": 0.0,
                "cashback": 0.0
            }
        if t.amount < 0:
            cards_dict[digits]["total_spent"] += abs(t.amount)
            cards_dict[digits]["cashback"] += round(abs(t.amount) / 100, 2)

    cards = [
        {
            "last_digits": digits,
            "total_spent": round(data["total_spent"], 2),
            "cashback": round(data["cashback"], 2)
        }
        for digits, data in cards_dict.items()
    ]

    #Топ 5 транзакций
    top = sorted(transactions, key=lambda t: abs(t.amount), reverse=True)[:5]
    top_transactions = [
        {
            "date": t.operation_date.strftime("%Y.%m.%d"),
            "amount": round(t.amount, 2),
            "category": t.category,
            "description": t.description
        }
        for t in top
    ]

    # Загружаем настройки пользователя
    settings = load_user_settings()
    currency_list = settings.get("user_currencies", [])
    stock_list = settings.get("user_stocks", [])

    currency_rates = get_currency_rate(currency_list)
    stock_prices = get_stock_prices(stock_list)

    result = {
        "greeting": get_greeting,
        "card": cards,
        "top_transactions": top_transactions,
        "currency_rate": [],
        "stock_prices": []
    }

    return json.dumps(result, ensure_ascii=False, indent=4)


def get_currency_rate(currencies: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv("API_EXCHANGERATES_DATA")
    if not api_key:
        print("Ключ не найден в .env")

    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": api_key}
    params = {"base": "RUB", "symbols": ','.join(currencies)}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})

        return [{"currency": cur, "rate": round(1 / rates[cur], 2)} for cur in currencies if cur in rates]

    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return []


def get_stock_prices(stocks: List[str]) -> List[Dict[str,Any]]:
    api_key = os.getenv("API_TWELVE_DATA")
    if not api_key:
        print("API-ключ для Twelve Data не найден в .env")
        return []

    base_url = "https://api.twelvedata.com/price"
    result = []

    for symbol in stocks:
        try:
            response = requests.get(
                base_url,
                params={"symbol": symbol, "apikey": api_key},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if "price" in data:
                result.append({
                    "stock": symbol,
                    "price": round(float(data["price"]), 2)
                })
            else:
                print(f"Не удалось загрузить цену для {symbol}:{data}")
        except Exception as e:
            print(f"Ошибка при получении цены акции {symbol}:{e}")

    return result


def run_analysis(file_path: str, datetime_str: str) -> str:
    try:
        transaction: list[Transaction] = parse_excel(file_path)
    except Exception as e:
        return json.dumps({"error": f"Ошибка при загрузке файла: {str(e)}"})

    result = {
        "datetime": datetime_str,
        "total_transactions": len(transaction),
        "total_income": round(sum(t.amount for t in transaction if t.amount > 0), 2),
        "total_expenses": round(sum(t.amount for t in transaction if t.amount < 0), 2),
        "total_cashback": round(sum(t.cashback for t in transaction), 2)
    }

    return json.dumps(result, ensure_ascii=False, indent=4)
