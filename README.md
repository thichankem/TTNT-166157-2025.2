# AI Medical Chatbot - Chẩn đoán bệnh từ triệu chứng

Hệ thống chatbot y tế sử dụng **Random Forest** để chẩn đoán bệnh dựa trên mô tả triệu chứng bằng tiếng Việt của bệnh nhân.

---

## 1. Tổng quan kiến trúc

```
┌──────────────────┐    HTTP/JSON    ┌─────────────────────────────────┐
│   Frontend       │ ──────────────► │   Backend (FastAPI)              │
│   React + Vite   │                 │                                  │
│   localhost:5173 │ ◄────────────── │   localhost:8000                 │
└──────────────────┘                 │                                  │
                                     │   ┌──────────────────────────┐   │
                                     │   │ Model 1: NLP Extractor   │   │
                                     │   │ text → [triệu chứng]     │   │
                                     │   └────────────┬─────────────┘   │
                                     │                ▼                  │
                                     │   ┌──────────────────────────┐   │
                                     │   │ Hot-Encoding             │   │
                                     │   │ [triệu chứng] → vector   │   │
                                     │   └────────────┬─────────────┘   │
                                     │                ▼                  │
                                     │   ┌──────────────────────────┐   │
                                     │   │ Model 2: Random Forest   │   │
                                     │   │ vector → bệnh + xác suất │   │
                                     │   └──────────────────────────┘   │
                                     └─────────────────────────────────┘
```

**Luồng xử lý:** Bệnh nhân nhập đoạn văn mô tả triệu chứng → Model 1 trích xuất các từ vựng triệu chứng → Hot-encoding thành vector nhị phân → Model 2 (Random Forest) dự đoán bệnh.

---

## 2. Dữ liệu (Dataset)

Dữ liệu được tự sinh dựa trên cơ sở tri thức y khoa lưu trong [`backend/data/diseases_symptoms.py`](backend/data/diseases_symptoms.py).

### 2.1 Thống kê

| Chỉ số | Giá trị |
|--------|---------|
| Số bệnh | **100 bệnh** phổ biến |
| Số triệu chứng | **268 triệu chứng** (~300) |
| Số mẫu training | **12,000** (120 mẫu/bệnh) |
| Mã hóa | **Hot-encoding** (one-hot vector nhị phân) |

### 2.2 Cấu trúc dữ liệu

File `diseases_symptoms.py` chứa 3 cấu trúc chính:

**a) `SYMPTOMS_LIST`** - Danh sách 268 mã triệu chứng (cố định thứ tự cột feature):
```python
SYMPTOMS_LIST = [
    "fever", "high_fever", "headache", "cough", "chest_pain",
    "joint_pain", "vomiting", "diarrhea", ...
]
```

**b) `SYMPTOM_KEYWORDS`** - Từ điển ánh xạ mã triệu chứng → các từ khóa tiếng Việt mà người dùng có thể dùng để mô tả triệu chứng đó:
```python
SYMPTOM_KEYWORDS = {
    "fever":    ["sốt", "bị sốt", "nóng người", "thân nhiệt tăng", "fever"],
    "headache": ["đau đầu", "nhức đầu", "đầu nhức", "đầu đau", "headache"],
    "cough":    ["ho", "bị ho", "ho nhiều", "húng hắng ho", "cough"],
    ...
}
```
Dùng cho **Model 1 (NLP Extractor)** để nhận diện triệu chứng từ câu nói tự nhiên.

**c) `DISEASES`** - 100 bệnh, mỗi bệnh có tên tiếng Việt + tiếng Anh + danh sách triệu chứng đặc trưng:
```python
DISEASES = {
    "influenza": {
        "name_vi": "Cúm (Influenza)",
        "name_en": "Influenza / Flu",
        "symptoms": ["fever", "high_fever", "chills", "fatigue",
                     "body_aches", "headache", "dry_cough",
                     "sore_throat", ...],
    },
    "dengue_fever": {
        "name_vi": "Sốt xuất huyết Dengue",
        "name_en": "Dengue Fever",
        "symptoms": ["high_fever", "severe_headache", "body_aches",
                     "rash", "eye_pain", "petechiae", ...],
    },
    ...
}
```

### 2.3 Sinh dữ liệu training (synthetic data)

Script [`train_model.py`](backend/train_model.py) sinh dữ liệu training:
- Với mỗi bệnh, sinh **120 mẫu bệnh nhân** giả định.
- Mỗi mẫu chứa **55–95%** triệu chứng đặc trưng của bệnh (lựa chọn ngẫu nhiên) để mô phỏng việc bệnh nhân không phải lúc nào cũng có đủ tất cả triệu chứng.
- Thêm nhiễu (**noise**): với xác suất 5%, một triệu chứng không liên quan có thể được "bật" để mô phỏng triệu chứng đi kèm.
- Mỗi mẫu là một vector hot-encoded: `[0, 1, 0, 0, 1, 1, 0, ...]` có độ dài 268.

### 2.4 Danh mục 100 bệnh

| Nhóm | Số lượng | Ví dụ |
|------|----------|-------|
| Nhiễm trùng | 20 | Cúm, COVID-19, Viêm phổi, Sốt xuất huyết, HIV |
| Tim mạch | 10 | Tăng huyết áp, Nhồi máu cơ tim, Đột quỵ, Suy tim |
| Hô hấp | 7 | Hen suyễn, COPD, Ung thư phổi, Viêm màng phổi |
| Nội tiết & Chuyển hóa | 8 | Tiểu đường 1/2, Suy/Cường giáp, Gút, Béo phì |
| Tiêu hóa | 12 | Viêm dạ dày, Viêm ruột thừa, GERD, Xơ gan |
| Thần kinh | 10 | Migraine, Động kinh, Alzheimer, Parkinson, MS |
| Tâm thần | 5 | Trầm cảm, Lo âu, Mất ngủ, Lưỡng cực |
| Cơ xương khớp | 9 | Thoái hóa khớp, Viêm khớp dạng thấp, Loãng xương |
| Thận – Tiết niệu | 5 | Sỏi thận, Nhiễm trùng tiểu, Suy thận mãn |
| Da liễu | 8 | Mụn trứng cá, Vảy nến, Chàm, Mề đay, Ghẻ |
| Mắt – Tai mũi họng | 6 | Glaucoma, Đục thủy tinh thể, Viêm xoang, Viêm amidan |

---

## 3. Cấu trúc thư mục Backend

```
backend/
├── data/
│   ├── __init__.py
│   └── diseases_symptoms.py        ← Cơ sở tri thức (100 bệnh, 268 triệu chứng, từ khóa tiếng Việt)
│
├── services/
│   ├── __init__.py
│   ├── transform_input.py          ← Model 1: NLP keyword extractor + hot-encoding
│   └── chatbot_engine.py           ← Model 2: Random Forest predictor
│
├── model/
│   └── random_forest_health_model.pkl   ← Model đã train (~371 MB)
│
├── main.py                         ← FastAPI server, endpoint POST /api/chat
├── train_model.py                  ← Script training Random Forest
└── requirements.txt                ← Python dependencies
```

### Mô tả từng file

| File | Chức năng |
|------|-----------|
| `data/diseases_symptoms.py` | Knowledge base: `SYMPTOMS_LIST`, `SYMPTOM_KEYWORDS`, `DISEASES` |
| `services/transform_input.py` | `process_clinical_text(text)`: text → list mã triệu chứng. `convert_to_matrix(symptoms)`: list → vector hot-encoded (1×268) |
| `services/chatbot_engine.py` | `predict_from_vector(vector)`: vector → `{prediction, confidence, top_3, ...}` |
| `main.py` | FastAPI app, CORS cho `localhost:5173`, endpoint `POST /api/chat` |
| `train_model.py` | Sinh dữ liệu giả định → train RF (n_estimators=200, max_depth=20) → lưu pickle |

---

## 4. Cài đặt & chạy hệ thống

### 4.1 Cài đặt Backend

**Yêu cầu:** Python 3.11+ và pip.

```powershell
cd backend
pip install -r requirements.txt
```

`requirements.txt`:
```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
scikit-learn>=1.4.0
numpy>=1.26.0
pandas>=2.2.0
```

### 4.2 Training Model (chỉ chạy 1 lần hoặc khi đổi dữ liệu)

```powershell
cd backend
python train_model.py
```

Output mong đợi:
```
============================================================
Disease Diagnosis - Random Forest Training
============================================================
  Diseases  : 100
  Symptoms  : 268
  Samples   : 12000
[1/4] Generating synthetic training data ...
[2/4] Encoding labels ...
[3/4] Training Random Forest ...
       Test accuracy : 89.78%
       Macro-avg F1 / Precision / Recall:
         Precision 0.902 | Recall 0.898 | F1 0.896
[4/4] Saving model ...
       Saved -> backend/model/random_forest_health_model.pkl  (371.6 MB)
Training complete!
```

File `backend/model/random_forest_health_model.pkl` được tạo, chứa:
- Model Random Forest đã train
- `LabelEncoder` để decode label → mã bệnh
- `SYMPTOMS_LIST` (thứ tự cột feature)
- Mapping mã bệnh → tên bệnh tiếng Việt

### 4.3 Chạy Backend Server

```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Server chạy tại **`http://localhost:8000`**.

> **Lưu ý Windows:** Nếu `python` mặc định không phải Anaconda, dùng đường dẫn đầy đủ:
> `C:\Users\<user>\anaconda3\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000`

### 4.4 Cài đặt & chạy Frontend

**Yêu cầu:** Node.js 18+ và npm.

```powershell
cd frontend
npm install        # cài dependencies (chỉ lần đầu)
npm run dev        # chạy dev server
```

Frontend mở tại **`http://localhost:5173`**.

---

## 5. Kết nối Backend ↔ Frontend

### 5.1 Cấu hình CORS (Backend)

Trong [`backend/main.py`](backend/main.py), CORS được mở cho địa chỉ Vite dev server:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5.2 Cấu hình API URL (Frontend)

Frontend gọi API qua `axios` trong [`frontend/src/services/chatService.js`](frontend/src/services/chatService.js):

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function sendChatMessage(message) {
  const response = await axios.post(`${API_BASE_URL}/api/chat`, { message });
  return response.data;
}
```

Có thể đổi URL backend bằng biến môi trường (tạo file `frontend/.env`):
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### 5.3 API Endpoint

**`POST /api/chat`**

Request body:
```json
{
  "message": "Tôi bị sốt cao, đau đầu và ho khan 3 ngày nay"
}
```

Response:
```json
{
  "status": "success",
  "reply": "Dựa trên 4 triệu chứng bạn mô tả, tôi chẩn đoán bạn có thể đang mắc: **Cúm (Influenza)**.\n\nLưu ý: Đây chỉ là dự đoán từ AI...",
  "prediction": {
    "prediction": "Cúm (Influenza)",
    "disease_code": "influenza",
    "confidence": 0.064,
    "top_3": [
      {"disease": "Cúm (Influenza)", "code": "influenza", "probability": 0.064},
      {"disease": "COVID-19", "code": "covid_19", "probability": 0.041},
      {"disease": "Viêm phổi", "code": "pneumonia", "probability": 0.032}
    ],
    "total_symptoms_detected": 4
  },
  "detected_symptoms": ["high_fever", "headache", "dry_cough", "fatigue"]
}
```

### 5.4 Sơ đồ luồng request

```
[User gõ text trong ChatBotPage]
    ↓
[chatService.js → axios.post("/api/chat", {message})]
    ↓ HTTP POST
[FastAPI nhận request]
    ↓
[process_clinical_text(message) → ["high_fever","headache",...]]
    ↓
[convert_to_matrix([...]) → numpy array shape (1, 268)]
    ↓
[predict_from_vector(vector) → {prediction, confidence, top_3}]
    ↓
[FastAPI trả JSON]
    ↓
[Frontend hiển thị reply trong khung chat]
```

### 5.5 Chạy đồng thời (2 terminals)

**Terminal 1 - Backend:**
```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000



cd "C:\Users\ADMIN\OneDrive\Máy tính\TTNT-166157-2025.2\backend"
& "C:\Users\ADMIN\anaconda3\python.exe" -m uvicorn main:app --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev



cd "C:\Users\ADMIN\OneDrive\Máy tính\TTNT-166157-2025.2\frontend"
npm run dev
```

Truy cập `http://localhost:5173` → giao diện chatbot sẵn sàng.

---

## 6. Chuyển đổi file `.ipynb` (Jupyter Notebook) sang `.py`

Nếu bạn có file Jupyter Notebook và muốn chuyển sang Python script để tích hợp vào backend, có **3 cách**:

### Cách 1: Dùng `jupyter nbconvert` (khuyến nghị)

```powershell
# Cài jupyter nếu chưa có
pip install jupyter

# Chuyển 1 file
jupyter nbconvert --to script notebook.ipynb

# Chuyển nhiều file cùng lúc
jupyter nbconvert --to script *.ipynb

# Chuyển và đặt tên output
jupyter nbconvert --to script notebook.ipynb --output ten_moi.py
```

Output: `notebook.py` (cùng thư mục).

### Cách 2: Dùng VS Code

1. Mở file `.ipynb` trong VS Code (cần extension **Jupyter**).
2. Click vào icon **"..."** ở góc phải trên của notebook.
3. Chọn **"Export"** → **"Python Script"**.
4. VS Code sẽ tạo file `.py` tương ứng.

### Cách 3: Dùng Python script

```python
import nbformat
from nbconvert import PythonExporter

with open("notebook.ipynb", "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

exporter = PythonExporter()
source, _ = exporter.from_notebook_node(nb)

with open("notebook.py", "w", encoding="utf-8") as f:
    f.write(source)
```

### Lưu ý sau khi chuyển

File `.py` được tạo ra sẽ có các marker `# In[1]:` đánh dấu cell. Bạn cần:

1. **Xóa các marker comment** (`# In[1]:`, `# In[2]:`, ...)
2. **Xóa các lệnh magic của Jupyter** nếu có (`%matplotlib inline`, `!pip install ...`)
3. **Tổ chức lại code thành các hàm** để có thể `import` từ file khác
4. **Đóng gói logic** thành các function với rõ ràng input/output

Ví dụ chuyển một cell training thành function:
```python
# Trước (notebook):
df = pd.read_csv("data.csv")
X = df.drop("label", axis=1)
y = df["label"]
model = RandomForestClassifier()
model.fit(X, y)

# Sau (file .py có thể tái sử dụng):
def train_model(data_path: str):
    df = pd.read_csv(data_path)
    X = df.drop("label", axis=1)
    y = df["label"]
    model = RandomForestClassifier()
    model.fit(X, y)
    return model
```

---

## 7. Test nhanh bằng curl

```powershell
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\":\"toi bi sot cao, ho khan, dau dau va on lanh 3 ngay\"}'
```

---

## 8. Troubleshooting

| Lỗi | Nguyên nhân | Cách sửa |
|-----|-------------|----------|
| `No module named 'uvicorn'` | Sai Python interpreter | Dùng `C:\Users\<user>\anaconda3\python.exe -m uvicorn ...` |
| `Cannot find module 'vite'` | `node_modules` chưa cài | `cd frontend && npm install` |
| `Model file not found` | Chưa train | Chạy `python train_model.py` trước |
| CORS error | Frontend chạy port khác 5173 | Thêm origin mới vào `allow_origins` trong `main.py` |
| Triệu chứng không nhận diện | Người dùng dùng từ ngữ lạ | Bổ sung từ khóa vào `SYMPTOM_KEYWORDS` |

---

## 9. Hiệu năng Model

| Metric | Giá trị |
|--------|---------|
| Test Accuracy | **89.78%** |
| Macro Precision | 0.902 |
| Macro Recall | 0.898 |
| Macro F1-score | 0.896 |
| Số trees | 200 |
| Max depth | 20 |
| Kích thước file model | ~371 MB |

---

## 10. Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Frontend | React 19 + Vite + React Router + Axios |
| Backend | FastAPI + Uvicorn |
| ML | scikit-learn (Random Forest) |
| NLP | Custom keyword matching (Vietnamese-aware) |
| Data | NumPy + Pandas |
