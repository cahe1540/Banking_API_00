from services.bank_services import BankServices
from services.account_services_impl import AccountServicesImpl
from services.client_services_impl import ClientServicesImpl
from daos.account_dao import AccountDAO
from daos.client_dao import ClientDAO
from entities.account import Account


class BankServicesImpl(BankServices, AccountServicesImpl, ClientServicesImpl):

    def __init__(self, accountDao: AccountDAO, clientDao: ClientDAO):
        super().__init__(accountDao=accountDao, clientDao=clientDao)

    def update_clients_account_by_account_id(self, client_id: int, account_id: int, account: Account) -> Account:
        # 1) check if client exists
        self.clientDao.get_client_by_Id(client_id)

        # 2) update account
        return self.accountDao.update_account_by_client_id(client_id, account_id, account)

    def create_account_for_client(self, client_id: int, account: Account) -> Account:
        # 1) check if account client_id exists in clients
        self.clientDao.get_client_by_Id(account.client_id)
        # 2) if exists, create the account
        new_acct = self.accountDao.create_account(account)
        return new_acct

    def retrieve_all_clients_accounts(self, client_id: int) -> list[Account]:
        # 1) check if client exists
        self.clientDao.get_client_by_Id(client_id)

        # 2) retrieve accounts and return
        return self.accountDao.get_accounts_by_client_id(client_id)

    def transfer_clients_funds(self, client_id: int, amount: float or int, acct_from_id: int, acct_to_id: int) -> bool:
        # 1) check if accounts exist
        acct1 = self.accountDao.get_account_by_id(acct_from_id)
        acct2 = self.accountDao.get_account_by_id(acct_to_id)

        # 2) perform transfer and return True for success
        self.accountDao.update_account_balance(acct1.account_id, client_id, 'withdraw', amount)
        self.accountDao.update_account_balance(acct2.account_id, client_id, 'deposit', amount)
        return True

    def withdraw_or_deposit(self, account_id: int, client_id: int, transaction_type: str, amount: float) -> Account:
        # 1) check if client exists
        client = self.clientDao.get_client_by_Id(client_id)

        # 2) make transaction
        return self.accountDao.update_account_balance(account_id, client_id, transaction_type, amount)

    def delete_client_and_accounts(self, client_id: int) -> bool:
        # 1) delete all accounts by client ID
        result = self.accountDao.delete_all_accounts_by_client_id(client_id)

        # 2) delete client by id
        return self.clientDao.delete_client(client_id)

    def delete_account_by_client_id(self, client_id: int, account_id: int) -> bool:
        # 1) check if client exists
        result = self.clientDao.get_client_by_Id(client_id)

        # 2) delete the account by client and account id
        return self.accountDao.delete_account_by_id_and_client_id(account_id, client_id)

    # OVERRIDE the method inherited from account_services_impl
    def retrieve_client_accounts_within_range(self, client_id: int, lower: float or int, upper: float or int):
        # 1. #check if the client with id client_id exists
        client = self.clientDao.get_client_by_Id(client_id)

        # 2) return accounts
        return self.accountDao.get_client_accounts_within_range(client_id, lower, upper)