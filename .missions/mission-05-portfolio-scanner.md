# Mission 05: Portfolio Scanner (Scale-up)
- **Goal**: Nâng cấp từ phân tích 1 mã tĩnh thành quét 1 danh sách mã theo chu kỳ.
- **Status**: Done
- **Task**: 
  - Khởi tạo thư viện `schedule` để chạy tác vụ tự động lặp lại (ví dụ: mỗi ngày 1 lần hoặc mỗi giờ).
  - Viết file `run_scanner.py` để duyệt qua một danh sách cấu hình sẵn các mã chứng khoán (Whitelist: HPG, FPT, SSI, MBB, MWG...).
  - Thêm cơ cấu trì hoãn (sleep/delay) giữa các lần gọi API Gemini để tránh bị quét spam (Rate Limit).
  - Kết xuất Log tổng hợp và bắn Alert riêng biệt cho từng mã vượt ngưỡng an toàn.
