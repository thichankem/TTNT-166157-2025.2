"""
transform_input.py
------------------
Bóc tách triệu chứng từ câu mô tả của người dùng, rồi đổi thành vector số
để đưa vào model dự đoán.
"""

import os
import csv
import re
import unicodedata
import numpy as np

from services.chatbot_engine import FEATURE_NAMES

# 1. Đọc bảng trọng số mức độ nghiêm trọng của triệu chứng (vd: "sốt cao" -> 6)
#    Đây chính là cách dữ liệu được mã hoá lúc huấn luyện model.
_FILE_TRONG_SO = os.path.join(os.path.dirname(__file__), "..", "model", "symptom_weights.csv")
TRONG_SO = {}
with open(_FILE_TRONG_SO, encoding="utf-8-sig") as f:
    for dong in csv.DictReader(f):
        TRONG_SO[dong["TrieuChung"]] = float(dong["TrongSo"])

# 2. Một số cách nói thường gặp -> tên triệu chứng chuẩn của model
TU_DONG_NGHIA = {
    "nhức đầu":       "đau đầu",
    "ngạt mũi":       "nghẹt mũi",
    "chảy nước mũi":  "sổ mũi",
    "buồn ói":        "buồn nôn",
    "ói":             "nôn",
    "đi ngoài":       "tiêu chảy",
    "tức ngực":       "đau ngực",
    "đau dạ dày":     "đau thượng vị",
}


def bo_dau(chuoi):
    """Bỏ dấu tiếng Việt để so khớp dễ hơn (vd: 'sốt' -> 'sot')."""
    chuoi = chuoi.replace("đ", "d").replace("Đ", "D")
    chuoi = unicodedata.normalize("NFD", chuoi)
    return "".join(c for c in chuoi if unicodedata.category(c) != "Mn")


def tim_trieu_chung(cau_mo_ta):
    """Tìm các triệu chứng xuất hiện trong câu người dùng nhập."""
    text = bo_dau(cau_mo_ta.lower())

    # Gộp lại: mỗi triệu chứng tự khớp chính nó, cộng thêm các cách nói khác
    tu_khoa = {tc: tc for tc in FEATURE_NAMES}
    tu_khoa.update(TU_DONG_NGHIA)

    ket_qua = []
    # Khớp cụm dài trước (vd "đau đầu dữ dội" được ưu tiên hơn "đau đầu")
    for cum in sorted(tu_khoa, key=len, reverse=True):
        mau = re.escape(bo_dau(cum.lower()))
        if re.search(rf"\b{mau}\b", text):          # khớp theo từ, tránh nhầm lẫn
            ten_chuan = tu_khoa[cum]
            if ten_chuan not in ket_qua:
                ket_qua.append(ten_chuan)
            text = re.sub(rf"\b{mau}\b", " ", text)  # xoá đi để khỏi khớp lại
    return ket_qua


def tao_vector(trieu_chung):
    """Đổi danh sách triệu chứng thành vector số (theo trọng số) cho model."""
    vector = np.zeros((1, len(FEATURE_NAMES)))
    for i, tc in enumerate(FEATURE_NAMES):
        if tc in trieu_chung:
            vector[0, i] = TRONG_SO.get(tc, 1)   # có triệu chứng -> điền trọng số
    return vector
