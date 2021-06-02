from flask import Flask, request
from services.bank_services_impl import BankServicesImpl
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from entities.account import Account
from utils.response_as_json import response_as_json
from exceptions.client_not_found_error import ClientNotFoundError
from exceptions.account_not_found_error import AccountNotFoundError
from exceptions.overdraft_exception import OverDraftError
import logging

app = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

clientDao = ClientDAOPostgres()
accountDao = AccountDAOPostgres()
bankingService = BankServicesImpl(accountDao, clientDao)


# Create a new client
@app.route("/clients", methods=['POST'])
def create_client():
    try:
        client = list(request.json.values())
        result = bankingService.add_client(Client(*client))
        return response_as_json("success", 201, result.as_json_dict()), 201
    except Exception as e:
        return response_as_json(str(e), 500), 500


# Create account for client with id of.
@app.route("/clients/<client_id>/accounts", methods=['POST'])
def create_account_for_client(client_id: int):
    try:
        body = request.json
        account = Account(0, body["type"], body["balance"], int(client_id))
        result = bankingService.create_account_for_client(client_id, account)
        return response_as_json("success", 201, result.as_json_dict()), 201
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except OverDraftError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


# Get all clients
@app.route("/clients", methods=['GET'])
def get_all_clients():
    try:
        results = bankingService.retrieve_all_clients()
        json_list = [client.as_json_dict() for client in results]
        return response_as_json("success", 200, json_list), 200
    except Exception as e:
        return response_as_json(str(e), 500), 500


# get client by id
@app.route("/clients/<user_id>", methods=['GET'])
def get_client_by_id(user_id: str):
    try:
        client = bankingService.retrieve_client_by_id(int(user_id))
        return response_as_json('success', 200, client.as_json_dict()), 200
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


# get all accounts for client by client_id, or get all account within range
@app.route("/clients/<client_id>/accounts", methods=['GET'])
def get_all_clients_accounts(client_id: str):
    try:
        upper = lower = accounts = 0
        if request.args:
            upper = float(request.args["amountLessThan"])
            lower = float(request.args["amountGreaterThan"])
        if upper and lower:
            print(upper, lower)
            accounts = bankingService.retrieve_client_accounts_within_range(int(client_id), lower, upper)
        else:
            accounts = bankingService.retrieve_all_clients_accounts(int(client_id))
        json_list = [acct.as_json_dict() for acct in accounts]
        return response_as_json('success', 200, json_list), 200
    except TypeError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


# get account by id for client
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["GET"])
def get_account_by_client_id(account_id: str, client_id: str):
    try:
        result = bankingService.retrieve_client_account_by_id(int(account_id), int(client_id))
        return response_as_json("success", 200, result.as_json_dict()), 200
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except AccountNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


# get all accounts
@app.route("/accounts", methods=['GET'])
def get_all_accounts():
    try:
        results = bankingService.retrieve_all_accounts()
        json_list = [acct.as_json_dict() for acct in results]
        return response_as_json("success", 200, json_list), 200
    except Exception as e:
        return response_as_json(str(e), 500), 500


# Update
# update account by id and client id
@app.route("/clients/<client_id>/accounts/<account_id>", methods = ["PUT"])
def update_users_account_by_account_id(account_id: str, client_id: str):
    try:
        body = request.json
        account = Account(body["accountId"], body["accountType"], body["balance"], body["clientId"])
        updated = bankingService.update_clients_account_by_account_id(int(client_id), int(account_id), account)
        return response_as_json("success", 200, updated.as_json_dict()), 200
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except OverDraftError as e:
        return response_as_json(str(e), 404), 404
    except TypeError as e:
        return response_as_json(str(e), 400), 400
    except AccountNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except LookupError as e:
        return response_as_json(str(e), 400), 400
    except Exception as e:
        return response_as_json(str(e), 500), 500


# update client by client id
@app.route("/clients/<client_id>", methods=["PUT"])
def update_client(client_id: str):
    try:
        data = request.json
        client = Client(int(client_id), data["firstName"], data["lastName"])
        updated = bankingService.update_client(client)
        return response_as_json("success", 200, updated.as_json_dict()), 200
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except TypeError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


# make account transfers
@app.route("/clients/<client_id>/accounts/<account_fr>/transfer/<account_to>", methods = ["PATCH"])
def account_transfer(client_id: str, account_fr: str, account_to: str):
    try:
        body = request.json
        result = bankingService.transfer_clients_funds(int(client_id), body["amount"], int(account_fr), int(account_to))
        return response_as_json("success", 201, result), 201
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except AccountNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except OverDraftError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


# withdraw or deposit
@app.route("/clients/<client_id>/accounts/<account_id>", methods = ["PATCH"])
def client_transaction(client_id: str, account_id: str):
    try:
        data = request.json
        updated = bankingService.withdraw_or_deposit(int(account_id), int(client_id), data["transactionType"], data["amount"])
        return response_as_json("success", 200, updated.as_json_dict()), 200
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except TypeError as e:
        return response_as_json(str(e), 400), 400
    except OverDraftError as e:
        return response_as_json(str(e), 422), 422
    except AccountNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


# Delete
@app.route("/clients/<client_id>", methods= ["DELETE"])
def delete_client(client_id: str):
    try:
        result = bankingService.delete_client_by_id(int(client_id))
        return response_as_json("Success", 205), 205
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


@app.route("/clients/<client_id>/accounts/<account_id>", methods= ["DELETE"])
def delete_account_by_both_ids(client_id: str, account_id: str):
    try:
        result = bankingService.delete_account_by_client_id(int(client_id), int(account_id))
        return response_as_json("Success", 205), 205
    except ValueError as e:
        return response_as_json(str(e), 404), 404
    except ClientNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except AccountNotFoundError as e:
        return response_as_json(str(e), 404), 404
    except Exception as e:
        return response_as_json(str(e), 500), 500


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, port=3030)
