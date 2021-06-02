from services.client_services import ClientServices
from entities.client import Client
from daos.client_dao import ClientDAO


class ClientServicesImpl(ClientServices):
    def __init__(self, clientDao: ClientDAO, **kwargs):
        super().__init__(**kwargs)
        self.clientDao = clientDao

    def add_client(self, client: Client):
        return self.clientDao.create_client(client)

    def retrieve_client_by_id(self, client_id: int):
        return self.clientDao.get_client_by_Id(client_id)

    def retrieve_all_clients(self):
        return self.clientDao.get_all_clients()

    def update_client(self, client: Client):
        return self.clientDao.update_client(client)

    def delete_client(self, client_id: int):
        return self.clientDao.delete_client(client_id)