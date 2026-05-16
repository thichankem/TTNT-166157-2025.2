from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from services.transform_input import process_clinical_text, convert_to_matrix
from services.chatbot_engine import predict_from_vector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat")
async def chat(payload: dict):
    message = payload.get("message")
    if not message or not isinstance(message, str):
        raise HTTPException(status_code=400, detail="Dữ liệu đầu vào không hợp lệ")

    symptoms = process_clinical_text(message)
    input_vector = convert_to_matrix(symptoms)
    prediction = predict_from_vector(input_vector)

    top_3 = ", ".join(
        [f"{item['disease']} ({item['probability']*100:.1f}%)" for item in prediction["top_3"]]
    )
    reply_text = (
        f"Dựa theo những gì bạn mô tả, mình thấy khả năng cao nhất là: {prediction['prediction']}. \n"
        f"Top 3 khả năng: {top_3}."
    )

    return {
        "status": "success",
        "reply": reply_text,
        "prediction": prediction,
        "detected_symptoms": symptoms,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)