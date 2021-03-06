import requests
from furl import furl

STATUS_SUCCESS = 200


class YandexTranslator:
    api = 'https://translate.yandex.net/api/v1.5/tr.json/'
    MAX_COUNT_TEXTS = 100  # max count texts in list can be translate free

    def __init__(self, api_key):
        """
        :param api_key: api key from https://translate.yandex.ru/developers/keys
        """
        self.api_key = api_key

    def get_language(self, text):
        """
            https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
            :param text: need translate text
            :param language: "ru" if need translate to russian language
                             "fr-ru" if need translate french language to russian 
            :return: translated text
            """
        args = {
            'text': text,
            'key': self.api_key
        }
        response = requests.post(self.get_api('detect', args))
        if not response.status_code == STATUS_SUCCESS:
            raise Exception(response.json())  # TODO
        return response.json()['lang']

    def translate_text(self, text, language):
        """
        https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
        :param text: need translate text
        :param language: "ru" if need translate to russian language
                         "fr-ru" if need translate french language to russian 
        :return: translated text
        """
        return text
        args = {
            'text': text,
            'key': self.api_key,
            'lang': language
        }
        response = requests.post(self.get_api('translate', args))
        if not response.status_code == STATUS_SUCCESS:
            raise Exception(response.json())  # TODO
        return response.json()['text']

    def translate_with_detect_language(self, text, language_to):
        language_from = self.get_language(text)
        return self.translate_text(text, language_from + '-' + language_to)

    def get_api(self, path, arguments):
        api = furl(self.api)
        api.add(path=path, args=arguments)
        return api.url


if __name__ == '__main__':
    from credentials import YandexTranslatorAPICredential
    translator = YandexTranslator(YandexTranslatorAPICredential.get_credentials())
    print(translator.get_language('hell'))
    print(translator.translate_text('un de mes amis', 'ru'))
