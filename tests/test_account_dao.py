from daos.account_dao import AccountDAO
from daos.account_dao_postgres import AccountDAOPostgres
from entities.account import Account
from exceptions.account_not_found_error import AccountNotFoundError
from exceptions.overdraft_exception import OverDraftError

# test Data
acctObj1: Account = Account(0, 'checking', 0.00, 1)
acctObj2: Account = Account(0, 'checking', 10.00, 2)
acctObj3: Account = Account(0, 'saving', 20.00, 2)
find_Obj_2: Account = Account(2, 'checking', 4000.00, 1)
updated_acct_1: Account = Account(7, 'saving', 100.00, 1)
updated_acct_1_2: Account = Account(7, 'checking', 11111.00, 1)
updater_Fail: Account = Account(555, 'checking', 100, 4)

# Dao object to perform tests on
accountDao: AccountDAO = AccountDAOPostgres()

# ------------CREATE
# add 3 accounts
def test_create_acct():
    accountDao.create_account(acctObj1) #acctObj1 has id of 14
    accountDao.create_account(acctObj2) #acctObj2 has id of 15
    result = accountDao.create_account(acctObj3) #acctObj3 has id of 16
    assert result.account_id == 17 #use 16 for exibition


# ------------READ
# successful attempt at getting acct by id
def test_get_acct_by_id():
    test_num = 2
    result = accountDao.get_account_by_id(test_num)
    assert str(result) == str(find_Obj_2)


# the account with input id doesn't exist
def test_get_by_id_fail():
    test_num = 44
    try:
        result = accountDao.get_account_by_id(test_num)
        assert False
    except AccountNotFoundError as e:
        assert str(e) == f'Account with id: {test_num} was not found.'

def test_get_acct_by_id_and_user_id():
    acct = accountDao.get_account_by_id_and_client(7,4)
    assert str(acct) == str(Account(7, 'saving', 2000.00, 4))


# # fail because empty
# def test_get_acct_by_id_and_user_id_fail_empty():
#     try:
#         acct = accountDao.get_account_by_id_and_client(111, 1111)
#         assert False
#     except AccountNotFoundError as e:
#         assert str(e) == f'The account with id: 3 and client_id: 5 could not be found. Account could not be retrieved.'


# fail because not present
def test_get_acct_by_id_and_user_id_fail():
    try:
        acct = accountDao.get_account_by_id_and_client(111,655)
        assert False
    except AccountNotFoundError as e:
        assert str(e) == 'Account with id: 111 and client_id: 655 was not found.'


# search within range success
def test_get_in_range():
    test_num = 4
    results = accountDao.get_client_accounts_within_range(test_num, 400.00, 4000.00)
    assert len(results) == 2


# empty array returned because nothing found in range
def test_get_in_range_out_of_range():
    test_num = 4
    results = accountDao.get_client_accounts_within_range(test_num, 100000.00, 200000.00)
    assert len(results) == 0


# # empty array returned because no such accounts exist to search within range
# def test_get_in_range_no_accounts():
#     test_num = 12
#     results = accountDao.get_client_accounts_within_range(test_num, 2000.00, 4000.00)
#     assert len(results) == 0


# empty array returned because ZERO accounts exist, fail search within range
def test_get_in_range_empty():
    test_num = 7  # Rick Morty will always not have accounts
    results = accountDao.get_client_accounts_within_range(test_num, 2000, 4000)
    assert len(results) == 0


# successfully return all accounts given client id
def test_get_acct_by_client_id():
    test_num = 4
    accounts = accountDao.get_accounts_by_client_id(test_num)
    assert len(accounts) == 2


# return empty array because id not in data
def test_get_acct_by_client_id_return_none():
    test_num = 10000
    accounts = accountDao.get_accounts_by_client_id(test_num)
    assert len(accounts) == 0

# get all accounts success
def test_get_all_accts():
    results = accountDao.get_all_accounts()
    assert len(results) >= 16  # start with 16

# # run test on get_all_accounts() before any accounts are added
# def test_get_all_accounts_with_no_data():
#     results = accountDao.get_all_accounts()
#     assert len(results) == 0


# # ------------UPDATE
# # successfully update account
def test_update_acct():
    result = accountDao.update_account(updated_acct_1)
    assert str(result) == str(updated_acct_1)


# # no accounts exist, so update fails
# def test_fail_update_acct_empty():
#     try:
#         result = accountDao.update_account(updater_Fail)
#         assert False
#     except AccountNotFoundError as e:
#         assert str(e) == "Account with id: 555 was not found, account could not be updated."


# success update account with client_id and account_id
def test_update_clients_acct_by_acct_id():
    result: Account = accountDao.update_account_by_client_id(1, 3, {"accountType": "saving", "balance": 11000.00})
    assert result.balance == 11000.00

# fail update account with client_id and account_id because account doesn't exist
def test_update_clients_acct_by_acct_id():
    try:
        result: Account = accountDao.update_account_by_client_id(1111, 3, updater_Fail)
        assert False
    except AccountNotFoundError as e:
        assert str(e) == 'Account with id: 555 was not found.'


# successful withdraw
def test_update_account_balance_withdraw():
    result: Account = accountDao.update_account_balance(2,1,'withdraw', 1000.00)
    assert result.balance == 3000.00  # start this as 3000.00

# successful deposit
def test_update_account_balance_deposit():
    result: Account = accountDao.update_account_balance(1, 1, 'deposit', 1000.00)
    assert result.balance == 3000.00 # start this as 3000


# fail withdraw because of overdraft
def test_update_account_balance_withdraw_fail():
    try:
        result: Account = accountDao.update_account_balance(3,2, 'withdraw', 100000.00)
        assert False
    except OverDraftError as e:
        assert str(e) == f'Account with id: 3 has insufficient funds, the transaction was cancelled.'


# fail, account does not exist
def test_update_account_balance_fail_deposit_fail():
    try:
        result: Account = accountDao.update_account_balance(55, 6, 'deposit', 1000.00)
        assert result.balance == 11000.00
    except AccountNotFoundError as e:
        assert str(e) == f'Account with id: 55 was not found.'


# the account with corresponding input id doesn't exist
def test_fail_update_acct():
    try:
        result = accountDao.update_account(updater_Fail)
        assert False
    except AccountNotFoundError as e:
        assert str(e) == "Account with id: 555 was not found."


# pass update account given id, client id and changes
def test_update_account_by_client_id():
    result = accountDao.update_account_by_client_id(7, 1, updated_acct_1_2)
    assert str(result) == str(updated_acct_1_2)

# fail, does not exist
def test_update_balance():
    try:
        result = accountDao.update_account_by_client_id(555, 2, updater_Fail)
        assert False
    except AccountNotFoundError as e:
        assert str(e) == 'Account with id: 555 was not found.'


# ------------DELETE
# successfully deleted account
def test_delete_acct():
    result = accountDao.delete_account(16)
    assert result == True

# successfully delete by id and client id
def test_delete_acct_by_client_id():
    assert accountDao.delete_account_by_id_and_client_id(14,2) is True

# fail to delete by id and client id
def test_delete_acct_by_client_id_fail():
    try:
        accountDao.delete_account_by_id_and_client_id(444,2)
        assert False
    except AccountNotFoundError as e:
        assert str(e) == 'Account with id: 444 was not found.'


# the account with corresponding id doesn't exist, delete fail
def test_fail_delete_acct():
    try:
        accountDao.delete_account(222)
        assert False
    except AccountNotFoundError as e:
        assert str(e) == "Account with id: 222 was not found."


# # fail to delete because no accounts exist
# def test_fail_delete_acct_empty():
#     try:
#         accountDao.delete_account(222)
#         assert False
#     except AccountNotFoundError as e:
#         assert str(e) == "Account with id: 222 was not found, account could not be deleted."

# delete none
def test_delete_all_by_client_id():
    result = accountDao.delete_all_accounts_by_client_id(8)
    assert result == 0

# delete multiple
def test_delete_all_by_client_id():
    result = accountDao.delete_all_accounts_by_client_id(9)
    assert result == 3

def test_delete_all_by_client_id_fail():
    result = accountDao.delete_all_accounts_by_client_id(99)
    assert result == 0
