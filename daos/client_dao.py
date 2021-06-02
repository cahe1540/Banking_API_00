from abc import ABC, abstractmethod
from entities.client import Client


class ClientDAO(ABC):

    # Create
    @abstractmethod
    def create_client(self, client: Client) -> Client:
        pass

    # Read
    @abstractmethod
    def get_all_clients(self) -> list[Client]:
        pass

    @abstractmethod
    def get_client_by_Id(self, client_id: int) -> Client:
        pass

    # Update
    @abstractmethod
    def update_client(self, client: Client) -> Client:
        pass

    # Delete
    @abstractmethod
    def delete_client(self, client_id: int) -> bool:
        pass
