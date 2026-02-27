import os
import csv
from datetime import datetime

class TradeJournal:
    """
    Module Ghi Nhật Ký (Journaling System)
    Tuân thủ Governance Rule: Mọi quyết định của AI phải được kiểm toán và lưu vết.
    Lưu dữ liệu đầu ra vào CSV để dễ dàng Import Excel, Pandas backtest.
    """
    def __init__(self, log_dir: str = "logs", filename: str = "trade_journal.csv"):
        # Lấy file tuyệt đối để tránh chạy lệch thư mục root
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.log_path = os.path.join(base_path, log_dir)
        self.file_path = os.path.join(self.log_path, filename)
        
        # Đảm bảo thư mục logs tồn tại
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
            
        # Nếu file chưa tồn tại thì ghi Header (Tiêu đề cột) trước
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", 
                    "Ticker", 
                    "Action", 
                    "Target Yield", 
                    "Safety Margin", 
                    "Confidence Score", 
                    "Reasoning"
                ])

    def log_trade(self, agent_result: dict):
        """Hàm lưu kết quả nhả ra từ AI (Dict) thành một Record trong CSV."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Bắt lỗi nếu Model phản hồi thiếu các khoá dữ liệu (Fallbacks)
        ticker = agent_result.get("ticker", "UNKNOWN")
        action = agent_result.get("action", "HOLD")
        target_yield = agent_result.get("target_yield", "N/A")
        safety_margin = agent_result.get("safety_margin", "N/A")
        confidence = agent_result.get("confidence_score", "0")
        reasoning = agent_result.get("reasoning", "Không rõ nguyên nhân.")
        
        # Sanitize Reasoning (bỏ ký tự newline để CSV không bị lệch dòng)
        reasoning = reasoning.replace("\n", " ").replace("\r", " ")
        
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                ticker,
                action,
                target_yield,
                safety_margin,
                confidence,
                reasoning
            ])
        
        return True
