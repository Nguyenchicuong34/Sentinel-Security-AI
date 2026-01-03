import re
import hashlib
import magic
import zipfile
import os

class SecurityScanner:
    def __init__(self):
        
        self.sql_patterns = [r"union.*select", r"select.*from", r"drop.*table", r"update.*set", r"insert.*into", r"'", r'"', r"--", r"\/\*", r"\*\/"]
        self.xss_patterns = [r"<script>", r"javascript:", r"onload", r"onerror", r"alert\(", r"document\.cookie", r"eval\("]
        self.cmd_patterns = [r";.*ls", r"\|.*cat", r"&&.*dir", r"ping.*-c", r"nc.*-e"]

    def scan_url(self, url):
        results = []
        risk_score = 0
        
        # Kiểm tra SQLi, XSS, Cmd Injection
        for p in self.sql_patterns:
            if re.search(p, url, re.IGNORECASE):
                results.append(f"Nguy hiểm: Dấu hiệu SQL Injection ({p})")
                risk_score += 20
        for p in self.xss_patterns:
            if re.search(p, url, re.IGNORECASE):
                results.append(f"Nguy hiểm: Mã độc XSS ({p})")
                risk_score += 25
        for p in self.cmd_patterns:
            if re.search(p, url, re.IGNORECASE):
                results.append(f"Cực nguy hiểm: Command Injection ({p})")
                risk_score += 50

        if not url.startswith("https://"):
            results.append("Cảnh báo: HTTP không an toàn (Dễ bị Sniffing)")
            risk_score += 10

        status = "AN TOÀN"
        if risk_score >= 50: status = "NGUY HIỂM CAO"
        elif risk_score > 0: status = "CÓ CẢNH BÁO"

        return {"status": status, "details": results, "score": risk_score}

    def scan_file_deep(self, file_stream, filename):
        file_stream.seek(0)
        content = file_stream.read()
        file_size = len(content)
        file_hash = hashlib.sha256(content).hexdigest()
        
        try:
            mime_type = magic.from_buffer(content, mime=True)
        except:
            mime_type = "unknown"

        warnings = []
        is_safe = True
        info = [f"Kích thước: {file_size / 1024:.2f} KB", f"MIME Type: {mime_type}"]

        # 1. Xử lý file nén ZIP 
        if zipfile.is_zipfile(file_stream):
            info.append("Loại file: Archive (ZIP/Compressed)")
            try:
                with zipfile.ZipFile(file_stream) as zf:
                    file_list = zf.namelist()
                    info.append(f"Nội dung file nén: {', '.join(file_list[:5])}...")
                    
                    # Tìm file thực thi ẩn trong zip
                    for name in file_list:
                        if name.lower().endswith(('.exe', '.sh', '.bat', '.vbs', '.cmd')):
                            warnings.append(f"NGUY HIỂM: Phát hiện file thực thi '{name}' ẩn trong file nén.")
                            is_safe = False
            except Exception as e:
                warnings.append("Lỗi: File nén bị hỏng hoặc có mật khẩu (Password Protected).")
        
        # 2. Xử lý RAR 
        elif content.startswith(b'Rar!'):
            info.append("Loại file: WinRAR Archive")
            warnings.append("Lưu ý: Hệ thống phát hiện file RAR. Cần giải nén để quét sâu hơn.")
        
        # 3. Check Spoofing 
        valid_imgs = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if filename.lower().endswith(('.jpg', '.png')) and mime_type not in valid_imgs:
            warnings.append(f"CẢNH BÁO GIẢ MẠO: Tên file là ảnh nhưng ruột là '{mime_type}'.")
            is_safe = False

        # 4. Quét chữ ký mã độc 
        dangerous_sigs = {
            b'<?php': 'Webshell PHP',
            b'eval(': 'JavaScript Eval Code',
            b'cmd.exe': 'Windows Command Shell',
            b'/bin/sh': 'Linux Shell',
            b'powershell': 'PowerShell Script'
        }
        for sig, name in dangerous_sigs.items():
            if sig in content:
                warnings.append(f"NGUY HIỂM: Phát hiện mã lệnh '{name}' trong file.")
                is_safe = False

        return {
            "filename": filename,
            "hash": file_hash,
            "is_safe": is_safe,
            "warnings": warnings if warnings else ["File sạch. Không phát hiện bất thường."],
            "info": info
        }