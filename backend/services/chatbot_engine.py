"""
chatbot_engine.py
-----------------
Dự đoán bệnh từ vector triệu chứng, dùng model Naive Bayes đã huấn luyện sẵn.
"""

import os
import pickle
import pandas as pd

# 1. Tải model đã huấn luyện (chỉ load 1 lần khi khởi động backend)
_FILE = os.path.join(os.path.dirname(__file__), "..", "model", "naive_bayes_health_model.pkl")
with open(_FILE, "rb") as f:
    goi = pickle.load(f)              # file .pkl chứa: model + bộ mã hoá nhãn

MODEL = goi["model"]                          # bộ phân loại Naive Bayes
NHAN = goi["label_encoder"]                   # dùng để đổi số thứ tự <-> tên bệnh
FEATURE_NAMES = list(MODEL.feature_names_in_)  # 135 triệu chứng (đúng thứ tự lúc train)


def du_doan(vector):
    """Nhận vào vector triệu chứng, trả về tên bệnh có khả năng cao nhất."""
    df = pd.DataFrame(vector, columns=FEATURE_NAMES)
    so_benh = MODEL.predict(df)[0]               # model trả về số thứ tự của bệnh
    return NHAN.inverse_transform([so_benh])[0]  # đổi số đó -> tên bệnh tiếng Việt
