from abc import ABC, abstractmethod
from entities.client import Client
from entities.account import Account


# certain operations MUST make changes in both DAOs
# these operations will go in BankServices
class BankServices(ABC):

    @abstractmethod
    def create_account_for_client(self, client_id: int, account: Account):
        pass

    @abstractmethod
    def retrieve_all_clients_accounts(self, client_id: int):
        pass

    @abstractmethod
    def update_clients_account_by_account_id(self, client_id: int, user_id: int, data: dict):
        pass

    @abstractmethod
    def withdraw_or_deposit(self, account_id: int, client_id: int, transaction_type: str, amount: float) -> Account:
        pass

    @abstractmethod
    def transfer_clients_funds(self, client_id: int, amount: int, acct_from_id: int, acct_to_id: int):
        pass

    @abstractmethod
    def delete_client_by_id(self, client_id: int):
        pass

    @abstractmethod
    def delete_account_by_client_id(self, client_id: int, account_id: int):
        pass
