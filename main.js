// --- 1. CHATBOT AI 
function toggleChat() {
    const body = document.getElementById('chatBody');
    const input = document.querySelector('.chat-input');
    const icon = document.getElementById('chatIcon');

    if (body.style.display === 'none' || body.style.display === '') {
        body.style.display = 'block';
        input.style.display = 'flex';
        icon.className = 'fa-solid fa-chevron-down';
    } else {
        body.style.display = 'none';
        input.style.display = 'none';
        icon.className = 'fa-solid fa-chevron-up';
    }
}

function sendChat() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;

    const chatBody = document.getElementById('chatBody');
    chatBody.innerHTML += `<div class="user-msg text-end mb-2"><span class="bg-light p-2 rounded d-inline-block">${msg}</span></div>`;
    input.value = '';

    
    chatBody.scrollTop = chatBody.scrollHeight;

    
    const loadingId = 'ai-loading-' + Date.now();
    chatBody.innerHTML += `<div class="ai-msg mb-2" id="${loadingId}"><i class="fas fa-spinner fa-spin"></i> Đang suy nghĩ...</div>`;

    fetch('/ask_ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    })
        .then(r => r.json())
        .then(data => {
            document.getElementById(loadingId).remove();
            chatBody.innerHTML += `<div class="ai-msg mb-2"><span class="bg-info text-white p-2 rounded d-inline-block">${data.response}</span></div>`;
            chatBody.scrollTop = chatBody.scrollHeight;
        });
}

// --- 2. QUÉT URL
function scanURL() {
    const url = document.getElementById('urlInput').value;
    const resArea = document.getElementById('resultArea');

    resArea.classList.remove('d-none');
    document.getElementById('resHeader').className = 'card-header bg-info text-white fw-bold';
    document.getElementById('resTitle').innerText = "Đang phân tích...";
    document.getElementById('resInfo').innerHTML = "";
    document.getElementById('resList').innerHTML = "";

    const formData = new FormData();
    formData.append('url', url);

    fetch('/scan_url', { method: 'POST', body: formData })
        .then(r => r.json())
        .then(data => {
            let color = data.score > 0 ? "bg-danger" : "bg-success";
            document.getElementById('resHeader').className = `card-header ${color} text-white fw-bold`;
            document.getElementById('resTitle').innerText = `KẾT QUẢ: ${data.status} (Score: ${data.score})`;

            let html = "";
            if (data.details.length === 0) html = `<li class="list-group-item text-success"><i class="fa-solid fa-check-circle"></i> URL an toàn.</li>`;
            data.details.forEach(msg => html += `<li class="list-group-item text-danger"><i class="fa-solid fa-bug"></i> ${msg}</li>`);
            document.getElementById('resList').innerHTML = html;
        });
}

// --- 3. QUÉT FILE 
function scanFile() {
    const file = document.getElementById('fileInput').files[0];
    if (!file) return;

    const resArea = document.getElementById('resultArea');
    resArea.classList.remove('d-none');
    document.getElementById('resHeader').className = 'card-header bg-primary text-white fw-bold';
    document.getElementById('resTitle').innerText = "Đang tải lên & Giải phẫu file...";

    const formData = new FormData();
    formData.append('file', file);

    fetch('/scan_file', { method: 'POST', body: formData })
        .then(r => r.json())
        .then(data => {
            let color = data.is_safe ? "bg-success" : "bg-danger";
            document.getElementById('resHeader').className = `card-header ${color} text-white fw-bold`;
            document.getElementById('resTitle').innerText = data.is_safe ? "FILE AN TOÀN" : "PHÁT HIỆN MÃ ĐỘC";

            
            let infoHtml = "<strong>Thông tin chi tiết:</strong><br>";
            data.info.forEach(line => infoHtml += `- ${line}<br>`);
            infoHtml += `<small class="text-muted">SHA256: ${data.hash}</small>`;
            document.getElementById('resInfo').innerHTML = infoHtml;

            let html = "";
            data.warnings.forEach(w => {
                let icon = data.is_safe ? "fa-check" : "fa-triangle-exclamation";
                let txtColor = data.is_safe ? "text-success" : "text-danger fw-bold";
                html += `<li class="list-group-item ${txtColor}"><i class="fa-solid ${icon}"></i> ${w}</li>`;
            });
            document.getElementById('resList').innerHTML = html;
        });
}