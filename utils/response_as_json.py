def response_as_json(message: str, status: int, data=None) -> dict:
    if data is not None:
        return {
            "message": message,
            "status": status,
            "data": [data]
        }
    else:
        return {
            "message": message,
            "status": status
        }
