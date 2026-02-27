import pytest
from unittest.mock import patch
from src.adapters.market_data import MarketDataAdapter

@pytest.fixture
def mock_yfinance_ticker():
    """Mock the yfinance Ticker to avoid hitting real API in tests."""
    with patch("yfinance.Ticker") as mock_ticker:
        mock_info = {
            "currentPrice": 28500,
            "marketCap": 150000000000,
            "trailingPE": 15.5,
            "forwardPE": 12.0,
            "trailingEps": 1800,
            "revenueGrowth": 0.15,
            "profitMargins": 0.12,
            "debtToEquity": 45.5,
            "priceToBook": 1.8,
            "fiftyTwoWeekLow": 22000,
            "fiftyTwoWeekHigh": 32000,
            "sector": "Basic Materials"
        }
        mock_ticker.return_value.info = mock_info
        yield mock_ticker

def test_fetch_stock_data(mock_yfinance_ticker):
    adapter = MarketDataAdapter()
    data = adapter.fetch_stock_data("HPG")
    
    # Assert
    assert data["ticker"] == "HPG"
    assert data["current_price"] == 28500
    assert data["trailing_pe"] == 15.5
    assert data["sector"] == "Basic Materials"
    # Ensure correct suffix was applied
    mock_yfinance_ticker.assert_called_once_with("HPG.VN")

def test_generate_financial_report(mock_yfinance_ticker):
    adapter = MarketDataAdapter()
    report = adapter.generate_financial_report("HPG")
    
    # Assert values are formatted correctly
    assert "28500" in report
    assert "15.5" in report
    assert "15.0%" in report # 0.15 * 100
    assert "12.0%" in report # 0.12 * 100
    assert "45.5%" in report
    assert "Basic Materials" in report

def test_market_context_returns_string():
    adapter = MarketDataAdapter()
    context = adapter.get_market_context()
    assert isinstance(context, str)
    assert len(context) > 0
