import json
import os
from urllib.parse import parse_qs

# IMPORTANT: Vercel gives /var/task as root
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

        except Exception:
            continue

    return None


# ✅ THIS is what Vercel calls
def handler(request, context):
    # get query string: ?name=AMD
    query = parse_qs(request.get("queryStringParameters") or {})
    name = query.get("name", [None])[0]

    if not name:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "missing name"})
        }

    result = search_all_files(name)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps(result or {"error": "not found"})
    }