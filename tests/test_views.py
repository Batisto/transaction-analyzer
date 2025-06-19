from src.views import home_page_view


def test_home_page_view(sample_transactions):
    result = home_page_view(sample_transactions, "2025-06-06 12:00:00")
    assert "Добрый день" in result
    assert "cards" in result
    assert "top_transactions" in result
