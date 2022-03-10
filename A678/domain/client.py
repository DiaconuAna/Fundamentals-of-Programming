
class ClientException(Exception):
    def __init__(self, msg = ''):
        self._msg = msg


class ClientValidationException(ClientException):
    def __init__(self, error_list):
        self._errors = error_list

    @property
    def errors(self):
        return self._errors

    def __str__(self):
        result = ''
        for e in self.errors:
            result += e
            result += '\n'
        return result


class Client:
    def __init__(self, client_id, name):
        self._client_id = client_id
        self._name = name

    def __str__(self):
        return str(self._client_id).rjust(2) + ': ' + str(self._name)

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class ClientValidator:
    def validate(self, client):
        """
        Validate the input data for a given client object
        :param client: -
        :return: -
        """
        errors = []
        tmp_id = client.client_id[1:]

        if len(client.name) == 0 or client.name == ' ':
            errors.append("Invalid name, your client is a Jane Doe...")
        l = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for index in range(len(l)):
            if l[index] in client.name:
                errors.append("Name should only contain letters!")

        if len(client.name) > 0:
            if len(client.client_id) != 5 or client.client_id[0].lower() != client.name[0].lower() or not tmp_id.isdigit():
                errors.append("Invalid client id provided. Input id of form first_letter_name abcd, where a,b,c,d are digits.")

        if len(errors) != 0:
            raise ClientValidationException(errors)



