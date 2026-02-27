import pandas as pd
import yfinance as yf

class TechnicalAnalyzer:
    """
    Module Phân Tích Kỹ Thuật (Technical Analysis)
    Nhiệm vụ: Cung cấp 3 chỉ báo quyền lực giúp Agent chốt Lực Đáy/Đỉnh.
    1. RSI 14 (Chỉ báo xung lượng Mua/Bán)
    2. MA 20 (Đường trung bình giá 20 ngày biểu thị xu hướng ngắn hạn)
    3. Volume Surge (Khối lượng Đột Biến so với trung bình 10 phiên)
    """

    @staticmethod
    def calculate_rsi(series: pd.Series, periods: int = 14) -> float:
        """Thuật toán Smoothed RSI chuẩn Wilder."""
        if len(series) < periods:
            return 50.0  # Mặc định trung lập nếu thiếu dữ liệu
            
        delta = series.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        
        # Exponential Moving Average cho RSI chuẩn
        ema_up = up.ewm(com=periods - 1, adjust=False).mean()
        ema_down = down.ewm(com=periods - 1, adjust=False).mean()
        
        rs = ema_up / ema_down
        rsi = 100 - (100 / (1 + rs))
        
        val = rsi.iloc[-1]
        return float(val) if not pd.isna(val) else 50.0

    @staticmethod
    def get_indicators(ticker: str, suffix: str = ".VN") -> dict:
        """Kéo nến (Candlestick) quá khứ để tính Technical."""
        vn_ticker = f"{ticker}{suffix}"
        
        try:
            # Lấy nến 3 tháng gần nhất để tính cho láng mịn
            stock = yf.Ticker(vn_ticker)
            history = stock.history(period="3mo")
            
            if history.empty:
                return {}

            close = history['Close']
            volume = history['Volume']

            current_price = close.iloc[-1]
            
            # 1. Đường Xu Hướng MA20
            ma20 = close.rolling(window=20).mean().iloc[-1]
            price_vs_ma20 = ((current_price - ma20) / ma20) * 100 if pd.notna(ma20) and ma20 != 0 else 0
            
            # 2. Xung Lực RSI 14
            rsi14 = TechnicalAnalyzer.calculate_rsi(close, 14)
            
            # 3. Lực Cầu (Volume Surge)
            current_vol = volume.iloc[-1]
            avg_vol_10d = volume.rolling(window=10).mean().iloc[-1]
            vol_surge_pct = ((current_vol - avg_vol_10d) / avg_vol_10d) * 100 if pd.notna(avg_vol_10d) and avg_vol_10d > 0 else 0

            return {
                "rsi_14": round(rsi14, 2),
                "ma_20": round(ma20, 2),
                "price_vs_ma20_pct": round(price_vs_ma20, 2),
                "current_volume": int(current_vol) if pd.notna(current_vol) else 0,
                "avg_volume_10d": int(avg_vol_10d) if pd.notna(avg_vol_10d) else 0,
                "vol_surge_pct": round(vol_surge_pct, 2)
            }
        except Exception as e:
            # Trả về Dict rỗng nếu lỗi để không chết hàm Adapter
            print(f"Lỗi tính toán Kỹ thuật mã {ticker}: {e}")
            return {}
