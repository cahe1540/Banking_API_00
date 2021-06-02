from daos.client_dao import ClientDAO
from entities.client import Client

from exceptions.client_not_found_error import ClientNotFoundError


class ClientDAOLocal(ClientDAO):
    id_generator = 0
    localClient = {}

    def create_client(self, client: Client) -> Client:
        # 1) just create client, can only fail if db fails
        ClientDAOLocal.id_generator += 1
        client.client_id = ClientDAOLocal.id_generator
        ClientDAOLocal.localClient[ClientDAOLocal.id_generator] = client
        return client

    def get_all_clients(self) -> list[Client]:
        return list(ClientDAOLocal.localClient.values())

    def get_client_by_Id(self, user_id: int) -> Client:
        # 1) if the account id in input argument doesn't exist, raise exception
        user = ClientDAOLocal.localClient.get(user_id)
        if user is None:
            raise ClientNotFoundError(f'User with id: {user_id} was not found.')

        # 2) otherwise return the account found
        return user

    def update_client(self, client: Client) -> Client:
        # 1) search if client exists
        old_client = ClientDAOLocal.localClient.get(client.client_id)
        if old_client is None:
            raise ClientNotFoundError(
                f'Client with id: {client.client_id} was not found, client information could not be updated.')

        # 2) replace the client in memory with new client data
        ClientDAOLocal.localClient[client.client_id] = client

        # 3) return the account just replaced to confirm successful update
        return ClientDAOLocal.localClient[client.client_id]

    def delete_client(self, client_id: int) -> bool:
        # 1) search if client exists
        old_client = ClientDAOLocal.localClient.get(client_id)
        if old_client is None:
            raise ClientNotFoundError(
                f'Client with id: {client_id} was not found, client could not be deleted.')

        # 2) # delete the client from memory
        del ClientDAOLocal.localClient[client_id]

        # 3) return True for success
        return True
