#  Sentinel - Hệ thống Quét Lỗ hổng & Giám sát An toàn Thông tin

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Security](https://img.shields.io/badge/Security-Scanner-red)

**Sentinel** là đồ án môn học chuyên ngành An toàn thông tin (Information Security), được xây dựng nhằm mục đích cung cấp một công cụ tự động hóa việc phát hiện lỗ hổng Website và phân tích mã độc trong tập tin, tích hợp trí tuệ nhân tạo để tư vấn bảo mật.

---

##  Tính năng nổi bật

### 1.  Quét lỗ hổng Website (URL Scanner)
* Phân tích cấu trúc URL để phát hiện các lỗi bảo mật phổ biến.
* Nhận diện các dấu hiệu **SQL Injection**, **XSS (Cross-site Scripting)**.
* Kiểm tra các Header bảo mật và trạng thái HTTPS.

### 2.  Phân tích Mã độc (File Analysis)
* Hỗ trợ quét nhiều định dạng: `.exe`, `.pdf`, `.docx`, `.zip`, `.rar`.
* Sử dụng **Signature-based detection** để tìm các mẫu virus đã biết.
* Phân tích cấu trúc file PE (Portable Executable) để tìm hành vi đáng ngờ.
* **Deep Scan:** Phát hiện file ẩn đuôi (Extension Spoofing).

### 3.  Trợ lý ảo AI (Sentinel AI Support)
* Tích hợp **Google Gemini Pro**.
* Chatbot hỗ trợ giải đáp thắc mắc về an toàn thông tin 24/7.
* Phân tích log và đưa ra lời khuyên khắc phục lỗ hổng.

### 4.  Nhật ký & Tin tức
* **Lịch sử quét (History):** Tự động lưu lại kết quả quét (URL/File) để tra cứu.
* **Tin tức bảo mật:** Cập nhật các lỗ hổng Zero-day và cảnh báo mới nhất.

---

##  Công nghệ sử dụng

* **Ngôn ngữ:** Python 3
* **Framework:** Flask (Web Server)
* **Giao diện:** HTML5, CSS3, Bootstrap 5, JavaScript
* **AI Engine:** Google Generative AI (Gemini API)
* **Thư viện phân tích:** `pefile`, `python-magic`, `requests`

---

##  Cài đặt và Chạy thử

```bash
git clone [https://github.com/TÊN_GITHUB_CỦA_BẠN/Sentinel_HUIT.git](https://github.com/TÊN_GITHUB_CỦA_BẠN/Sentinel_HUIT.git)
cd Sentinel_HUIT
Sentinel_HUIT/
├── static/              # Chứa CSS, JS, Hình ảnh
├── templates/           # Chứa giao diện (HTML)
│   ├── index.html       # Trang chủ
│   └── history.html     # Trang lịch sử
├── app.py               # Code xử lý chính (Backend)
├── scanner.py           # Module quét lỗ hổng & file
├── scan_history.json    # Database lưu lịch sử (JSON)
└── requirements.txt     # Danh sách thư viện
By Nguyen Chi Cuong
