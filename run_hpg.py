import os
import sys
import json
from dotenv import load_dotenv

# Đảm bảo đường dẫn module gốc
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

# Đọc cấu hình từ .env
load_dotenv()

# Gọi động Analyzer Flash (vì thư mục chứa dấu chấm .agents)
import importlib.util
spec = importlib.util.spec_from_file_location("analyzer_flash", os.path.join(base_dir, ".agents", "skills", "analyzer-flash.py"))
analyzer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer_module)
AnalyzerFlash = analyzer_module.AnalyzerFlash

def run_test_hpg():
    # Trong môi trường Local Governance, API Key thường nằm trong Vault.
    # Trong bản demo test này, chúng ta nạp thẳng từ biến môi trường GEMINI_API_KEY.
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("🚨 LỖI: Không tìm thấy GEMINI_API_KEY.")
        print("Vui lòng tạo file '.env' ở thư mục gốc và thêm dòng:")
        print("GEMINI_API_KEY=AIzaSy...your_real_key_here")
        return

    print("🛡️ NPO System: Đang khởi tạo bộ não Analyzer Flash...")
    try:
        analyzer = AnalyzerFlash(gemini_api_key=api_key)
    except Exception as e:
        print(f"Lỗi khởi tạo: {e}")
        return

    from src.adapters.market_data import MarketDataAdapter
    print("🌐 Đang kết nối MarketDataAdapter kéo Live Data từ Yahoo Finance...")
    adapter = MarketDataAdapter()
    
    try:
        hpg_financial_report = adapter.generate_financial_report("HPG")
        hpg_market_context = adapter.get_market_context()
        print("✅ Đã lấy dữ liệu thật (Live) thành công!\n")
    except Exception as e:
        print(f"🚨 Lỗi kết nối Market Data: {e}")
        return

    print("📊 Đang tiến hành chưng cất dữ liệu HPG...")
    print(f"Target Yield định tuyến: 15-18%")
    print("Đang truyền Live Data lên Gemini API...\n")

    try:
        # Gọi thực thi phân tích
        result = analyzer.analyze_stock(
            ticker="HPG",
            financial_report=hpg_financial_report,
            market_context=hpg_market_context
        )
        
        print("✅ KẾT QUẢ TỪ AGENT (JSON Output):")
        print("="*50)
        print(json.dumps(result, indent=4, ensure_ascii=False))
        print("="*50)
        print("="*50)

    except Exception as e:
        import traceback
        print(f"🚨 Lỗi trong quá trình AI xử lý: {e}")
        traceback.print_exc()
if __name__ == "__main__":
    run_test_hpg()
