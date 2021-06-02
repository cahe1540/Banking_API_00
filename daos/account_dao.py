from abc import ABC, abstractmethod
from entities.account import Account


class AccountDAO(ABC):

    # Create
    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    # Read
    @abstractmethod
    def get_all_accounts(self) -> list[Account]:
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_accounts_by_client_id(self, client_id: int) -> list[Account]:
        pass

    @abstractmethod
    def get_client_accounts_within_range(self, client_id: int, lower: int, upper: int) -> list[Account]:
        pass

    @abstractmethod
    def get_account_by_id_and_client(self, account_id: int, client_id: int) -> Account:
        pass

    @abstractmethod
    def update_account_by_client_id(self, account_id: int, client_id: int, account: Account) -> Account:
        pass

    # Update
    @abstractmethod
    def update_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def update_account_balance(self, account_id: int, client_id: int, transaction_type: str, amount: float) -> Account:
        pass

    # Delete
    @abstractmethod
    def delete_account(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def delete_account_by_id_and_client_id(self, account_id: int, client_id: float or int):
        pass

    @abstractmethod
    def delete_all_accounts_by_client_id(self, client_id: int):
        pass