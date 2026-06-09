import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_DIR = os.path.join(BASE_DIR, "Predictions")


def handler(request):
    from urllib.parse import parse_qs

    query = parse_qs(request.query_string.decode())
    name = query.get("name", [None])[0]

    if not name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "name is required"})
        }

    # 🔍 scan all files in Predictions folder
    for file in os.listdir(PRED_DIR):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(PRED_DIR, file)

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            # search inside file
            if name in data:
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "file": file,
                        "name": name,
                        "data": data[name]
                    })
                }

        except Exception as e:
            continue

    return {
        "statusCode": 404,
        "body": json.dumps({"error": "component not found"})
    }