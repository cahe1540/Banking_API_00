from daos.client_dao import ClientDAO
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from exceptions.client_not_found_error import ClientNotFoundError

# test data
client1: Client = Client(0, 'Carlos', 'Herrera')
client2: Client = Client(0, 'Sarah', 'Connor')
client3: Client = Client(0, 'Flor', 'Anastasia')
get_client: Client = Client(7, 'Rick', 'Morty')
client2_update: Client = Client(6, 'Xena', 'Hercules')
update_fail: Client = Client(222, 'A', 'B')

# test Dao
clientDao: ClientDAO = ClientDAOPostgres()


def test_create_client():
    clientDao.create_client(client1)
    clientDao.create_client(client3)
    result = clientDao.create_client(client2)
    assert type(result.client_id) == int


def test_get_client_by_id():
    test_num = 7
    result = clientDao.get_client_by_Id(test_num)
    assert str(result) == str(get_client)


def test_get_by_id_fail():
    test_num = 22222
    try:
        result = clientDao.get_client_by_Id(test_num)
        assert False
    except ClientNotFoundError as e:
        assert str(e) == f'User with id: {test_num} was not found.'


def test_update_acct():
    result = clientDao.update_client(client2_update)
    assert str(result) == str(client2_update)


def test_fail_update_acct():
    try:
        result = clientDao.update_client(update_fail)
        assert False
    except ClientNotFoundError as e:
        assert str(
            e) == f'Client with id: {update_fail.client_id} was not found.'


def test_delete_acct():
    test_num = 8
    result = clientDao.delete_client(test_num)
    assert result


def test_fail_delete_acct():
    test_num = 444
    try:
        clientDao.delete_client(test_num)
        assert False
    except ClientNotFoundError as e:
        assert str(e) == f'Client with id: {test_num} was not found, client could not be deleted.'


def test_get_all_users():
    client3: Client = Client(0, 'George', 'Bezos')
    client4: Client = Client(0, 'Annai', 'Dogao')
    clientDao.create_client(client3)
    clientDao.create_client(client4)
    all_clients = clientDao.get_all_clients()
    assert len(all_clients) >= 2

