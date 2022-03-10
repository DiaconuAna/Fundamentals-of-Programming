"""
The user can add, remove, update, and list clients
Client: client_id, name
"""
from random import randrange, choice

from domain.client import Client, ClientValidationException, ClientException, ClientValidator


class ClientRepository:
    def __init__(self):
        self._client_list = []

    def __len__(self):
        return len(self._client_list)

    def get_last_client(self):
        return self._client_list[-1]

    @property
    def clients(self):
        return self._client_list

    def add_client(self, client):
        """
        Adds a client to the list if its id is not in the list already
        :param client:
        :return:
        """

        self._client_list.append(client)

    def remove_client_object(self, client):
        """

        :param client:
        :return:
        """
        self._client_list.remove(client)
        return client

    def update_client(self, client, update_info, update_id):
        """
        One can update all of client's parameters: client_id, name
        The client the user wants to update the info for is found based on the client_data given
        If several clients have the same name, only the first occurrence is updated
        IMPORTANT: If I change a client's name, the id also needs to be changed so that the first letter of the new name
                   will be in it
        :param client: Used to identify the client we want to update
        :param update_info: Client's new info
        :param update_id: 1 if client_id, 2 if name
        :return:
        """
        c1 = ClientValidator()
        client_index = self.find_client_index(client)

        if update_id == '1':
            client.client_id = update_info
            c1.validate(client)
            self._client_list[client_index].client_id = update_info
        elif update_id == '2':
            aux = client.client_id[1:]
            client.client_id = aux
            client.client_id = update_info[0] + client.client_id
            client.name = update_info
            c1.validate(client)
            self._client_list[client_index].client_id = self._client_list[client_index].client_id[1:]
            self._client_list[client_index].client_id = update_info[0] + self._client_list[client_index].client_id
            self._client_list[client_index].name = update_info

        return client

    def find_client_index(self, client):
        """
        Returns the index of a client if it's in the list
        :param client:
        :return: -1 if client is not in the list
        """
        for index in range(len(self._client_list)):
            c1 = self._client_list[index]
            if client.client_id == c1.client_id:
                return index

    def list(self, print_list):
        """

        :return:
        """
        for index in range(len(self)):
            print_list.append(self._client_list[index])

    def generate_list(self, length):
        """
        Generate first 10 elements from a list
        Convention: client_id is of form first_name_letter + 4 digits
        Name is a string of letters
        :return:
        """

        first_name = ['Anna', 'Linda', 'Chloe', 'Jackson', 'Bill', 'John', 'Sarah', 'Jordan', 'Rose', 'Strip', 'Sasha',
                      'Aliona', 'Michael', 'Nathan', 'Brian', 'Frances', 'Leah', 'Fred', 'George', 'Harry', 'Jane']
        last_name = ['Larson', 'McLachlan', 'Smith', 'Jefferson', 'Goodwin', 'Harding', 'Price', 'White', 'Johnson',
                     'Kay', 'Harper', 'Thomson', 'Gardner', 'Dean', 'Hamilton', 'Murray']

        for i in range(10):
            id_ = str(randrange(1000, 9999))
            name = choice(first_name) + ' ' + choice(last_name)
            client_id = name[0] + id_
            client = Client(client_id, name)
            self.add_client(client)

