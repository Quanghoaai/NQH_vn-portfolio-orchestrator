import os
import sys
import time
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
load_dotenv()

# Nạp động Analyzer Flash (Bộ não AI)
import importlib.util
spec = importlib.util.spec_from_file_location("analyzer_flash", os.path.join(base_dir, ".agents", "skills", "analyzer-flash.py"))
analyzer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer_module)
AnalyzerFlash = analyzer_module.AnalyzerFlash

from src.adapters.market_data import MarketDataAdapter
from src.core.journal import TradeJournal

# Tập 10 mã đại diện đa dạng mọi nhóm ngành
BACKTEST_WATCHLIST = [
    "HPG", # Thép cơ bản (Tốt)
    "VHM", # Bất động sản Vinhomes (Biên lợi nhuận cao nhưng rủi ro dòng tiền)
    "NVL", # Bất động sản Novaland (Cảnh báo nợ khổng lồ)
    "VCB", # Ngân hàng (Chỉ số cực đẹp nhưng có thể bị đắt)
    "VPB", # Ngân hàng (Biên lợi nhuận cao nhưng nợ xấu FE)
    "DGC", # Hóa chất cơ bản (Tài chính cực sạch)
    "HAG", # Nông nghiệp (Tái cơ cấu)
    "MWG", # Bán lẻ (Phục hồi mảng Bách Hóa)
    "FPT", # Công nghệ
    "VIX"  # Chứng khoán tự doanh (Lợi nhuận gập ghềnh)
]

DELAY_BETWEEN_REQUESTS = 5 # Giây (Chạy Backtest nhanh hơn Scanner 1 chút)

def run_historical_sensitivity_test():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("LỖI: Thiếu API KEY")
        return

    print("="*60)
    print("🔬 NPO BACKTESTING: KIỂM TRA ĐỘ NHẠY(SENSITIVITY) TRUY XUẤT CỦA AI TRÊN 10 MÃ")
    print("Mục tiêu: Đánh giá xem AI có tỉnh táo bỏ qua những mã rác/kém an toàn hay không.")
    print("="*60)

    analyzer = AnalyzerFlash(gemini_api_key=api_key)
    adapter = MarketDataAdapter()
    journal = TradeJournal(filename="backtest_journal.csv") # Tạo file Backtest riêng

    for ticker in BACKTEST_WATCHLIST:
        print(f"\n[{ticker}] Đang kéo Live Data và chưng cất...")
        try:
            financial_report = adapter.generate_financial_report(ticker)
            market_context = adapter.get_market_context()
            
            result = analyzer.analyze_stock(
                ticker=ticker,
                financial_report=financial_report,
                market_context=market_context
            )
            
            # Lưu vết Journal
            journal.log_trade(result)
            
            action = result.get('action')
            reason = result.get('reasoning')
            
            # Chỉ Report ngắn gọn ra Terminal (Không đẩy Telegram làm phiền Alert thực chiến)
            indicator = "🟢 BUY" if action == "BUY" else "🔴 SELL" if action == "SELL" else "⏸️ HOLD"
            print(f"-> {indicator} | Phản biện: {reason}")
            
        except Exception as e:
            print(f"-> 🚨 LỖI ({ticker}): {e}")
            
        time.sleep(DELAY_BETWEEN_REQUESTS)

    print("\n✅ THÀNH CÔNG: Mở file `logs/backtest_journal.csv` để xem toàn bộ quá trình Backtest.")

if __name__ == "__main__":
    run_historical_sensitivity_test()
