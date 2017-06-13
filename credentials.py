import json


class Credential:
    credentials_file = 'credentials.json'

    @classmethod
    def get_all_credentials(cls):
        try:
            with open(cls.credentials_file) as file_:
                return json.loads(file_.read())
        except FileNotFoundError:
            return {}

    @classmethod
    def add_credentials(cls, key, dict_credentials):
        my_credentials = cls.get_all_credentials()
        my_credentials[key] = dict_credentials

        with open(cls.credentials_file, 'w') as file_:
            file_.write(json.dumps(my_credentials, indent=3))


class CourseraCredential(Credential):
    @classmethod
    def set_credentials(cls, username, password):
        credentials = {
            'username': username,
            'password': str(password)
        }
        cls.add_credentials('coursera', credentials)

    @classmethod
    def get_credentials(cls):
        credentials = cls.get_all_credentials().get('coursera')
        if not credentials:
            raise GetCredentialsException('Need set coursera credentials: '
                                          'CourseraCredential.set_credentials(login, password)')
        return credentials


class GetCredentialsException(Exception):
    pass


if __name__ == '__main__':
    Credential.add_credentials('Vasya', {'Yot': 'Mot'})
    CourseraCredential.set_credentials('Example', 12331)
