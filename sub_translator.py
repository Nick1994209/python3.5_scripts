from credentials import YandexTranslatorAPICredential
from translator import YandexTranslator

with open('01_non-linear-hypotheses.en.srt') as file_:
    # print(file_.read())
    translator = YandexTranslator(YandexTranslatorAPICredential.get_credentials())
    ru_srt = translator.translate_text(str(file_.read().split('\n')[2]))

print(ru_srt)
with open('01_non-linear-hypotheses.ru.srt', 'w') as file_:
    file_.write(ru_srt)
