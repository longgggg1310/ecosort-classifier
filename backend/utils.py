from keras.models import load_model
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import os
import time
from dotenv import load_dotenv

load_dotenv()
import numpy as np
import requests
import base64

HF_API = os.getenv("HF_API")
model = load_model("models/model.h5")
output_class = ["battery", "glass", "metal", "organic", "paper", "plastic"]
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def preprocessing_input(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)  # ResNet50 preprocess_input
    return img


def predict_normal(new_image_path):
    try:
        test_image = preprocessing_input(new_image_path)
        predicted_array = model.predict(test_image)
        predicted_value = output_class[np.argmax(predicted_array)]
        predicted_accuracy = round(np.max(predicted_array) * 100, 2)

        return predicted_value, predicted_accuracy
    except Exception as e:
        return f"Error processing image: {str(e)}", 0


def zeroshot(new_image_path):
    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14-336"
            headers = {"Authorization": f"Bearer {HF_API}"}

            def query(data):
                with open(data["image_path"], "rb") as f:
                    img = f.read()
                payload = {
                    "parameters": data["parameters"],
                    "inputs": base64.b64encode(img).decode("utf-8"),
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                time.sleep(3)
                return response.json()

            output = query(
                {
                    "image_path": f"{new_image_path}",
                    "parameters": {"candidate_labels": output_class},
                }
            )
            max_component = max(output, key=lambda x: x["score"])
            predicted_value, predicted_accuracy = (
                max_component["label"],
                max_component["score"],
            )
            return predicted_value, predicted_accuracy

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            retry_count += 1
            if retry_count < max_retries:
                print("Retrying...")
                time.sleep(1)

    return "unknown", 0
