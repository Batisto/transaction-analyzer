from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    operation_date: datetime
    payment_date: datetime
    category: str
    description: str
    cashback: float
    amount: float
    bonuses: float
