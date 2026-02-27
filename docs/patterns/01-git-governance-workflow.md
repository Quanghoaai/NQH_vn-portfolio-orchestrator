# Đẩy Code Lên GitHub: AI Giúp Tăng Tốc, Governance Giúp Không Lao Xuống Vực.

30 năm trước, lần cuối tôi quản lý phiên bản phần mềm là bằng những thư mục nén `.zip` chép qua đĩa mềm — đề án tốt nghiệp 1994. Tư duy tuần tự ảnh hưởng sâu đến cách tôi làm việc. Rồi tôi rẽ sang quản trị — và không trực tiếp gõ lệnh lưu trữ nữa.

Cho đến khi làm việc với Agentic AI.

Tôi dùng AI để dựng NQH_vn-portfolio-orchestrator (NPO). AI sinh code cực nhanh. Từ Vault, Analyzer, đến Scanner. Nhưng tôi nhanh chóng nhận ra một sự thật trần trụi: “Sinh code nhanh chỉ để hệ thống sụp đổ nhanh hơn nếu bạn không kiểm soát được các phiên bản.” 

Tôi chứng kiến những dự án đắp code AI liên tục, chạy trên Local rất mượt, nhưng đến lúc đưa lên GitHub thì "vỡ trận": Lộ API Key, rác file hệ thống (`__pycache__`), mất dấu vết không biết code này sửa từ lúc nào, vì sao lại sửa. Chi phí tìm lỗi đắt gấp 10 lần thời gian nhờ AI viết.

Tôi không đổ lỗi cho AI. Hay đổ lỗi cho Git. Tôi xây framework.
Mỗi lần "vỡ" khi push code là một bài học. Mỗi bài học được đóng thành quy tắc. 
Trong kiến trúc TinySDLC của NPO, luồng đẩy code lên GitHub cũng phải "Nhỏ nhưng dùng được", được kiểm soát bằng Governance.

Dưới đây là **Quy trình 4 Bước (Governance Workflow)** để đẩy mã nguồn NPO lên GitHub. Không cảm xúc. Rõ ràng. Và kỷ luật.

---

### Bước 1: Kiểm toán trước khi xuất kích (Thấu hiểu sự thay đổi)
Đừng bao giờ đẩy lên đám mây thứ mà bạn không biết rõ nó là gì. Giống như trước khi ra quyết định đầu tư, phải xem kỹ báo cáo.

```bash
git status
```
*Governance Rule:* Lệnh này giúp bạn nhìn thấy rành mạch file nào bị sửa (màu đỏ). Nếu có file `.env` hay `NPO_MASTER_KEY` xuất hiện ở đây, dừng lại ngay lập tức! Bạn đang đối mặt với thảm họa bảo mật. Hãy đảm bảo `.gitignore` đã làm tốt nhiệm vụ khiên chắn.

### Bước 2: Đóng gói vào vùng Kỷ luật (Staging)
Đưa các file đã kiểm toán vào trạng thái sẵn sàng ghi nhận.

```bash
git add .
```
*Governance Rule:* Dấu `.` đại diện cho sự chấp nhận toàn bộ khu vực làm việc. Chỉ gõ lệnh này khi đã chắc chắn bộ Test (Pytest) chạy Passed 100% ở Local. Tuyệt đối không đưa code lỗi lên Staging.

### Bước 3: Định danh trách nhiệm (Semantic Commit)
Một đoạn log không có cấu trúc vô giá trị hệt như một báo cáo tài chính rác. Đừng dùng những câu vô nghĩa như *"update code", "fix lỗi"*. Hãy dùng chuẩn Semantic.

```bash
git commit -m "feat(core): implement Mission 07 - trade log journaling"
```
*Governance Rule:* Mỗi commit phải gắn liền với một Mission cụ thể.
- Dùng `feat(tên_module)` cho tính năng mới.
- Dùng `fix(tên_module)` khi vá lỗi.
- Dùng `chore(tên_module)` cho cấu hình hệ thống (như Git, Env).

### Bước 4: Chuyển giao lên tầng Cloud (Push)
Hoàn tất chu kỳ phát triển, tích hợp di sản vào Repo trung tâm.

```bash
git push origin main
```
*Governance Rule:* Nếu có xung đột (Conflict), tức là kiến trúc đang chồng chéo. Không dùng cờ ép lệnh (`--force`) trừ khi bạn hiểu rõ mình đang ghi đè lên lịch sử nào.

---

Sau hành trình xây dựng 7 Mission đầu tiên của NPO, tôi thao tác hàng chục lần vòng lặp Git này. 
Tôi rút ra 1 điều: **AI không ghép các mảnh vỡ lại cho bạn. Kỷ luật phiên bản mới là lợi thế cạnh tranh.**

Nếu bạn đang dùng AI để viết code khối lượng lớn mà chưa có một tiêu chuẩn Commit và Version Control rõ ràng — hệ thống của bạn chỉ đang chực chờ sụp đổ.

Nếu thấy hướng dẫn này hữu ích, hãy áp dụng nó như một Pattern cốt lõi trong chính dự án NPO của chúng ta!

#TinySDLC #Governance #AgenticAI #GitWorkflow #SoftwareEngineering #NPO
