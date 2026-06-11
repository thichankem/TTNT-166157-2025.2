# -*- coding: utf-8 -*-
"""Sinh cac notebook .ipynb don gian, de hieu cho nguoi moi hoc ML."""
import json, os, uuid

BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE, "02_tien_xu_ly"), exist_ok=True)
os.makedirs(os.path.join(BASE, "03_huan_luyen"), exist_ok=True)

def md(t):  return {"cell_type":"markdown","id":uuid.uuid4().hex[:8],"metadata":{},"source":t.splitlines(keepends=True)}
def code(t):return {"cell_type":"code","id":uuid.uuid4().hex[:8],"metadata":{},"execution_count":None,"outputs":[],"source":t.splitlines(keepends=True)}
def save(path, cells):
    nb={"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
        "language_info":{"name":"python","version":"3.11"}},"nbformat":4,"nbformat_minor":5}
    with open(path,"w",encoding="utf-8") as f: json.dump(nb,f,ensure_ascii=False,indent=1)
    print("wrote", os.path.basename(path))


# ===================== FILE 1: TIEN XU LY DATA =====================
c=[]
c.append(md(
"""# Tiền xử lý dữ liệu bệnh & triệu chứng

Notebook này **chỉ xử lý 2 file dữ liệu** trong thư mục `01_data`:
- `benh_trieuchung.csv` — mỗi dòng là một ca bệnh với các triệu chứng.
- `trongso_mucdo_nghiemtrong.csv` — trọng số (mức độ nặng) của từng triệu chứng.

**Mục tiêu:** biến dữ liệu chữ thành **bảng số** để máy học được, rồi lưu ra `features.csv`.

> Việc xử lý câu mô tả của bệnh nhân (NLP) nằm ở notebook riêng: `xu_ly_input_nlp.ipynb`.
"""))
c.append(md("## Bước 1. Đọc 2 file dữ liệu"))
c.append(code(
"""import pandas as pd

benh = pd.read_csv("../01_data/benh_trieuchung.csv")
print("Số ca bệnh:", len(benh), "| Số bệnh khác nhau:", benh["Benh"].nunique())
benh.head()
"""))
c.append(code(
"""trongso = pd.read_csv("../01_data/trongso_mucdo_nghiemtrong.csv")
print("Số triệu chứng có trọng số:", len(trongso))
trongso.head()
"""))
c.append(md("## Bước 2. Tạo \"từ điển\" trọng số\n\nĐổi bảng trọng số thành `dict` để tra cứu nhanh: tên triệu chứng → mức độ nặng."))
c.append(code(
"""trong_so = dict(zip(trongso["TrieuChung"], trongso["TrongSo"]))
ds_trieuchung = list(trongso["TrieuChung"])   # danh sách triệu chứng (thứ tự cột)
print("Ví dụ:", {k: trong_so[k] for k in ds_trieuchung[:5]})
"""))
c.append(md(
"""## Bước 3. Mã hóa one-hot có trọng số

Mỗi **triệu chứng là một cột**. Với mỗi ca bệnh:
- Nếu **có** triệu chứng đó → điền **trọng số** của nó.
- Nếu **không có** → điền 0.

Cột `Benh` là nhãn cần dự đoán.
"""))
c.append(code(
"""cot_trieuchung = [c for c in benh.columns if c.startswith("TrieuChung")]

X = pd.DataFrame(0, index=benh.index, columns=ds_trieuchung)
for i in range(len(benh)):
    for cot in cot_trieuchung:
        tc = benh.loc[i, cot]
        if isinstance(tc, str) and tc.strip() in trong_so:
            X.loc[i, tc.strip()] = trong_so[tc.strip()]

X["Benh"] = benh["Benh"]
print("Bảng đặc trưng:", X.shape)
X.head()
"""))
c.append(md("## Bước 4. Lưu kết quả ra file"))
c.append(code(
"""import os
os.makedirs("../01_data/processed", exist_ok=True)
X.to_csv("../01_data/processed/features.csv", index=False, encoding="utf-8-sig")
print("Đã lưu: 01_data/processed/features.csv")
"""))
save(os.path.join(BASE,"02_tien_xu_ly","tien_xu_ly_data.ipynb"), c)


# ===================== FILE 2: XU LY INPUT NLP =====================
c=[]
c.append(md(
"""# Xử lý câu mô tả của bệnh nhân (NLP)

Notebook **riêng** này nhận câu mô tả tiếng Việt tự do của bệnh nhân
(`input_mota_benhnhan.csv`) và **tách từ → nhận ra các triệu chứng**,
sau đó chuyển thành vector số giống dữ liệu huấn luyện.
"""))
c.append(md("## Bước 1. Đọc dữ liệu input và danh sách triệu chứng"))
c.append(code(
"""import pandas as pd

inp = pd.read_csv("../01_data/input_mota_benhnhan.csv")
trongso = pd.read_csv("../01_data/trongso_mucdo_nghiemtrong.csv")
trong_so = dict(zip(trongso["TrieuChung"], trongso["TrongSo"]))
ds_trieuchung = list(trongso["TrieuChung"])
inp
"""))
c.append(md(
"""## Bước 2. Tách từ (tokenize)

Nếu máy có cài `underthesea` (thư viện NLP tiếng Việt) thì tách chuẩn hơn;
nếu không có thì tách đơn giản theo khoảng trắng.
"""))
c.append(code(
"""import re

def chuan_hoa(text):
    text = str(text).lower()
    text = re.sub(r"[.,;!?()]", " ", text)
    text = re.sub(r"\\s+", " ", text).strip()
    return text

try:
    from underthesea import word_tokenize
    def tach_tu(text):
        return word_tokenize(chuan_hoa(text))
    print("Dùng underthesea để tách từ.")
except Exception:
    def tach_tu(text):
        return chuan_hoa(text).split()
    print("Không có underthesea -> tách theo khoảng trắng.")

inp["tu"] = inp["mo_ta"].apply(tach_tu)
inp[["mo_ta", "tu"]]
"""))
c.append(md(
"""## Bước 3. Nhận diện triệu chứng trong câu

Tên triệu chứng là **cụm tiếng Việt** (ví dụ `"sốt cao"`, `"ho có đờm"`), nên ta
tìm trực tiếp cụm đó trong câu. Thêm vài **từ đồng nghĩa** để bắt cách diễn đạt
khác. Ưu tiên khớp cụm **dài trước** (để "sốt cao" được nhận trước "sốt").
"""))
c.append(code(
"""dong_nghia = {
    "tức ngực": "đau ngực",
    "đau tức ngực": "đau ngực",
    "sợ ánh sáng": "nhạy cảm ánh sáng",
    "đau mỏi cơ": "đau nhức cơ",
}

def tim_trieu_chung(text):
    norm = chuan_hoa(text)
    tim_thay = []
    ung_vien = list(ds_trieuchung) + list(dong_nghia.keys())
    for cum in sorted(ung_vien, key=len, reverse=True):
        if cum in norm:
            chuan = dong_nghia.get(cum, cum)
            if chuan not in tim_thay:
                tim_thay.append(chuan)
            norm = norm.replace(cum, " ")
    return tim_thay

inp["trieu_chung"] = inp["mo_ta"].apply(tim_trieu_chung)
inp[["mo_ta", "trieu_chung"]]
"""))
c.append(md(
"""## Bước 4. Chuyển thành vector số (one-hot có trọng số) và lưu

Vector có **cùng thứ tự cột** với dữ liệu huấn luyện nên đưa thẳng vào mô hình đã train được.
"""))
c.append(code(
"""def thanh_vector(trieu_chung):
    vec = {tc: 0 for tc in ds_trieuchung}
    for tc in trieu_chung:
        if tc in vec:
            vec[tc] = trong_so[tc]
    return vec

vec_df = pd.DataFrame([thanh_vector(t) for t in inp["trieu_chung"]])
vec_df.insert(0, "mo_ta", inp["mo_ta"])

import os
os.makedirs("../01_data/processed", exist_ok=True)
vec_df.to_csv("../01_data/processed/input_vectorized.csv", index=False, encoding="utf-8-sig")
print("Đã lưu: 01_data/processed/input_vectorized.csv")
vec_df.head()
"""))
save(os.path.join(BASE,"02_tien_xu_ly","xu_ly_input_nlp.ipynb"), c)


# ===================== 3 FILE HUAN LUYEN =====================
LOAD = """import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Đọc dữ liệu đã tiền xử lý (chạy notebook tien_xu_ly_data.ipynb trước)
data = pd.read_csv("../01_data/processed/features.csv")

X = data.drop(columns=["Benh"])     # các cột triệu chứng
y = data["Benh"]                    # nhãn bệnh (dạng chữ)

le = LabelEncoder()
y_num = le.fit_transform(y)         # đổi nhãn chữ -> số

X_train, X_test, y_train, y_test = train_test_split(
    X, y_num, test_size=0.2, random_state=42, stratify=y_num)
print("Train:", X_train.shape, "| Test:", X_test.shape, "| Số bệnh:", len(le.classes_))
"""

def train_nb(fname, tieude, gioithieu, imp, tao_model, tenmodel,
             vc_param, vc_range, vc_xlabel, vc_xlog, vc_estimator, pkl):
    c=[]
    c.append(md(f"# {tieude}\n\n{gioithieu}\n\n> Nhớ chạy `02_tien_xu_ly/tien_xu_ly_data.ipynb` trước để có `features.csv`."))
    c.append(md("## Bước 1. Đọc dữ liệu đã tiền xử lý"))
    c.append(code(imp+"\n"+LOAD))
    c.append(md("## Bước 2. Huấn luyện và đánh giá"))
    c.append(code(f"""from sklearn.metrics import accuracy_score

{tao_model}
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Độ chính xác trên tập test:", round(accuracy_score(y_test, y_pred), 3))
"""))
    c.append(md(
f"""## Bước 3. Đường cong học tập theo tham số

Thử nhiều giá trị của **`{vc_param}`** để xem mô hình tốt nhất ở đâu.
- Đường **Train** cao mà **Kiểm tra (CV)** thấp ⇒ **quá khớp** (overfitting).
- Cả hai cùng thấp ⇒ **chưa khớp** (underfitting).
"""))
    c.append(code(f"""import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import validation_curve

gia_tri = {vc_range}
train_sc, val_sc = validation_curve(
    {vc_estimator}, X_train, y_train,
    param_name="{vc_param}", param_range=gia_tri,
    cv=3, scoring="accuracy")

plt.figure(figsize=(7,5))
plt.plot(gia_tri, train_sc.mean(axis=1), "o-", label="Train")
plt.plot(gia_tri, val_sc.mean(axis=1), "o-", label="Kiểm tra (CV)")
{'plt.xscale("log")' if vc_xlog else ''}
plt.xlabel("{vc_xlabel}"); plt.ylabel("Độ chính xác")
plt.title("Đường cong theo tham số - {tenmodel}")
plt.legend(); plt.grid(True, alpha=0.3); plt.show()

tot_nhat = gia_tri[int(np.argmax(val_sc.mean(axis=1)))]
print("Giá trị {vc_param} tốt nhất:", tot_nhat)
"""))
    c.append(md("## Bước 4. Đường cong học tập theo số lượng mẫu\n\nXem mô hình có học tốt hơn khi có **nhiều dữ liệu** hơn không."))
    c.append(code(f"""from sklearn.model_selection import learning_curve

sizes, train_sc2, val_sc2 = learning_curve(
    model, X, y_num, cv=3, scoring="accuracy",
    train_sizes=np.linspace(0.1, 1.0, 6))

plt.figure(figsize=(7,5))
plt.plot(sizes, train_sc2.mean(axis=1), "o-", label="Train")
plt.plot(sizes, val_sc2.mean(axis=1), "o-", label="Kiểm tra (CV)")
plt.xlabel("Số mẫu huấn luyện"); plt.ylabel("Độ chính xác")
plt.title("Đường cong theo số mẫu - {tenmodel}")
plt.legend(); plt.grid(True, alpha=0.3); plt.show()
"""))
    c.append(md("## Bước 5. Lưu mô hình"))
    c.append(code(f"""import pickle
with open("{pkl}", "wb") as f:
    pickle.dump({{"model": model, "label_encoder": le}}, f)
print("Đã lưu {pkl}")
"""))
    save(os.path.join(BASE,"03_huan_luyen",fname), c)


train_nb(
    "01_random_forest.ipynb", "Huấn luyện Random Forest",
    "**Random Forest** = nhiều cây quyết định bỏ phiếu chung. Mạnh và ít phải chỉnh.",
    "from sklearn.ensemble import RandomForestClassifier",
    "model = RandomForestClassifier(n_estimators=100, random_state=42)",
    "Random Forest",
    "n_estimators", "[10, 25, 50, 100, 150, 200]", "Số cây (n_estimators)", False,
    "RandomForestClassifier(random_state=42)", "random_forest_model.pkl",
)
train_nb(
    "02_knn.ipynb", "Huấn luyện KNN (K láng giềng gần nhất)",
    "**KNN** dự đoán dựa trên k ca bệnh giống nhất trong dữ liệu.",
    "from sklearn.neighbors import KNeighborsClassifier",
    "model = KNeighborsClassifier(n_neighbors=5)",
    "KNN",
    "n_neighbors", "[1, 3, 5, 7, 9, 11, 15, 21]", "Số láng giềng (k)", False,
    "KNeighborsClassifier()", "knn_model.pkl",
)
train_nb(
    "03_naive_bayes.ipynb", "Huấn luyện Naive Bayes",
    "**Naive Bayes** dựa trên xác suất (định lý Bayes), chạy rất nhanh.",
    "from sklearn.naive_bayes import GaussianNB",
    "model = GaussianNB()",
    "Naive Bayes",
    "var_smoothing", "list(np.logspace(-9, 0, 10))", "var_smoothing (thang log)", True,
    "GaussianNB()", "naive_bayes_model.pkl",
)
print("XONG")
