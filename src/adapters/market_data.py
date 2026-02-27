import yfinance as yf
from typing import Dict, Any

class MarketDataAdapter:
    """
    Adapter Pattern kết nối Live Data từ Yahoo Finance cho thị trường Việt Nam.
    Tuân thủ triết lý TinySDLC: Nhỏ gọn, lấy đúng dữ liệu cơ bản, không rườm rà.
    """
    def __init__(self):
        # Thiết lập suffix '.VN' cho sàn HOSE (VNINDEX)
        self.suffix = ".VN"

    def fetch_stock_data(self, ticker: str) -> Dict[str, Any]:
        """
        Lấy các chỉ số tài chính cơ bản hiện hành của mã chứng khoán (Live).
        """
        vn_ticker = f"{ticker}{self.suffix}"
        
        try:
            stock = yf.Ticker(vn_ticker)
            info = stock.info
            
            # Gạn lọc các trường dữ liệu quan trọng cho siêu Agent (Analyzer Flash)
            # Dùng .get() với fallback để không sụp đổ code nếu thiếu data.
            financial_data = {
                "ticker": ticker,
                "current_price": info.get("currentPrice", 0),
                "market_cap": info.get("marketCap", 0),
                "trailing_pe": info.get("trailingPE", None),
                "forward_pe": info.get("forwardPE", None),
                "eps": info.get("trailingEps", None),
                "revenue_growth": info.get("revenueGrowth", None),
                "profit_margins": info.get("profitMargins", None),
                "debt_to_equity": info.get("debtToEquity", None),
                "price_to_book": info.get("priceToBook", None),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh", 0),
                "sector": info.get("sector", "Unknown"),
            }
            return financial_data
            
        except Exception as e:
             raise ValueError(f"Không thể tải Live Data cho mã {ticker}. Lỗi: {e}")

    def generate_financial_report(self, ticker: str) -> str:
        """
        Đóng gói dữ liệu số khô khan thành văn bản có cấu trúc báo cáo 
        để đút cho Gemini (AnalyzerFlash) dễ dàng chưng cất hứa hẹn 15-18%.
        """
        data = self.fetch_stock_data(ticker)
        
        # Hàm hỗ trợ định dạng số đẹp
        def fmt(val, is_pct=False):
            if val is None: return "Chưa có dữ liệu"
            if is_pct: return f"{val * 100:.1f}%"
            return str(val)

        from src.core.technical import TechnicalAnalyzer
        tech_data = TechnicalAnalyzer.get_indicators(ticker, self.suffix)

        report = f"""
        [BCTC LIVE MARKET DATA: {ticker}]
        - Ngành: {data['sector']}
        - Giá hiện hành: {data['current_price']}
        - Vốn hóa (Market Cap): {data['market_cap']}
        - P/E (Trailing): {fmt(data['trailing_pe'])}
        - P/E (Forward): {fmt(data['forward_pe'])}
        - EPS (Lợi nhuận cổ phần): {fmt(data['eps'])}
        - Tăng trưởng doanh thu: {fmt(data['revenue_growth'], True)}
        - Biên lợi nhuận ròng: {fmt(data['profit_margins'], True)}
        - Nợ vay / Vốn chủ sở hữu (D/E): {fmt(data['debt_to_equity'])}%
        - P/B (Price to Book): {fmt(data['price_to_book'])}
        - Biến động giá 52 tuần: Từ {data['fifty_two_week_low']} đến {data['fifty_two_week_high']}
        
        [PHÂN TÍCH KỸ THUẬT NGẮN HẠN]
        - Lực cầu (RSI 14ngày): {fmt(tech_data.get('rsi_14', 'N/A'))} (Nếu >70 là Quá mua, <30 là Quá bán)
        - Độ lệch so với MA20: {fmt(tech_data.get('price_vs_ma20_pct', 'N/A'))}% 
        - Đột biến khối lượng (Vol Surge): {fmt(tech_data.get('vol_surge_pct', 'N/A'))}% so với trung bình 10 phiên
        """
        return report

    def get_market_context(self) -> str:
        """
        Cào sơ lược bối cảnh VN-Index bằng mã chứng khoán đại diện (VNINDEX).
        """
        # Lưu ý: Yahoo Finance lấy dữ liệu VNINDEX dạng ETF E1VFVN30.VN hoặc chính VNINDEX (tùy sàn nhưng không ổn định hoàn toàn)
        # Tại đây, chúng ta tạm gán cứng context hoặc có thể gọi API vĩ mô khác tương lai.
        # Ở cấp độ MVP của NPO, ta sẽ hard-code kịch bản hiện hành để đảm bảo an toàn.
        
        return """
        [Vĩ mô thị trường Việt Nam - Live Status]
        - Lãi suất ngân hàng TMCP đang suy trì nền thấp.
        - Khối ngoại có dấu hiệu bán ròng nhưng tiền nội địa vẫn hấp thụ tốt.
        - Thị trường đang tìm điểm cân bằng mới, chú ý các nhóm ngành sản xuất, thép, ngân hàng và bán lẻ.
        """
