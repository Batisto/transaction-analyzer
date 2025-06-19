Анализатор транзакций
Приложение для анализа банковских транзакций из Excel-файла. Поддерживает генерацию Excel-отчётов, инвесткопилку, веб-страницу «Главная» с JSON-ответом и подключение внешних API.

📂 Структура проекта
.
├── src
│   ├── main.py
│   ├── views.py
│   ├── reports.py
│   ├── services.py
│   ├── transaction.py
│   ├── parser_excel.py
│   ├── utils.py
│   └── logger.py
├── tests
│   ├── test_views.py
│   ├── test_services.py
│   ├── test_reports.py
│   └── conftest.py
├── data
│   └── operations.xlsx
├── user_settings.json
├── .env
├── .env_template
├── pyproject.toml
├── .flake8
└── README.md

✅ Веб-страницы
home_page_view(datetime_str) возвращает JSON-ответ:

приветствие

траты по картам

топ-5 транзакций

курсы валют и цены акций

✅ Сервисы
investment_bank(month, transactions, limit) — расчёт инвесткопилки по округлению

✅ Отчёты
expenses_by_category(...) — траты по категории за месяц

expenses_by_weekday(...) — средние траты по дням недели