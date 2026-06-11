# Hướng dẫn chạy demo (Backend + Frontend)

Demo gồm 2 phần chạy **song song** trong 2 cửa sổ terminal riêng:

- **Backend** (FastAPI + model Naive Bayes) — cổng `8000`
- **Frontend** (React + Vite) — cổng `5173`

---

## Cách nhanh nhất (Windows)

Nhấp đúp lần lượt 2 file ở thư mục gốc dự án:

1. `run_backend.bat`  → đợi đến khi thấy dòng `Backend dang chay: http://127.0.0.1:8000`
2. `run_frontend.bat` → mở trình duyệt vào địa chỉ nó in ra (mặc định http://localhost:5173)

Để dừng: nhấn `Ctrl + C` trong mỗi cửa sổ.

---

## Cách thủ công (gõ lệnh)

### 1. Backend

```powershell
cd backend
# Dùng Python có đủ thư viện (anaconda). Lần đầu, nếu thiếu thư viện thì cài:
& "C:\Users\ADMIN\anaconda3\python.exe" -m pip install -r requirements.txt
# Chạy server:
& "C:\Users\ADMIN\anaconda3\python.exe" main.py
```

Kiểm tra: mở http://127.0.0.1:8000 phải thấy `{"status":"ok",...}`.

> Lưu ý: lệnh `python` mặc định trên máy có thể trỏ tới bản Python khác **không có** scikit-learn/FastAPI. Hãy dùng đúng đường dẫn anaconda như trên.

### 2. Frontend

```powershell
cd frontend
npm install   # chỉ cần lần đầu
npm run dev
```

Mở địa chỉ Vite in ra (mặc định http://localhost:5173).

---

## Thử nhanh

Trong giao diện chat, nhập ví dụ:

> đau bụng, buồn nôn, nôn, tiêu chảy

Kết quả mong đợi: chẩn đoán **Ngộ độc thực phẩm** (tên bệnh tiếng Việt, không còn mã/`%`).

---

## Cấu trúc liên quan

| Thành phần | Vị trí |
|---|---|
| Model đang dùng | `backend/model/naive_bayes_health_model.pkl` |
| Bảng trọng số triệu chứng | `backend/model/symptom_weights.csv` |
| Bóc tách triệu chứng (NLP) | `backend/services/transform_input.py` |
| Dự đoán bệnh | `backend/services/chatbot_engine.py` |
| API | `backend/main.py` (`POST /api/chat`) |
| Địa chỉ API frontend gọi | `frontend/src/services/chatService.js` |

Muốn đổi địa chỉ API của frontend: tạo file `frontend/.env` với dòng
`VITE_API_BASE_URL=http://127.0.0.1:8000`
