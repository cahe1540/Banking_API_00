from services.bank_services_impl import BankServicesImpl
from daos.account_dao_local import AccountDAOLocal
from daos.client_dao_local import ClientDAOLocal
from daos.account_dao import AccountDAO
from daos.client_dao import ClientDAO
from entities.account import Account
from entities.client import Client
from exceptions.client_not_found_error import ClientNotFoundError
from exceptions.account_not_found_error import AccountNotFoundError
from exceptions.overdraft_exception import OverDraftError
from unittest.mock import MagicMock, Mock

accountDao: AccountDAO = AccountDAOLocal()
clientDao: ClientDAO = ClientDAOLocal()
bankService = BankServicesImpl(accountDao, clientDao)


# pass delete client by id
def test_delete_client_by_id():
    bankService.accountDao.delete_all_accounts_by_client_id = MagicMock(return_value = 2)
    bankService.clientDao.delete_client = MagicMock(return_value=True)
    result = bankService.delete_client_and_accounts(1)
    assert result is True


# fail to delete client by id because not exist
def test_fail_delete_client_by_id():
    try:
        bankService.accountDao.delete_all_accounts_by_client_id = MagicMock(return_value=0)
        bankService.clientDao.delete_client = Mock(side_effect=ClientNotFoundError('Client with id: 1 was not found, client could not be deleted.'))
        result = bankService.delete_client_and_accounts(1)
        assert False
    except ClientNotFoundError as e:
        assert str(e) == f'Client with id: 1 was not found, client could not be deleted.'


# successfully deleted client when client exists, but has no bank accounts
def test_delete_client_by_id_no_accounts():
    bankService.accountDao.delete_all_accounts_by_client_id = MagicMock(return_value = 0)
    bankService.clientDao.delete_client = MagicMock(return_value = True)
    result = bankService.delete_client_and_accounts(1)
    assert result is True


# successfully added a new account for x user
def test_add_account_to_client():
    acct = Account(1, 'checking', 1000.00, 4)
    bankService.clientDao.get_client_by_Id = MagicMock(return_value = {4: Client(4, 'Carlos', 'Herrera')})
    bankService.accountDao.create_account = MagicMock(return_value = acct)
    new_acct = bankService.create_account_for_client(4, acct)
    assert str(new_acct) == str(acct)


# fail to create account because user does not exist
def test_add_account_to_client_fail():
    acct = Account(1, 'checking', 1000.00, 4)
    bankService.clientDao.get_client_by_Id = Mock(side_effect= ClientNotFoundError('Client with id: 1 was not found.'))
    bankService.accountDao.create_account = MagicMock(return_value=acct)
    try:
        new_acct = bankService.create_account_for_client(4, acct)
        assert False
    except ClientNotFoundError as e:
        assert str(e) == 'Client with id: 1 was not found.'


# successfully transferred funds
def test_transfer_funds():
    acct1 = Account(1, 'checking', 1000.00, 4)
    acct2 = Account(2, 'saving', 2000.00, 4)
    acct1_after = Account(1, 'checking', 500.00, 4)
    acct2_after = Account(2, 'saving', 2500.00, 4)
    mock = Mock(side_effect= [acct1, acct2, acct1_after, acct2_after])
    bankService.accountDao.get_account_by_id = mock
    bankService.accountDao.update_account_balance = mock
    result = bankService.transfer_clients_funds(4,500.00, 1, 2)
    assert result is True


# fail to transfer funds because a single account doesn't exist
def test_transfer_funds_fail():
    acct2 = Account(2, 'saving', 2000.00, 4)
    acct1_after = Account(1, 'checking', 500.00, 4)
    acct2_after = Account(2, 'saving', 2500.00, 4)
    try:
        mock = Mock(side_effect= [AccountNotFoundError('Acct not found.'), acct2, acct1_after, acct2_after])
        bankService.accountDao.get_account_by_id = mock
        bankService.accountDao.update_account_balance = mock
        result = bankService.transfer_clients_funds(4,500.00, 1, 2)
        assert False
    except AccountNotFoundError as e:
        assert str(e) == 'Acct not found.'


# fail to transfer funds because overdraft
def test_transfer_funds_fail_overdraft():
    acct1 = Account(1, 'checking', 1000.00, 4)
    acct2 = Account(2, 'saving', 2000.00, 4)
    acct1_after = Account(1, 'checking', 500.00, 4)
    acct2_after = Account(2, 'saving', 2500.00, 4)
    try:
        mock = Mock(side_effect= [acct1, acct2, OverDraftError('Overdraft.'), acct2_after])
        bankService.accountDao.get_account_by_id = mock
        bankService.accountDao.update_account_balance = mock
        result = bankService.transfer_clients_funds(4,1000.00, 1, 2)
        assert False
    except OverDraftError as e:
        assert str(e) == 'Overdraft.'
