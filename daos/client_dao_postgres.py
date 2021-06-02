from daos.client_dao import ClientDAO
from entities.client import Client
from psycopg2._psycopg import ProgrammingError

from exceptions.client_not_found_error import ClientNotFoundError
from utils.connection import connection


class ClientDAOPostgres(ClientDAO):
    def create_client(self, client: Client) -> Client:
        # 1) just create client, can only fail if db fails
        sql = """insert into client (first_name, last_name) values (%s, %s) returning client_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (client.first_name, client.last_name))
        connection.commit()
        c_id = cursor.fetchone()[0]
        client.client_id = c_id
        return client

    def get_all_clients(self) -> list[Client]:
        # 1) get all clients
        sql = """select * from client"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        result = [Client(*record) for record in records]
        # 2) return
        return result

    def get_client_by_Id(self, client_id: int) -> Client:
        # 1) search for client if the client id in input argument doesn't exist, raise exception
        sql = """select * from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (client_id,))
        record = cursor.fetchone()
        if record is None:
            raise ClientNotFoundError(f'User with id: {client_id} was not found.')

        # 2) otherwise return the account found
        client = Client(*record)
        return client

    def update_client(self, client: Client) -> Client:
        # 1) attempt to update
        try:
            sql = """update client set first_name = %s, last_name = %s where client_id = %s returning *"""
            cursor = connection.cursor()
            cursor.execute(sql, (client.first_name, client.last_name, client.client_id))
            result = cursor.fetchone()
            connection.commit()
            client.client_id = result[0]
            return client
        # 2) raise ClientNotFoundError not present if fail
        except TypeError:
            raise ClientNotFoundError(f'Client with id: {client.client_id} was not found.')
        except ProgrammingError:
            raise ClientNotFoundError(f'Client with id: {client.client_id} was not found.')

    def delete_client(self, client_id: int) -> bool:
        # 1) search if client exists, raise exception if not
        try:
            sql = """delete from client where client_id = %s returning *"""
            cursor = connection.cursor()
            cursor.execute(sql, (client_id,))
            cursor.fetchone()[0]
            connection.commit()
            return True
        # 2) raise ClientNotFoundError not present if fail
        except TypeError:
            raise ClientNotFoundError(f'Client with id: {client_id} was not found, client could not be deleted.')
        except ProgrammingError:
            raise ClientNotFoundError(f'Client with id: {client_id} was not found, client could not be deleted.')
