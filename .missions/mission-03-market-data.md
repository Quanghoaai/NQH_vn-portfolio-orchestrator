# Mission 03: Market Data Adapter (Real-time feed)
- **Goal**: Xây dựng cầu nối (Adapter) để hút dữ liệu chứng khoán thật từ thị trường.
- **Status**: Done
- **Task**: 
  - Đánh giá và tích hợp thư viện lấy dữ liệu tài chính (ưu tiên `yfinance` vì Google Finance không có API chính thức mượt mà bằng).
  - Viết module `src/adapters/market_data.py` để kéo giá lịch sử và chỉ số cơ bản (P/E, EPS, Doanh thu...).
  - Thiết kế hàm Adapter trả về đúng định dạng mà Analyzer Flash (Gemini) mong đợi ở `mission-02`.
  - Viết Unit Test đảm bảo việc kéo live data cho VN-Index và mã HPG thành công.
