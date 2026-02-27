# Mission 07: Log Journaling (Nhật Ký Giao Dịch)
- **Goal**: Ghi vết vĩnh viễn mọi phán quyết của Agent (Buy/Hold/Sell) vào file hệ thống để kiểm toán theo Governance Rule.
- **Status**: Done
- **Task**: 
  - Tạo module `src/core/journal.py`.
  - Format Logs dạng CSV (`logs/trade_journal.csv`) để dễ dàng phân tích trên Excel (Ticker, Action, Target Yield, Confidence, Reasoning, Timestamp).
  - Kết nối Journal vào luồng chạy Backtest và Scanner.
