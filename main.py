from flask import Flask, request
from services.bank_services_impl import BankServicesImpl
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from entities.account import Account
from utils.response_as_json import response_as_json
from utils.catch_invalid_inputs import catch_invalid_inputs
from utils.handle_exceptions import handle_exceptions_no_args, handle_exceptions_w_args

import logging

app = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

clientDao = ClientDAOPostgres()
accountDao = AccountDAOPostgres()
bankingService = BankServicesImpl(accountDao, clientDao)


# Create a new client
@app.route("/clients", methods=['POST'])
@handle_exceptions_no_args
def create_client():
        client = list(request.json.values())
        result = bankingService.add_client(Client(*client))
        return response_as_json("success", 201, result.as_json_dict()), 201


#Create account for client with id of.
@app.route("/clients/<client_id>/accounts", methods=['POST'])
@handle_exceptions_w_args
def create_account_for_client(client_id: str):
    # 1) get body
    body = request.json

    # 2) make sure input data is valid
    acct_type = catch_invalid_inputs("string", body["type"])
    balance = catch_invalid_inputs("number", body["balance"])
    catch_invalid_inputs("int", int(client_id))

    # 3) handle request and return data
    account = Account(0, acct_type, balance, int(client_id))
    result = bankingService.create_account_for_client(int(client_id), account)
    return response_as_json("success", 201, result.as_json_dict()), 201


# Get all clients
@app.route("/clients", methods=['GET'])
@handle_exceptions_no_args
def get_all_clients():
    results = bankingService.retrieve_all_clients()
    json_list = [client.as_json_dict() for client in results]
    return response_as_json("success", 200, json_list), 200


# get client by id
@app.route("/clients/<user_id>", methods=['GET'])
@handle_exceptions_w_args
def get_client_by_id(user_id: str):
    # 1) make sure input data is valid
    user_id = catch_invalid_inputs("int", int(user_id))

    # 2) handle request and send data
    client = bankingService.retrieve_client_by_id(int(user_id))
    return response_as_json('success', 200, client.as_json_dict()), 200


# get all accounts for client by client_id, or get all account within range
@app.route("/clients/<client_id>/accounts", methods=['GET'])
@handle_exceptions_w_args
def get_all_clients_accounts(client_id: str):
    # 1) validate client id
    client_id = catch_invalid_inputs("int", int(client_id))
    upper = lower = accounts = 0

    # 2) check for queries
    if request.args:
        # 3) get queries and validate them
        upper = float(request.args["amountLessThan"])
        lower = float(request.args["amountGreaterThan"])
        catch_invalid_inputs("number", upper)
        catch_invalid_inputs("number", lower)

    # 3) if query strings, get accounts in range
    if upper and lower:
        accounts = bankingService.retrieve_client_accounts_within_range(int(client_id), lower, upper)
    # 4) otherwise just get all client's accounts
    else:
        accounts = bankingService.retrieve_all_clients_accounts(int(client_id))

    # 5) make data json friendly and return
    json_list = [acct.as_json_dict() for acct in accounts]
    return response_as_json('success', 200, json_list), 200


# get account by id for client
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["GET"])
@handle_exceptions_w_args
def get_account_by_client_id(account_id: str, client_id: str):
    # 1) validate data
    catch_invalid_inputs("int", int(account_id))
    catch_invalid_inputs("int", int(client_id))

    # 2) handle request and return
    result = bankingService.retrieve_client_account_by_id(int(account_id), int(client_id))
    return response_as_json("success", 200, result.as_json_dict()), 200


# get all accounts
@app.route("/accounts", methods=['GET'])
@handle_exceptions_no_args
def get_all_accounts():
    results = bankingService.retrieve_all_accounts()
    json_list = [acct.as_json_dict() for acct in results]
    return response_as_json("success", 200, json_list), 200


# Update
# update account by id and client id
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PUT"])
@handle_exceptions_w_args
def update_users_account_by_account_id(account_id: str, client_id: str):
    body = request.json

    # 1) validate data
    catch_invalid_inputs("int", body["accountId"])
    catch_invalid_inputs("string", body["accountType"])
    catch_invalid_inputs("number", body["balance"])
    catch_invalid_inputs("int", body["clientId"])
    catch_invalid_inputs("int", int(account_id))
    catch_invalid_inputs("int", int(client_id))

    # 2) handle request and return
    account = Account(body["accountId"], body["accountType"], body["balance"], body["clientId"])
    updated = bankingService.update_clients_account_by_account_id(int(client_id), int(account_id), account)
    return response_as_json("success", 200, updated.as_json_dict()), 200


# update client by client id
@app.route("/clients/<client_id>", methods=["PUT"])
@handle_exceptions_w_args
def update_client(client_id: str):
    data = request.json

    # 1) validate data
    catch_invalid_inputs("int", int(client_id))
    catch_invalid_inputs("string", data["firstName"])
    catch_invalid_inputs("string", data["lastName"])

    # 2) handle request
    client = Client(int(client_id), data["firstName"], data["lastName"])
    updated = bankingService.update_client(client)
    return response_as_json("success", 200, updated.as_json_dict()), 200


# make account transfers
@app.route("/clients/<client_id>/accounts/<account_fr>/transfer/<account_to>", methods=["PATCH"])
@handle_exceptions_w_args
def account_transfer(client_id: str, account_fr: str, account_to: str):
    body = request.json
    # 1) validate data
    catch_invalid_inputs("number", body["amount"])
    catch_invalid_inputs("int", int(client_id))
    catch_invalid_inputs("int", int(account_fr))
    catch_invalid_inputs("int", int(account_to))

    # 2) handle request
    result = bankingService.transfer_clients_funds(int(client_id), body["amount"], int(account_fr), int(account_to))
    return response_as_json("success", 201, result), 201


# withdraw or deposit
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PATCH"])
@handle_exceptions_w_args
def client_transaction(client_id: str, account_id: str):
    # 1) validate data
    data = request.json
    catch_invalid_inputs("int", int(client_id))
    catch_invalid_inputs("int", int(account_id))
    catch_invalid_inputs("number", data["amount"])
    catch_invalid_inputs("string", data["transactionType"])

    # 2) submit request
    updated = bankingService.withdraw_or_deposit(int(account_id), int(client_id), data["transactionType"],
                                                 data["amount"])
    return response_as_json("success", 200, updated.as_json_dict()), 200


# Delete
@app.route("/clients/<client_id>", methods=["DELETE"])
@handle_exceptions_w_args
def delete_client(client_id: str):
    # 1) validate data
    catch_invalid_inputs("int", int(client_id))

    # 2) submit request
    result = bankingService.delete_client_and_accounts(int(client_id))
    return response_as_json("Success", 205), 205


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["DELETE"])
@handle_exceptions_w_args
def delete_account_by_both_ids(client_id: str, account_id: str):
    # 1) validate data
    catch_invalid_inputs("int", int(client_id))
    catch_invalid_inputs("int", int(account_id))

    result = bankingService.delete_account_by_client_id(int(client_id), int(account_id))
    return response_as_json("Success", 205), 205


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, port=3030)
