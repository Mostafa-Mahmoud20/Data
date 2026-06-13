from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_DIR = os.path.join(BASE_DIR, "Predictions")


def search_all_files(name: str):
    if not os.path.exists(PRED_DIR):
        return None

    for file in os.listdir(PRED_DIR):
        if not file.endswith(".json"):
            continue

        path = os.path.join(PRED_DIR, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if name in data:
                return {"file": file, "name": name, "data": data[name]}
        except:
            pass

    return None


@app.get("/api/prediction")
def prediction(name: str):
    result = search_all_files(name)
    return result or {"error": "not found"}