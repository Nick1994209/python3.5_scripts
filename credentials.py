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
    def get_credentials_by_key(cls, key):
        return cls.get_all_credentials().get(key)

    @classmethod
    def add_credentials(cls, key, credentials):
        my_credentials = cls.get_all_credentials()
        my_credentials[key] = credentials

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
        credentials = cls.get_credentials_by_key(cls.key)
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
        credentials = cls.get_credentials_by_key(cls.key)
        if not credentials:
            raise GetCredentialsException('Need set yandex translator api credentials: '
                                          'YandexTranslatorAPICredential.set_credentials(api_key)'
                                          'https://translate.yandex.ru/developers/keys')
        return credentials


class GoogleServicesCredential(Credential):
    key = 'google-services'

    @classmethod
    def set_credentials(cls, username, password):
        cls.add_credentials(cls.key, {'username': username, 'password': password})

    @classmethod
    def get_credentials(cls):
        credentials = cls.get_credentials_by_key(cls.key)
        if not credentials:
            raise GetCredentialsException('GoogleServicesCredential.set_credentials(api_key)')
        return credentials


class SmartreadingCredential(Credential):
    key = 'smartreading'

    @classmethod
    def set_creadentials(cls, raw_cookie: str):
        # raw_cookie got from browser document.script
        cookie = {c.split('=')[0]: c.split('=')[1] for c in raw_cookie.split('; ')}
        cls.add_credentials('smartreading', cookie)


class GetCredentialsException(Exception):
    pass


# if __name__ == '__main__':
#     Credential.add_credentials('Vasya', {'Yot': 'Mot'})
#     CourseraCredential.set_credentials('Example', 12331)
#     YandexTranslatorAPICredential.set_credentials('my_api_key')
