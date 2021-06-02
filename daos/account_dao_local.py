from daos.account_dao import AccountDAO
from entities.account import Account
from exceptions.account_not_found_error import AccountNotFoundError
from exceptions.overdraft_exception import OverDraftError


class AccountDAOLocal(AccountDAO):
    id_generator = 0
    localAccount = {}

    def create_account(self, account: Account) -> Account:
        # 1) create account and return
        AccountDAOLocal.id_generator += 1
        account.account_id = AccountDAOLocal.id_generator
        AccountDAOLocal.localAccount[AccountDAOLocal.id_generator] = account
        return AccountDAOLocal.localAccount[AccountDAOLocal.id_generator]

    def get_all_accounts(self) -> list[Account]:
        # just return all users
        return list(AccountDAOLocal.localAccount.values())

    def get_account_by_id(self, account_id: int) -> Account:
        # 1) if the account ID in input argument doesn't exist, raise exception
        account = AccountDAOLocal.localAccount.get(account_id)
        if account is None:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found.')

        # 2) otherwise return the account found
        return account

    def get_accounts_by_client_id(self, client_id: int) -> list[Account]:
        # 1) look for account and return
        data = AccountDAOLocal.localAccount.values()
        accounts = [account for account in data if account.client_id == client_id]
        return accounts

    def get_client_accounts_within_range(self, client_id: int, lower: int, upper: int) -> list[Account]:
        # 1) look for account and return
        data = AccountDAOLocal.localAccount.values()
        accounts = [account for account in data if account.client_id == client_id and lower <= account.balance <= upper]
        return accounts

    def get_account_by_id_and_client(self, account_id: int, client_id: int) -> Account:
        # 1) look for account id
        acct = AccountDAOLocal.localAccount.get(account_id)
        # 2) if the account does NOT belong to user with input id, raise exception
        if acct is None or acct.client_id != client_id:
            raise AccountNotFoundError(f'The account with id: {account_id} and client_id: {client_id} could not be found. Account could not be retrieved.')
        return acct

    def update_account(self, account: Account) -> Account:
        # 1) search if account with corresponding id to input account exists
        old_acct = AccountDAOLocal.localAccount.get(account.account_id)
        if old_acct is None:
            raise AccountNotFoundError(
                f'Account with id: {account.account_id} was not found, account could not be updated.')

        # 2) replace the account in memory with new account
        AccountDAOLocal.localAccount[account.account_id] = account

        # 3) return the account just replaced to confirm successful update
        return AccountDAOLocal.localAccount[account.account_id]

    def update_account_balance(self, account_id: int, client_id: int, transaction_type: str, amount: float or int) -> Account:
        # 1) look for account
        data = AccountDAOLocal.localAccount.values()
        accounts: list[Account] = [account for account in data if account.client_id == client_id and account.account_id == account_id]

        # 2) if no account found, raise error
        if len(accounts) == 0:
            raise AccountNotFoundError(f'The account with id: {account_id} and client_id: {client_id} could not be found. Account could not be retrieved.')

        # 3) perform transaction
        if transaction_type == 'withdraw':
            amount *= -1

        temp_balance = accounts[0].balance
        temp_balance += amount

        # 4) check if account is negative, if negative, raise overdraft error
        if temp_balance < 0:
            raise OverDraftError(f'The account with id: {account_id} has insufficient funds, the transaction was '
                                 f'cancelled.')

        # 5) if valid, then replace in memory and return
        accounts[0].balance += amount
        AccountDAOLocal.localAccount[accounts[0].account_id] = accounts[0]
        return accounts[0]

    def update_account_by_client_id(self, account_id: int, client_id: int, account: Account) -> Account:
        # 1) find the account, raise error if no account exists
        acct = AccountDAOLocal.localAccount.get(account_id)
        if acct is None or acct.client_id != client_id:
            raise AccountNotFoundError(
                f'The account with id: {account_id} and client_id: {client_id} could not be found. Account could not be updated.')

        # 2) make changes and update, store in memory then return
        account.account_id = account_id
        account.client_id = client_id
        AccountDAOLocal.localAccount[account_id] = account
        return acct

    def delete_account(self, account_id: int) -> bool:
        # 1) check if account with input id exists
        acct = AccountDAOLocal.localAccount.get(account_id)
        if acct is None:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found, account could not be deleted.')

        # 2) delete account
        del AccountDAOLocal.localAccount[account_id]
        return True

    def delete_account_by_id_and_client_id(self, account_id: int, client_id: int) -> bool:
        # 1) look for account id
        acct = AccountDAOLocal.localAccount.get(account_id)
        # 2) if the account does NOT belong to user with input id, raise exception
        if acct is None or acct.client_id != client_id:
            raise AccountNotFoundError(
                f'The account with id: {account_id} and client_id: {client_id} could not be found. Account could not be deleted.')
        del AccountDAOLocal.localAccount[account_id]
        return True

    def delete_all_accounts_by_client_id(self, client_id: int) -> int:
        # 1) look for all accounts with client_id
        data = AccountDAOLocal.localAccount.values()
        accounts = [account for account in data if account.client_id == client_id]

        # 2) remove them each from memory
        if len(accounts) == 1:
            del AccountDAOLocal.localAccount[accounts[0].account_id]
            return 1

        deleted_count = 0
        for acct in accounts:
            del AccountDAOLocal.localAccount[acct.account_id]
            deleted_count += 1

        # return a count of number of entries deleted
        return deleted_count
