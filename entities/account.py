import json


class Account:
    def __init__(self, account_id: int, account_type: str, balance: float, client_id: int):
        self.account_id = account_id
        self.account_type = account_type
        self.balance = balance
        self.client_id = client_id

    # returns a JSON STRING with camel case fields
    def __str__(self) -> str:
        return json.dumps(self.as_json_dict())

    # returns a DICTIONARY representation of self with camelCase fields
    def as_json_dict(self) -> dict:
        return {
            "accountId": self.account_id,
            "accountType": self.account_type,
            "balance": self.balance,
            "clientId": self.client_id
        }
