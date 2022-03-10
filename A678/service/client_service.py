from domain.client import Client, ClientValidator, ClientException
from service.undo_service import FunctionCall, Operation, CascadedOperation


class ClientService:
    def __init__(self, client_repo, rental_service, undo_service):
        self._clients_list = client_repo
        self._rental_service = rental_service
        self._undo_service = undo_service

    @property
    def client_repo(self):
        return self._clients_list

    def find_client(self, data):
        """
        Finds whether a client is in the list or not based on the given data
        :param data:
        :return: client's index
        """
        for index in range(len(self._clients_list.clients)):
            client = self._clients_list.clients[index]
            if data == client.client_id or data.lower() == client.name.lower():
                return index
        return -1

    def add_client(self, client_id, name):
        client = Client(client_id, name)
        c1 = ClientValidator()
        c1.validate(client)
        client_list = self._clients_list.clients

        for c in range(len(client_list)):
            client1 = client_list[c]
            if client.client_id == client1.client_id:
                raise ClientException("Two clients cannot have the same id")

        self._clients_list.add_client(client)

        undo = FunctionCall(self._clients_list.remove_client_object, client )
        redo = FunctionCall(self._clients_list.add_client, client)
        operation = Operation(undo, redo)
        self._undo_service.add_operation(operation)

    def remove_client(self, data):
        client_index = self.find_client(data)
        if client_index != -1:
            client = self._clients_list.clients[client_index]

            self._clients_list.remove_client_object(client)
            undo = FunctionCall(self._clients_list.add_client, client)
            redo = FunctionCall(self._clients_list.remove_client_object, client)
            operation = Operation(undo, redo)
            #self._undo_service.add_operation(operation)
            cascade_list = [operation]

            rental_list = self._rental_service.filter_clients(client.client_id)
            if len(rental_list) != 0:
                for rent in rental_list:
                    self._rental_service.delete_rental(rent.rental_id)
                    undo = FunctionCall(self._rental_service._rentals_list.add_rental, rent)
                    redo = FunctionCall(self._rental_service._rentals_list.remove_rental, rent)
                    cascade_list.append(Operation(undo, redo))

            cop = CascadedOperation(*cascade_list)
            self._undo_service.add_operation(cop)
        else:
            raise ClientException("Invalid data given. No client could be removed.")

    def update_client(self, data, update_info, update_id):
        client_index = self.find_client(data)
        client = self._clients_list.clients[client_index]
        if client_index == -1:
            raise ClientException("Invalid data given. No client could be updated.")
        if update_id == '1':
            initial_data = client.client_id
            rental_list = self._rental_service.rental_list
            for rental in rental_list:
                if rental.client_id == client.client_id:
                    self._rental_service.update_rental(rental.rental_id, update_info, '2')

        if update_id == '2':
            initial_data = client.name

        updated_client = self._clients_list.update_client(client, update_info, update_id)
        undo = FunctionCall(self._clients_list.update_client, updated_client, initial_data, update_id)
        redo = FunctionCall(self._clients_list.update_client, client, update_info, update_id)
        operation = Operation(undo, redo)
        self._undo_service.add_operation(operation)

    def list_clients(self, print_list):
        self._clients_list.list(print_list)

    def generate_list(self, length):
        self._clients_list.generate_list(length)

    def get_list(self):
        return self._clients_list.clients

    def get_client(self, data):
        """
        Find client by given data
        :param data:
        :return:
        """
        index = self.find_client(data)
        if index == -1:
            raise ClientException("Client could not be found.")
        return self._clients_list.clients[index]

    def search_client(self, data, search_list):
        """
        Search for clients using any one of their fields (client_id, name).
        The search must work using case-insensitive, partial string matching, and must return all matching items.
        :param data:
        :param search_list:
        :return:
        """
        self.search_by_id(data, search_list)
        self.search_by_name(data, search_list)

        if len(search_list) == 0:
            raise ClientException("No matches for the given data!")

    def search_by_id(self, data, search_list):
        """
        Search a client by id and return all partial matches
        :param data:
        :param search_list:
        :return:
        """
        client_list = self.client_repo.clients
        for index in range(len(client_list)):
            client = client_list[index]
            if data.lower() in client.client_id.lower():
                search_list.append(client)

    def search_by_name(self, data, search_list):
        """
        Search a client by name and return all partial matches
        :param data:
        :param search_list:
        :return:
        """
        client_list = self.client_repo.clients
        for index in range(len(client_list)):
            client = client_list[index]
            if data.lower() in client.name.lower():
                search_list.append(client)

