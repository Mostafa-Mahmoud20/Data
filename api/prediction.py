import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_DIR = os.path.join(BASE_DIR, "Predictions")


def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Headers": "*",
    }


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
                    "data": data[name],
                }

        except Exception:
            continue

    return None


def handler(request):
    # ✅ HANDLE CORS PRE-FLIGHT
    if request.get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": "",
        }

    params = request.get("queryStringParameters") or {}
    name = params.get("name")

    if not name:
        return {
            "statusCode": 400,
            "headers": cors_headers(),
            "body": json.dumps({"error": "missing name"}),
        }

    result = search_all_files(name)

    return {
        "statusCode": 200,
        "headers": cors_headers(),
        "body": json.dumps(result or {"error": "not found"}),
    }