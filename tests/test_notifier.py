import pytest
from unittest.mock import patch
from src.adapters.notifier import Notifier

@pytest.fixture
def mock_clean_env(monkeypatch):
    """Môi trường sạch, không chứa config Telegram từ .env."""
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

def test_telegram_skip_if_no_config(mock_clean_env):
    notifier = Notifier()
    status = notifier.telegram_alert("Test", "Message")
    assert status == False # Không có token thì ngắt ngay

def test_console_alert_handles_valid_level(capsys):
    notifier = Notifier()
    notifier.console_alert("BUY FPT", "Lý luận kinh doanh mạnh", level="BUY")
    
    # Bắt dòng được in ra màn hình
    captured = capsys.readouterr()
    assert "BUY FPT" in captured.out
    assert "Lý luận kinh doanh mạnh" in captured.out

@patch('requests.post')
def test_telegram_success(mock_post, monkeypatch):
    # Set config ảo
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake_token_123")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "fake_chat_456")
    
    notifier = Notifier()
    
    # Mocking response 200 HTTP OK
    mock_post.return_value.status_code = 200
    status = notifier.telegram_alert("Test Signal", "Mua 100K")
    
    assert status == True
    # Kiểm tra URL được Request đến đúng cú pháp API của Telegram
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert "https://api.telegram.org/botfake_token_123" in args[0]
    assert kwargs['json']['chat_id'] == "fake_chat_456"

@patch('requests.post')
def test_telegram_failed(mock_post, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "wrong_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123")
    
    notifier = Notifier()
    mock_post.return_value.status_code = 401
    mock_post.return_value.text = "Unauthorized"
    
    status = notifier.telegram_alert("Test Signal", "Bị lỗi 401")
    assert status == False
