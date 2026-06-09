import json
import os
from fastapi import FastAPI

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_DIR = os.path.join(BASE_DIR, "Predictions")


def search_all_files(name: str):
    for file in os.listdir(PRED_DIR):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(PRED_DIR, file)

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            if name in data:
                return {
                    "file": file,
                    "name": name,
                    "data": data[name]
                }
        except:
            continue

    return None


@app.get("/api/prediction")
def get_prediction(name: str):
    result = search_all_files(name)

    if not result:
        return {"error": "not found"}

    return result