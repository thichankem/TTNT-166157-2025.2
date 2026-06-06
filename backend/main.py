from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from services.transform_input import process_clinical_text, convert_to_matrix
from services.chatbot_engine import predict_from_vector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Medical backend is running"}

@app.post("/api/chat")
async def chat(payload: dict):
    message = payload.get("message")
    if not message or not isinstance(message, str):
        raise HTTPException(status_code=400, detail="Dữ liệu đầu vào không hợp lệ")

    symptoms = process_clinical_text(message)

    if not symptoms:
        return {
            "status": "success",
            "reply": (
                "Mình chưa nhận ra triệu chứng cụ thể nào trong mô tả của bạn. "
                "Bạn có thể mô tả chi tiết hơn, ví dụ: sốt, đau đầu, ho khan, mệt mỏi…?"
            ),
            "prediction": None,
            "detected_symptoms": [],
        }

    input_vector = convert_to_matrix(symptoms)
    prediction = predict_from_vector(input_vector)

    disease_name = prediction["prediction"]
    reply_text = (
        f"Dựa trên {len(symptoms)} triệu chứng bạn mô tả, "
        f"tôi chẩn đoán bạn có thể đang mắc: **{disease_name}**.\n\n"
        f"Lưu ý: Đây chỉ là dự đoán từ AI, không thay thế cho ý kiến bác sĩ. "
        f"Hãy đến cơ sở y tế để được khám và chẩn đoán chính xác."
    )

    return {
        "status": "success",
        "reply": reply_text,
        "prediction": prediction,
        "detected_symptoms": symptoms,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)