from abc import ABC, abstractmethod

from entities.account import Account


class AccountServices(ABC):
    @abstractmethod
    def add_account(self, account: Account):
        pass

    @abstractmethod
    def retrieve_account_by_id(self, account_id: int):
        pass

    @abstractmethod
    def retrieve_all_accounts(self):
        pass

    @abstractmethod
    def retrieve_all_accounts_by_client_id(self, client_id: int):
        pass

    @abstractmethod
    def retrieve_client_account_by_id(self, account_id: int, client_id: int):
        pass

    @abstractmethod
    def retrieve_client_accounts_within_range(self, client_id: int, lower: float or int, upper: float or int):
        pass

    @abstractmethod
    def update_account(self, account: Account):
        pass

    @abstractmethod
    def delete_account(self, account_id: int):
        pass
