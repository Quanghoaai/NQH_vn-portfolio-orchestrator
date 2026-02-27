import os
import requests
from colorama import init, Fore, Style

# Khởi tạo colorama để hiển thị màu trên Terminal Windows/Linux
init(autoreset=True)

class Notifier:
    """
    Module Cảnh Báo Đa Kênh (Terminal + Telegram)
    Trách nhiệm: Đẩy tín hiệu Agentic đã xử lý đến người dùng cuối.
    """
    def __init__(self):
        # Lấy token thông qua môi trường (hoặc Vault trong tương lai)
        self.telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    def console_alert(self, title: str, message: str, level: str = "INFO"):
        """In thông báo ra màn hình Console/Terminal với màu sắc."""
        if level == "BUY":
            color = Fore.GREEN + Style.BRIGHT
            icon = "🟢"
        elif level == "SELL":
            color = Fore.RED + Style.BRIGHT
            icon = "🔴"
        elif level == "WARNING":
            color = Fore.YELLOW + Style.BRIGHT
            icon = "⚠️"
        else:
            color = Fore.CYAN + Style.BRIGHT
            icon = "ℹ️"

        # Hiển thị Terminal
        print(f"\n{color}[{icon} {level}] {title}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTWHITE_EX}{message}{Style.RESET_ALL}\n")
        print("-" * 50)

    def telegram_alert(self, title: str, message: str) -> bool:
        """Đẩy cảnh báo trực tiếp qua Telegram REST API."""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            self.console_alert(
                "TELEGRAM CONFIG MISSING", 
                "Không tìm thấy TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong .env. Bỏ qua gửi Telegram.", 
                "WARNING"
            )
            return False

        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        
        # Định dạng văn bản sử dụng HTML của Telegram
        telegram_msg = f"<b>🚨 {title}</b>\n\n{message}\n\n<i>--NPO Agent System--</i>"
        
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": telegram_msg,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                self.console_alert("TELEGRAM SENT", "Đã gửi thông báo đến điện thoại thành công!", "INFO")
                return True
            else:
                self.console_alert("TELEGRAM FAILED", f"Lỗi API: {response.text}", "WARNING")
                return False
        except Exception as e:
            self.console_alert("TELEGRAM ERROR", f"Lỗi mạng khi kết nối Telegram: {str(e)}", "WARNING")
            return False

    def notify_trade_signal(self, agent_result: dict):
        """Hàm tích hợp kết quả JSON của AnalyzerFlash thành chuỗi cảnh báo."""
        action = agent_result.get("action", "HOLD")
        ticker = agent_result.get("ticker", "UNKNOWN")
        target_yield = agent_result.get("target_yield", "N/A")
        safety_margin = agent_result.get("safety_margin", "N/A")
        reasoning = agent_result.get("reasoning", "Không có lý do rõ ràng.")
        
        title = f"TÍN HIỆU GIAO DỊCH NPO: {action} {ticker}"
        
        message = (
            f"🎯 Target Yield: {target_yield}\n"
            f"🛡️ Biên an toàn: {safety_margin}\n"
            f"🧠 AI Phân tích: {reasoning}"
        )
        
        # 1. Hiển thị Console cục bộ
        self.console_alert(title, message, level=action)
        
        # 2. Đẩy ra thiết bị cá nhân (Telegram)
        self.telegram_alert(title, message)
