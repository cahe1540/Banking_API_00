from daos.account_dao import AccountDAO
from entities.account import Account
from exceptions.account_not_found_error import AccountNotFoundError
from exceptions.overdraft_exception import OverDraftError
import psycopg2
from psycopg2._psycopg import ProgrammingError
from utils.connection import connection


class AccountDAOPostgres(AccountDAO):

    def create_account(self, account: Account) -> Account:
        try:
            # 1) just create account, can only fail if db fails
            sql = """insert into account (account_type, balance, client_id) values (%s, %s, %s) returning account_id"""
            cursor = connection.cursor()
            cursor.execute(sql, (account.account_type, account.balance, account.client_id))
            connection.commit()
            a_id = cursor.fetchone()[0]
            account.account_id = a_id
            return account
        except psycopg2.errors.CheckViolation as e:
            connection.rollback()
            raise OverDraftError(f'Invalid balance amount. Can not create the account.')

    def get_all_accounts(self) -> list[Account]:
        # 1) get all accounts
        sql = """select * from account"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        results = [Account(record[0], record[1], float(record[2]), record[3]) for record in records]
        # 2) return
        return results

    def get_account_by_id(self, account_id: int) -> Account:
        # 1) search for client if the client id in input argument doesn't exist, raise exception
        sql = """select * from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (account_id,))
        record = cursor.fetchone()
        if record is None:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found.')
        # 2) otherwise return the account found
        account = Account(record[0], record[1], float(record[2]), record[3])
        return account

    def get_accounts_by_client_id(self, client_id: int) -> list[Account]:
        # 1) search for client if the client id in input argument doesn't exist, raise exception
        sql = """select * from account where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (client_id,))
        records = cursor.fetchall()
        if records is None:
            raise AccountNotFoundError(f'Account with id: {client_id} was not found.')

        accounts = [Account(record[0], record[1], float(record[2]), record[3]) for record in records]
        # 2) otherwise return the account found
        return accounts

    def get_client_accounts_within_range(self, client_id: int, lower: int, upper: int) -> list[Account]:
        # 1) search for client if the client id in input argument doesn't exist, raise exception
        sql = """select * from account where client_id = %s and account.balance >= %s and account.balance <= %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (client_id, lower, upper))
        records = cursor.fetchall()
        if records is None:
            raise AccountNotFoundError(f'Account with id: {client_id} was not found.')

        accounts = [Account(record[0], record[1], float(record[2]), record[3]) for record in records]
        # 2) otherwise return the account found
        return accounts

    def get_account_by_id_and_client(self, account_id: int, client_id: int) -> Account:
        # 1) search for client if the client id in input argument doesn't exist, raise exception
        sql = """select * from account where account_id = %s and client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (account_id, client_id))
        record = cursor.fetchone()
        if record is None:
            raise AccountNotFoundError(f'Account with id: {account_id} and client_id: {client_id} was not found.')

        # 2) otherwise return the account found
        account = Account(record[0], record[1], float(record[2]), record[3])
        return account

    def update_account(self, account: Account) -> Account:
        # 1) attempt to update
        try:
            sql = """update account set account_type = %s, balance = %s, client_id = %s where account_id = %s returning *"""
            cursor = connection.cursor()
            cursor.execute(sql, (account.account_type, account.balance, account.client_id, account.account_id))
            result = cursor.fetchone()
            connection.commit()
            account.account_id = result[0]
            return account
        # 2) raise AccountNotFoundError not present if fail
        except psycopg2.errors.CheckViolation as e:
            connection.rollback()
            raise OverDraftError(f'Invalid balance amount. Can not create the account.')
        except TypeError:
            raise AccountNotFoundError(f'Account with id: {account.account_id} was not found.')
        except ProgrammingError:
            raise AccountNotFoundError(f'Account with id: {account.account_id} was not found.')

    def update_account_balance(self, account_id: int, client_id: int, transaction_type: str,
                               amount: float or int) -> Account:
        if transaction_type == "withdraw":
            amount *= -1
        # 1) attempt to update
        try:
            sql = """update account set balance = balance + %s where client_id = %s and account_id = %s returning *"""
            cursor = connection.cursor()
            cursor.execute(sql, (amount, client_id, account_id))
            result = cursor.fetchone()
            connection.commit()
            account = Account(result[0], result[1], float(result[2]), result[3])
            return account
        # 2) raise AccountNotFoundError not present if fail
        except psycopg2.errors.CheckViolation as e:
            connection.rollback()
            raise OverDraftError(f'Account with id: {account_id} has insufficient funds, the transaction was cancelled.')
        except TypeError:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found.')
        except ProgrammingError:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found.')

    def update_account_by_client_id(self, account_id: int, client_id: int, account: Account) -> Account:
        # 1) attempt to update
        try:
            sql = """update account set account_type = %s, balance = %s, client_id = %s where account_id = %s and client_id = %sreturning *"""
            cursor = connection.cursor()
            cursor.execute(sql,
                           (account.account_type, account.balance, account.client_id, account.account_id, client_id))
            result = cursor.fetchone()
            connection.commit()
            account.account_id = result[0]
            return account
        # invalid balance amount
        except psycopg2.errors.CheckViolation as e:
            connection.rollback()
            raise OverDraftError(
                f'Invalid balance amount. Can not create the account.')
        # 2) raise AccountNotFoundError not present if fail
        except TypeError:
            raise AccountNotFoundError(f'Account with id: {account.account_id} was not found.')
        except ProgrammingError:
            raise AccountNotFoundError(f'Account with id: {account.account_id} was not found.')

    def delete_account(self, account_id: int) -> bool:
        # 1) search if client exists, raise exception if not
        try:
            sql = """delete from account where account_id = %s returning *"""
            cursor = connection.cursor()
            cursor.execute(sql, (account_id,))
            cursor.fetchone()[0]  # this is meant to raise typeErrors
            connection.commit()
            return True
        # 2) raise AccountNotFoundError not present if fail
        except TypeError:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found.')
        except ProgrammingError:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found.')

    def delete_account_by_id_and_client_id(self, account_id: int, client_id: int) -> bool:
        # 1) try to delete
        try:
            sql = """delete from account where account_id = %s and client_id = %s returning *"""
            cursor = connection.cursor()
            cursor.execute(sql, (account_id, client_id))
            cursor.fetchone()[0]
            connection.commit()
            return True
        # 2) raise AccountNotFoundError not present if fail
        except TypeError:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found.')
        except ProgrammingError:
            raise AccountNotFoundError(f'Account with id: {account_id} was not found.')

    def delete_all_accounts_by_client_id(self, client_id: int) -> int:
        sql = """delete from account where client_id = %s returning *"""
        cursor = connection.cursor()
        cursor.execute(sql, (client_id,))
        result = cursor.fetchall()
        connection.commit()
        return len(result)
