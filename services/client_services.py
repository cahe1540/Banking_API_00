from abc import ABC, abstractmethod

from entities.client import Client


class ClientServices(ABC):
    @abstractmethod
    def add_client(self, client: Client):
        pass

    @abstractmethod
    def retrieve_client_by_id(self, client_id: int):
        pass

    @abstractmethod
    def retrieve_all_clients(self):
        pass

    @abstractmethod
    def update_client(self, client: Client):
        pass

    @abstractmethod
    def delete_client(self, client_id: int):
        pass
