import json


class Client:
    def __init__(self, client_id: int, first_name: str, last_name: str):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name

    # returns a JSON STRING with camel case fields
    def __str__(self) -> str:
        return json.dumps(self.as_json_dict())

    # returns a DICTIONARY representation of self with camelCase fields
    def as_json_dict(self) -> dict:
        return {
            "clientId": self.client_id,
            "firstName": self.first_name,
            "lastName": self.last_name
        }
