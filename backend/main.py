from fastapi import FastAPI, File, UploadFile
import datetime
import uvicorn
import shutil
import os
import pytz
from PIL import Image

from utils import predict_normal, zeroshot

app = FastAPI()


@app.get("/")
async def health_check():
    return {
        "message": "Service is running ✅",
        "timestamp": datetime.datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        upload_path = f"/tmp/{datetime.datetime.now().timestamp()}.png"
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        predicted_value, predicted_accuracy = await predict_normal(upload_path)

        return {
            "path": upload_path,
            "predicted_value": predicted_value,
            "predicted_accuracy": predicted_accuracy,
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/predict_test")
async def predict_zeroshot(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        upload_path = f"/tmp/{(datetime.datetime.now()).timestamp()}.png"

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        predicted_value, predicted_accuracy = await zeroshot(upload_path)

        return {
            "path": upload_path,
            "predicted_value": predicted_value,
            "predicted_accuracy": predicted_accuracy,
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True
    )
