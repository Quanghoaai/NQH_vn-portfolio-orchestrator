import os
import json
import pytest
from unittest.mock import patch, MagicMock
import sys

# Đảm bảo có thể import module từ base_path của root dự án
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# Import module đã tạo trong `.agents.skills.analyzer-flash`
import importlib.util
spec = importlib.util.spec_from_file_location("analyzer_flash", os.path.join(base_dir, ".agents", "skills", "analyzer-flash.py"))
analyzer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer_module)
AnalyzerFlash = analyzer_module.AnalyzerFlash

class MockGeminiResponse:
    def __init__(self, text_payload):
        self.text = text_payload

@pytest.fixture
def mock_gemini():
    with patch('google.generativeai.configure') as mock_configure:
        with patch('google.generativeai.GenerativeModel') as MockModel:
            mock_model_instance = MagicMock()
            MockModel.return_value = mock_model_instance
            yield mock_model_instance

def test_analyzer_initialization_missing_key():
    """Test Governance Rule: Không thiết lập nếu thiếu API Key."""
    with pytest.raises(ValueError, match="Thiếu Gemini API Key"):
        AnalyzerFlash(gemini_api_key="")

def test_analyzer_analyze_stock_success(mock_gemini):
    """Test Agent chưng cất dữ liệu tạo tín hiệu mua chuẩn hóa."""
    # Giả lập trả về từ mô hình
    fake_json_string = '''{
        "ticker": "FPT",
        "action": "BUY",
        "target_yield": "15%",
        "confidence_score": "85",
        "reasoning": "Doanh thu tăng trưởng 20% so với cùng kỳ, PE hợp lý. Lợi nhuận gộp 18%.",
        "safety_margin": "Cao"
    }'''
    
    mock_gemini.generate_content.return_value = MockGeminiResponse(fake_json_string)
    
    analyzer = AnalyzerFlash(gemini_api_key="fake-secure-key")
    result = analyzer.analyze_stock(
        ticker="FPT",
        financial_report="Doanh thu 1000 tỷ, lợi nhuận gộp 18%, tăng trưởng 20%...",
        market_context="VN-Index đi ngang tích luỹ"
    )
    
    assert result["ticker"] == "FPT"
    assert result["action"] == "BUY"
    assert "15" in result["target_yield"]
    assert result["safety_margin"] == "Cao"
    assert "reasoning" in result

def test_analyzer_analyze_stock_invalid_json(mock_gemini):
    """Test cảnh báo lỗi format nếu AI chưng cất hỏng/lệch chuẩn."""
    # Cố tình mô phỏng lỗi LLM bị hỏng định dạng
    mock_gemini.generate_content.return_value = MockGeminiResponse("Tôi không chắc. Phải xem lại.")
    
    analyzer = AnalyzerFlash(gemini_api_key="fake-secure-key")
    
    with pytest.raises(ValueError, match="Lỗi Format"):
        analyzer.analyze_stock("SSI", "Loss 5%", "Downtrend")
