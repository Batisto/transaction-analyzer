from dataclasses import asdict

from src.services import investment_bank


def test_investment_bank(sample_transactions):
    result = investment_bank(
        "2025-06", [asdict(t) for t in sample_transactions], limit=100
    )
    assert isinstance(result, float)
    assert result >= 0
