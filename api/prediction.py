import json
import os
from urllib.parse import parse_qs

def handler(request, context=None):

    # Get query params
    query = parse_qs(request.query_string.decode())
    name = query.get("name", [None])[0]

    if not name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "name is required"})
        }

    # project root
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PRED_DIR = os.path.join(BASE_DIR, "Predictions")

    # search all json files
    for file in os.listdir(PRED_DIR):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(PRED_DIR, file)

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            # match by name key
            if name in data:
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "name": name,
                        "data": data[name]
                    })
                }

        except Exception as e:
            continue

    return {
        "statusCode": 404,
        "body": json.dumps({"error": "not found"})
    }