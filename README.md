# NQH_vn-portfolio-orchestrator (NPO)

## Tuyên bố
> "AI không phải lợi thế cạnh tranh, kỷ luật mới là lợi thế"

## Giới thiệu
NQH_vn-portfolio-orchestrator (NPO) là một công cụ đầu tư chứng khoán Việt Nam được định hướng Agentic AI và quản trị chặt chẽ (Governance). Với cốt lõi tập trung vào quản trị rủi ro và các quyết định kỷ luật dựa trên dữ liệu, NPO giúp tự động hóa khâu phân tích và bảo vệ lợi nhuận kỳ vọng một cách bền vững.

## Tiêu chí
**Dự án**: NQH_VN-Portfolio-Orchestrator  
**Kiến trúc**: TinySDLC Framework  
**Ngôn ngữ**: Python 3.10+ (Security focus)  
**AI Engine**: Gemini 3.1 Flash API  
**Mục tiêu lợi nhuận**: 15-18%  

## Cấu trúc dự án
Dự án kế thừa triết lý từ TinySDLC của A Tài, bao gồm mã nguồn (`src/`), đặc tả tác vụ (`.missions/`), định nghĩa tác vụ Agent (`.agents/`), và khuôn mẫu kiến trúc (`docs/patterns/`).

## Giấy phép (License)
Dự án được phân phối dưới giấy phép MIT License.

---

## 🚀 Hướng Dẫn Sử Dụng (Dành cho người mới)

Dự án này được thiết kế theo đúng triết lý "Nhỏ nhưng dùng được", chạy hoàn toàn trên máy cá nhân cục bộ (Local) của bạn. Hệ thống hoạt động như một Trợ lý AI (Agent) đa kênh để quét, phân tích và báo động chứng khoán.

### 1. Chuẩn Bị Môi Trường
Đảm bảo máy tính của bạn đã cài đặt **Python 3.10** trở lên.

Mở Terminal (Command Prompt hoặc PowerShell) và chạy các dòng lệnh sau để tải dự án về máy:
```bash
git clone https://github.com/Quanghoaai/NQH_vn-portfolio-orchestrator.git
cd NQH_vn-portfolio-orchestrator
```

Tạo một môi trường ảo (Virtual Environment) để cài đặt các thư viện không bị xung đột với hệ thống:
```bash
python -m venv venv
```
Kích hoạt môi trường vừa tạo:
- **Windows**: `.\venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

Tiếp theo, hãy cài đặt toàn bộ "vũ khí" cần thiết bằng lệnh:
```bash
pip install -r requirements.txt
```

### 2. Cấu Hình Sức Mạnh (API Keys)
Chìa khóa để bật bộ não AI và hệ thống thông báo là file `.env`. 
Nhân bản (copy) nội dung tệp ở dự án ra thành tự tạo mới tên `.env` ngay trong thư mục gốc (ngang hàng `README.md`) và dán thông tin của bạn vào:

```env
# 1. API Key của Google Gemini (Lấy miễn phí tại: https://aistudio.google.com/)
GEMINI_API_KEY=AIzaSy_CUA_BAN_O_DAY

# 2. Hệ thống cảnh báo Telegram (Lấy từ BotFather)
TELEGRAM_BOT_TOKEN=TOKEN_BOT_CUA_BAN
TELEGRAM_CHAT_ID=CHAT_ID_CUA_BAN
```

### 3. Vận Hành Tác Chiến
Chúng tôi đã setup sẵn 3 module để bạn có thể sử dụng sức mạnh Agent tùy theo nhu cầu:

#### a. Quét Mẫu Dữ Liệu Live (Check kết nối 1 mã)
File này sẽ kéo dữ liệu của Tập đoàn Hòa Phát (HPG) ngay tại thời điểm thực và nhờ Gemini phân tích chốt lời.
```bash
python run_hpg.py
```

#### b. Chế Độ Thợ Săn Định Kỳ (Auto-Scanner)
Đây là trái tim của hệ thống. Bạn gõ lệnh này, nó sẽ âm thầm quét tự động danh mục (FPT, MWG, SSI...) và sẽ báo thẳng "tinh tinh" vào điện thoại Telegram nếu định tuyến có siêu Cổ Phiếu vượt mốc 15% - 18%.
```bash
python run_scanner.py
```

#### c. Chế Độ Đánh Giá Độ Thông Minh (Backtest)
Kiểm tra độ nhạy (Sensitivity) của AI đối với tín hiệu Xấu / Tốt của thị trường bằng cách quét 10 mã cổ phiếu lớn với đủ kiểu rủi ro và cơ hội. File log ghi lại sẽ được xuất dưới định dạng có thể đọc trên Excel ở `logs/backtest_journal.csv` để bạn dễ dàng quản trị (Governance).
```bash
python run_backtest.py
```

---

## Đẩy Code Lên GitHub: AI Giúp Tăng Tốc, Governance Giúp Không Lao Xuống Vực.
📖 **CÂU CHUYỆN THỰC CHIẾN: TỪ ASSEMBLER 2006 ĐẾN AGENTIC AI 2026** 
*Hành trình 20 năm: Từ những dòng lệnh hợp ngữ đến kỷ nguyên điều phối Agent.*

Năm 2006, tôi bắt đầu những bước chân đầu tiên vào thế giới lập trình với Assembler và C++. Đó là thời điểm của những tư duy logic tầng thấp, nơi mỗi ô nhớ và thanh ghi đều đòi hỏi sự chính xác tuyệt đối.

Đến năm 2009, tôi rẽ hướng sang lĩnh vực Viễn thông, gắn bó với hạ tầng 2G và 3G. Suốt hơn một thập kỷ, tôi tập trung vào quản trị và vận hành hệ thống — những công việc đòi hỏi sự bền bỉ nhưng dần rời xa việc trực tiếp viết mã.

Bước ngoặt đến vào năm 2020. Khi tham gia khóa học Data Analyst tại FUNiX, tôi tiếp xúc với Python. Từ những dòng code xử lý dữ liệu đầu tiên, tôi nhận ra sức mạnh của tự động hóa. Nhưng phải đến khi cơn bão AI ập đến, tôi mới thực sự hiểu: Tốc độ của AI là vô nghĩa nếu thiếu đi sự kỷ luật trong quy trình.

03 tháng. 09 phiên bản. 06 dự án thực chiến. Tôi chứng kiến nhiều hệ thống ứng dụng AI "vỡ trận" vì sai lầm trong logic hoặc rò rỉ bảo mật. Tôi không đổ lỗi cho AI. Tôi hiểu rằng không thể yêu cầu hệ thống thay đổi nếu chính mình không làm gương. Tôi tự học lại từ đầu, áp dụng kinh nghiệm quản trị viễn thông vào cấu trúc lập trình hiện đại:

`Python (Security focus) → Gemini 3.1 Flash → Google Antigravity IDE → Gemini CLI.`

Mỗi lần hệ thống phát sinh lỗi là một "Pattern" được tôi đóng gói thành quy tắc. Ở tuổi 45, tôi không còn viết những đoạn code rời rạc. Tôi xây dựng `NQH_vn-portfolio-orchestrator (NPO)` — một thứ "nhỏ nhưng dùng được", chạy local, chat-native để thực thi kỷ luật tài chính cho chính mình.

Tôi rút ra một điều: **AI không phải lợi thế cạnh tranh. Kỷ luật mới là lợi thế cạnh tranh.**

Hôm nay, tôi chia sẻ dự án open-source này (MIT License) với hy vọng giúp cộng đồng nhà đầu tư Việt Nam có một bộ khung quản trị vững chắc. Nếu bạn đang dùng AI để code hoặc đầu tư mà chưa có cấu trúc — hãy vào repo xem thử. Nếu hữu ích: Star, mở Issue, hoặc PR góp ý/phản biện.

🔗 **Repo NPO**: https://github.com/Quanghoaai/NQH_vn-portfolio-orchestrator

#OpenSource #MITLicense #AICoding #SoftwareEngineering
