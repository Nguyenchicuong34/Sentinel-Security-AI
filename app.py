import os
import json
import datetime
from flask import Flask, render_template, request, jsonify
from scanner import SecurityScanner
import google.generativeai as genai

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  

# --- CẤU HÌNH GEMINI API ---
GEMINI_API_KEY = 'AIzaSyC8UUYFxqIbodQkpjE449SiJ-5Y_rkkWNs' 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

scanner = SecurityScanner()

# --- CẤU HÌNH FILE LỊCH SỬ ---
# Đường dẫn file json để lưu lịch sử
HISTORY_FILE = os.path.join(app.root_path, 'scan_history.json')

# --- HÀM HỖ TRỢ: LƯU & ĐỌC LỊCH SỬ ---
def load_history():
    """Đọc dữ liệu từ file json"""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_to_history(scan_type, target, result):
    """Lưu kết quả quét vào file json"""
    history = load_history()
    
    # Xác định trạng thái an toàn dựa trên kết quả trả về
    status = "KHÔNG XÁC ĐỊNH"
    if 'status' in result:
        status = result['status']
    elif 'is_safe' in result:
        status = "AN TOÀN" if result['is_safe'] else "NGUY HIỂM"

    # Lấy chi tiết lỗi (nếu có)
    details_list = []
    if 'details' in result: details_list = result['details']
    elif 'warnings' in result: details_list = result['warnings']

    entry = {
        "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "type": scan_type,     # 'URL' hoặc 'FILE'
        "target": target,      # Link hoặc Tên file
        "status": status,      # AN TOÀN / NGUY HIỂM
        "score": result.get('score', 0),
        "details": details_list # Danh sách lỗi cụ thể
    }
    
    # Thêm vào đầu danh sách (Mới nhất lên trên)
    history.insert(0, entry)
    
    # Chỉ giữ lại 100 dòng lịch sử gần nhất để file không quá nặng
    history = history[:100]
    
    # Ghi lại vào file
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# --- DỮ LIỆU TIN TỨC (Đã bổ sung thêm thông tin) ---
news_data = [
    {
        "title": "Lỗ hổng Zero-day trên Windows 11",
        "title_en": "Zero-day vulnerability on Windows 11",
        "desc": "Microsoft cảnh báo lỗ hổng thực thi mã từ xa nghiêm trọng CVE-2026-1234. Hacker có thể chiếm quyền kiểm soát máy tính mà không cần người dùng thao tác.",
        "img": "static/img/news1.jpg", 
        "date": "03/01/2026",
        "severity": "Nghiêm trọng", # Thêm mức độ
        "category": "Hệ điều hành",   # Thêm thể loại
        "source": "Microsoft Security Center" # Thêm nguồn
    },
    {
        "title": "Chiến dịch Phishing qua mã QR",
        "title_en": "QR Code Phishing Campaign",
        "desc": "Cẩn trọng khi quét mã QR lạ tại nơi công cộng, quán cafe. Kẻ gian dán đè mã QR độc hại để đánh cắp thông tin ngân hàng.",
        "img": "static/img/news2.jpg",
        "date": "02/01/2026",
        "severity": "Cảnh báo cao",
        "category": "Lừa đảo trực tuyến",
        "source": "WhiteHat VN"
    },
    {
        "title": "Rò rỉ dữ liệu thẻ tín dụng",
        "title_en": "Credit Card Data Leak",
        "desc": "Hơn 1 triệu thông tin người dùng bị rao bán trên Dark Web bao gồm số thẻ, CVV và địa chỉ. Hãy đổi mật khẩu ngay lập tức.",
        "img": "static/img/news3.jpg",
        "date": "01/01/2026",
        "severity": "Trung bình",
        "category": "Dữ liệu người dùng",
        "source": "CyberNews"
    }
]

# --- ROUTES (ĐƯỜNG DẪN) ---

@app.route('/')
def index():
    return render_template('index.html', news=news_data)

@app.route('/history')
def history_page():
    """Trang xem lại lịch sử quét"""
    data = load_history()
    return render_template('history.html', history=data)

@app.route('/scan_url', methods=['POST'])
def scan_url_endpoint():
    url = request.form.get('url')
    if not url: return jsonify({"error": "Thiếu URL"}), 400
    
    # 1. Thực hiện quét
    result = scanner.scan_url(url)
    
    # 2. Lưu vào lịch sử
    save_to_history("URL", url, result)
    
    return jsonify(result)

@app.route('/scan_file', methods=['POST'])
def scan_file_endpoint():
    if 'file' not in request.files: return jsonify({"error": "Thiếu file"}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({"error": "Chưa chọn file"}), 400
    
    # 1. Thực hiện quét
    result = scanner.scan_file_deep(file.stream, file.filename)
    
    # 2. Lưu vào lịch sử
    save_to_history("FILE", file.filename, result)
    
    return jsonify(result)

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    user_msg = request.json.get('message')
    if not user_msg: return jsonify({"response": "Vui lòng nhập câu hỏi."})
    
    try:
        prompt = f"Bạn là Sentinel AI - Chuyên gia an toàn thông tin của HUIT. Hãy trả lời ngắn gọn, chuyên nghiệp về vấn đề bảo mật này: {user_msg}"
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "Hệ thống AI đang bảo trì. Vui lòng thử lại sau."})

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5001, debug=False)