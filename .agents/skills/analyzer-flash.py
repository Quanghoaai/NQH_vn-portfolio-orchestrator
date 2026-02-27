import os
import json
import google.generativeai as genai
from typing import Dict, Any

class AnalyzerFlash:
    def __init__(self, gemini_api_key: str, definition_path: str = '.agents/definitions/analyzer.json'):
        """
        Khởi tạo Analyzer Flash agent. 
        Lưu ý: API Key phải được giải mã từ Vault trước khi truyền vào đây 
        (Tuân thủ Governance Rule #01).
        """
        if not gemini_api_key:
            raise ValueError("Thiếu Gemini API Key.")
            
        genai.configure(api_key=gemini_api_key)
        
        # Load định nghĩa agent từ JSON
        # Path resolve để chạy đúng bất chấp current working directory
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        full_def_path = os.path.join(base_path, definition_path)
            
        with open(full_def_path, 'r', encoding='utf-8') as f:
            self.agent_def = json.load(f)
            
        # Khởi tạo Gemini 2.5 Flash
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=self.agent_def.get('system_prompt', '')
        )

    def analyze_stock(self, ticker: str, financial_report: str, market_context: str) -> Dict[str, Any]:
        """
        Chưng cất dữ liệu báo cáo tài chính và bối cảnh thị trường thành tín hiệu Mua/Bán.
        Mục tiêu Target: 15-18%.
        """
        prompt = f"""
        Phân tích mã chứng khoán: {ticker}
        
        [Dữ liệu Tài chính - Financial Statement]:
        {financial_report}
        
        [Biến động thị trường - Macro/Market context]:
        {market_context}
        
        Nhiệm vụ: Dựa trên Rule biên an toàn và xác suất rủi ro thấp, hãy chưng cất dữ liệu.
        Trả về DUY NHẤT một chuỗi JSON chuẩn xác theo cấu trúc sau (không có markdown code block):
        {{
            "ticker": "{ticker}",
            "action": "BUY" | "SELL" | "HOLD",
            "target_yield": "Expected %",
            "confidence_score": "<0-100>",
            "reasoning": "Lý giải ngắn gọn trích dẫn đúng con số từ dữ liệu đầu vào. Bỏ qua nhiễu.",
            "safety_margin": "Đánh giá biên an toàn (Thấp/Trung Bình/Cao)"
        }}
        """
        
        # Cấu hình tính quy chuẩn (Governance)
        config = genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.1 # Độ lạnh lùng, loại bỏ cảm xúc phi lý trí
        )
        
        response = self.model.generate_content(prompt, generation_config=config)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
             raise ValueError(f"Lỗi Format: Agent trả về sai chuẩn JSON. RAW: {response.text}")
