"""
main.py
-------
API backend cho chatbot chẩn đoán bệnh (FastAPI).
Chạy:  python main.py   ->  mở http://127.0.0.1:8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from services.transform_input import tim_trieu_chung, tao_vector
from services.chatbot_engine import du_doan

app = FastAPI()

# Cho phép frontend (chạy ở cổng khác) gọi được API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend chẩn đoán bệnh đang chạy"}


@app.post("/api/chat")
def chat(payload: dict):
    cau_mo_ta = payload.get("message", "")

    # Bước 1: tìm triệu chứng trong câu người dùng nhập
    trieu_chung = tim_trieu_chung(cau_mo_ta)

    # Bước 2: nếu không tìm thấy triệu chứng nào thì hỏi lại
    if not trieu_chung:
        return {
            "reply": "Mình chưa nhận ra triệu chứng nào. Bạn mô tả rõ hơn nhé "
                     "(ví dụ: sốt, ho, đau đầu, mệt mỏi...).",
            "trieu_chung": [],
        }

    # Bước 2b: cần tối thiểu 3 triệu chứng thì dự đoán mới đáng tin.
    # Ít hơn -> hỏi thêm thay vì đoán bừa (model rất kém khi quá ít triệu chứng).
    SO_TRIEU_CHUNG_TOI_THIEU = 3
    if len(trieu_chung) < SO_TRIEU_CHUNG_TOI_THIEU:
        con_thieu = SO_TRIEU_CHUNG_TOI_THIEU - len(trieu_chung)
        return {
            "reply": (
                f"Mình mới nhận ra {len(trieu_chung)} triệu chứng: "
                f"**{', '.join(trieu_chung)}**.\n\n"
                f"Để dự đoán chính xác, mình cần ít nhất {SO_TRIEU_CHUNG_TOI_THIEU} "
                f"triệu chứng. Bạn mô tả thêm {con_thieu} triệu chứng nữa nhé "
                f"(ví dụ: sốt, ho, đau đầu, mệt mỏi, đau họng, buồn nôn...)."
            ),
            "trieu_chung": trieu_chung,
        }

    # Bước 3: đổi triệu chứng thành vector số rồi đưa vào model dự đoán
    vector = tao_vector(trieu_chung)
    benh = du_doan(vector)

    # Bước 4: tạo câu trả lời gửi về frontend
    reply = (
        f"Dựa trên {len(trieu_chung)} triệu chứng bạn mô tả, "
        f"bạn có thể đang mắc: **{benh}**.\n\n"
        f"Lưu ý: đây chỉ là dự đoán của AI, hãy đi khám bác sĩ để chắc chắn."
    )

    return {
        "reply": reply,
        "benh": benh,
        "trieu_chung": trieu_chung,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
