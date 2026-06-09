import json
import os
from urllib.parse import parse_qs

def handler(request):
    # get query params
    query = parse_qs(request.query_string.decode())

    type_ = query.get("type", [None])[0]
    name = query.get("name", [None])[0]

    if not type_ or not name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "type and name are required"})
        }

    file_path = os.path.join("Predictions", f"{type_}.json")

    if not os.path.exists(file_path):
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "type not found"})
        }

    with open(file_path, "r") as f:
        data = json.load(f)

    result = data.get(name)

    if not result:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "name not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "type": type_,
            "name": name,
            "data": result
        })
    }