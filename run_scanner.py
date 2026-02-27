import os
import sys
import time
import schedule
from dotenv import load_dotenv

# Đảm bảo đường dẫn module gốc
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

# Đọc cấu hình từ .env
load_dotenv()

# Nạp động Analyzer Flash (Bộ não AI)
import importlib.util
spec = importlib.util.spec_from_file_location("analyzer_flash", os.path.join(base_dir, ".agents", "skills", "analyzer-flash.py"))
analyzer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer_module)
AnalyzerFlash = analyzer_module.AnalyzerFlash

from src.adapters.market_data import MarketDataAdapter
from src.adapters.notifier import Notifier

# ==========================================
# CẤU HÌNH DANH SÁCH THEO DÕI (WHITELIST)
# ==========================================
PORTFOLIO_WATCHLIST = [
    "HPG", # Thép
    "FPT", # Công nghệ
    "SSI", # Chứng khoán
    "MBB", # Ngân hàng
    "MWG"  # Bán lẻ
]

# Thời gian nghỉ (Sleep) giữa các lần gọi AI để tránh dính Rate Limit của Google (15 RPM cho free tier)
DELAY_BETWEEN_REQUESTS = 10 # Giây

def scan_single_stock(ticker: str, analyzer: AnalyzerFlash, adapter: MarketDataAdapter, notifier: Notifier):
    """Quy trình chưng cất 1 mã duy nhất."""
    print(f"\n🔍 [SCANNER] Đang cào dữ liệu Live cho mã: {ticker}...")
    try:
        financial_report = adapter.generate_financial_report(ticker)
        market_context = adapter.get_market_context()
        
        print(f"🧠 [SCANNER] Nhờ Gemini AI chưng cất {ticker}...")
        result = analyzer.analyze_stock(
            ticker=ticker,
            financial_report=financial_report,
            market_context=market_context
        )
        
        # Chỉ đẩy Noti ra Telegram nếu Hành động là BUY (MUA)
        # Bỏ qua HOLD, tránh SPAM điện thoại
        if result.get("action") == "BUY":
            notifier.notify_trade_signal(result)
        else:
            # Vẫn in ra Terminal để theo dõi ngầm
            notifier.console_alert(f"GIỮ TRẠNG THÁI: {ticker}", f"Lý do: {result.get('reasoning')}", level="HOLD")
            
    except Exception as e:
        import traceback
        notifier.console_alert(f"LỖI QUÉT MÃ {ticker}", str(e), level="WARNING")

def run_portfolio_scan():
    """Hàm chạy chuỗi sự kiện quét toàn bộ Watchlist."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("🚨 LỖI: Không tìm thấy GEMINI_API_KEY trong .env")
        return

    print("\n" + "="*60)
    print("🚀 NPO: BẮT ĐẦU CHU KỲ QUÉT TỰ ĐỘNG DANH MỤC")
    print(f"📋 Danh sách theo dõi: {PORTFOLIO_WATCHLIST}")
    print("="*60)

    try:
        analyzer = AnalyzerFlash(gemini_api_key=api_key)
        adapter = MarketDataAdapter()
        notifier = Notifier()
    except Exception as e:
        print(f"Lỗi khởi tạo hệ thống: {e}")
        return

    for ticker in PORTFOLIO_WATCHLIST:
        scan_single_stock(ticker, analyzer, adapter, notifier)
        print(f"⏳ Nghỉ {DELAY_BETWEEN_REQUESTS}s để tránh Anti-spam AI...\n")
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
    print("✅ ĐÃ HOÀN THÀNH QUÁ TRÌNH QUÉT DANH MỤC.")

if __name__ == "__main__":
    print("🟢 Khởi động NPO Auto-Scanner...")
    
    # 1. Chạy quét ngay lập tức khi vừa bật file
    run_portfolio_scan()
    
    # 2. Lên lịch chạy định kỳ
    # Ví dụ: Chạy quét mỗi ngày vào lúc 14:00 (Gần phiên ATC để ra quyết định đóng nến)
    # Tùy ý bạn thay đổi thời gian này!
    schedule.every().day.at("14:00").do(run_portfolio_scan)
    
    print("⚙️ Hệ thống đang ngủ đông chờ đến lịch quét tiếp theo...")
    print("⚠️ Bấm Ctrl+C để thoát.")
    
    # Vòng lặp vĩnh cửu ngầm giữ cho Script sống
    while True:
        try:
            schedule.run_pending()
            time.sleep(60) # Cứ 60s thức dậy 1 lần để xem tới lịch chưa
        except KeyboardInterrupt:
            print("\n⏹️ Đã tắt NPO Auto-Scanner.")
            sys.exit(0)
