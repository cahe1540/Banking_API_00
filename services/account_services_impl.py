from services.account_services import AccountServices
from entities.account import Account
from daos.account_dao import AccountDAO


class AccountServicesImpl(AccountServices):
    def __init__(self, accountDao: AccountDAO, **kwargs):
        super().__init__(**kwargs)
        self.accountDao = accountDao

    def add_account(self, account: Account):
        return self.accountDao.create_account(account)

    def retrieve_account_by_id(self, account_id: int):
        return self.accountDao.get_account_by_id(account_id)

    def retrieve_client_account_by_id(self, account_id: int, client_id: int):
        return self.accountDao.get_account_by_id_and_client(account_id, client_id)

    def retrieve_all_accounts(self):
        return self.accountDao.get_all_accounts()

    def retrieve_all_accounts_by_client_id(self, client_id: int):
        return self.accountDao.get_accounts_by_client_id(client_id)

    def retrieve_client_accounts_within_range(self, client_id: int, lower: float or int, upper: float or int):
        return self.accountDao.get_client_accounts_within_range(client_id, lower, upper)

    def update_account(self, account: Account):
        return self.accountDao.update_account(account)

    def delete_account(self, account_id: int):
        return self.accountDao.delete_account(account_id)
