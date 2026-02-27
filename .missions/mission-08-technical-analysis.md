# Mission 08: Technical Analysis (Con Mắt Phân Tích Kỹ Thuật)
- **Goal**: Cung cấp thêm "Vũ khí" phân tích kỹ thuật (Technical Analysis) cho Agent để đánh giá Lực Đáy, Dòng Tiền và Xung Lực Mua/Bán trước khi chốt lệnh.
- **Status**: Pending
- **Task**: 
  - Xây dựng module xử lý thuật toán `src/core/technical.py`.
  - Tính toán các chỉ báo Cơ bản nhưng cực kỳ quyền lực: RSI (Xung lực - Quá mua/Quá bán), MA20 (Xu hướng ngắn hạn) và Đột biến Khối lượng (Volume Surge).
  - Tích hợp số liệu này vào Bản Cáo Bạch của `MarketDataAdapter` để truyền cho Gemini.
  - Test lại hệ thống với `run_scanner.py` hoặc `run_backtest.py` để xem AI có từ chối các mã "Quá Mua" (RSI > 70) hay không.
