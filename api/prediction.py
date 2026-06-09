import json
import os
from fastapi import FastAPI

app = FastAPI()

# load data once (IMPORTANT for performance)
DATA_CACHE = {}

def load_file(type_):
    if type_ in DATA_CACHE:
        return DATA_CACHE[type_]

    file_path = os.path.join("Predictions", f"{type_}.json")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r") as f:
        DATA_CACHE[type_] = json.load(f)

    return DATA_CACHE[type_]


@app.get("/api/prediction")
def get_prediction(type: str, name: str):
    data = load_file(type)

    if not data:
        return {"error": "type not found"}

    result = data.get(name)

    if not result:
        return {"error": "name not found"}

    return {
        "type": type,
        "name": name,
        "data": result
    }