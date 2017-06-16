import json
import os

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)


class Credential:
    credentials_file = os.path.join(dir_path, 'credentials.json')

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
    key = 'coursera'

    @classmethod
    def set_credentials(cls, username, password):
        credentials = {
            'username': username,
            'password': str(password)
        }
        cls.add_credentials(cls.key, credentials)

    @classmethod
    def get_credentials(cls):
        credentials = cls.get_all_credentials().get(cls.key)
        if not credentials:
            raise GetCredentialsException('Need set coursera credentials: '
                                          'CourseraCredential.set_credentials(login, password)'
                                          'https://www.coursera.org/')
        return credentials


class YandexTranslatorAPICredential(Credential):
    key = 'yandex_translator_api'

    @classmethod
    def set_credentials(cls, api_key):
        cls.add_credentials(cls.key, api_key)

    @classmethod
    def get_credentials(cls):
        credentials = cls.get_all_credentials().get(cls.key)
        if not credentials:
            raise GetCredentialsException('Need set yandex translator api credentials: '
                                          'YandexTranslatorAPICredential.set_credentials(api_key)'
                                          'https://translate.yandex.ru/developers/keys')
        return credentials


class GetCredentialsException(Exception):
    pass


# if __name__ == '__main__':
#     Credential.add_credentials('Vasya', {'Yot': 'Mot'})
#     CourseraCredential.set_credentials('Example', 12331)
#     YandexTranslatorAPICredential.set_credentials('my_api_key')
