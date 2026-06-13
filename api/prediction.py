import json
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing. Later replace with your frontend URL.
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

        file_path = os.path.join(PRED_DIR, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if name in data:
                return {
                    "file": file,
                    "name": name,
                    "data": data[name]
                }

        except Exception as e:
            print(e)
            continue

    return None


@app.get("/api/prediction")
async def get_prediction(name: str = Query(...)):
    result = search_all_files(name)

    if result is None:
        return {"error": "not found"}

    return result