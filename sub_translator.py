import os
import re


class DirectoryWithSubtitlesTranslate:
    subtitles_ext = '.srt'

    def __init__(self,
                 sub_translate: 'SubtitlesTranslator().translate') -> None:
        """
        :param sub_translate: SubtitlesTranslator.translate
        """
        self.sub_translate = sub_translate

    def translate_subtitles(self, directory, translate_from, translate_to,
                            recursive=True):
        """

        :param directory: path with subtitles files
        :param translate_from: translate from language
        :param translate_to: translate to language
        :param recursive: translate all subtitles in current directory catalogs
        """
        list_files_with_directories = os.listdir(directory)

        for path in list_files_with_directories:
            path = os.path.join(directory, path)
            if os.path.isdir(path) and recursive:
                self.translate_subtitles(path, translate_from, translate_to)
            elif self.check_file_to_translate(path, translate_from,
                                              translate_to):
                self.translate_one_file(path, translate_to)

    def check_file_to_translate(self, subtitle_path, translate_from,
                                translate_to):
        if not subtitle_path.lower().endswith(
                self.generate_end_file(translate_from)):
            return False

        list_files_with_directories = os.listdir(
            os.path.dirname(subtitle_path))
        file_name = os.path.basename(subtitle_path)
        base_file = \
        file_name.lower().rsplit(self.generate_end_file(translate_from), 1)[0]
        # print(base_file)
        for path in list_files_with_directories:
            path = path.lower()
            if not path.endswith(self.generate_end_file(translate_to)):
                continue
            if path.startswith(base_file):
                return False
        return True

    def translate_one_file(self, path, translate_to):
        try:
            self.sub_translate(path, translate_to_language=translate_to)
        except Exception as e:
            print('ERROR', e, '\n\n')

    def generate_end_file(self, language):
        return language + self.subtitles_ext


class SubtitlesTranslator:
    search_translate_phrase = r'[a-zA-Z]+'

    def __init__(self, translator: 'YandexTranslator',
                 add_name_translated_file='_translated_'):
        """
        :param translator: YandexTranslator(YandexTranslatorAPICredential.get_credentials())
        :param add_name_translated_file: if subtitle been sub.en.srt => sub.translated_.ru.srt
        """
        self.translator = translator
        self.add_name_translated_file = add_name_translated_file

    def translate(self, subtitles_file_path, translate_to_language):
        subtitles_lines = self.read_file(subtitles_file_path)
        translated_lines = self.translate_lines(subtitles_lines,
                                                translate_to_language)
        new_name_subtitles = self.generate_new_name(subtitles_file_path,
                                                    translate_to_language)
        self.write_file(new_name_subtitles, translated_lines)

    @staticmethod
    def read_file(file_path):
        with open(file_path) as file_:
            return list(file_.readlines())

    def translate_lines(self, subtitles_lines, translate_to_language):
        need_translate_lines = self.search_indexes_lines_for_translate(
            subtitles_lines)
        phrases = [line for index, line in enumerate(subtitles_lines)
                   if index in need_translate_lines]
        translated_phrases = self.translate_phrases(phrases,
                                                    translate_to_language)
        for index_translated_line, index_subtitle_line in enumerate(
                need_translate_lines):
            subtitles_lines[index_subtitle_line] = translated_phrases[
                index_translated_line]
        return subtitles_lines

    def search_indexes_lines_for_translate(self, lines):
        indexes_lines = []
        for index, line in enumerate(lines):
            if re.search(self.search_translate_phrase, line):
                indexes_lines.append(index)
        return indexes_lines

    def translate_phrases(self, phrases, translate_to_language):
        limit_count_translate = self.translator.MAX_COUNT_TEXTS
        count_lists = len(phrases) // limit_count_translate + 1

        translated_phrases = []
        for index_list_pages in range(count_lists):
            translate_from = index_list_pages * limit_count_translate
            translate_to = translate_from + limit_count_translate
            translated_phrases += self.translator.translate_text(
                phrases[translate_from: translate_to], translate_to_language
            )
        return translated_phrases

    def generate_new_name(self, subtitles_file_path, translate_to_language):
        filename, file_extension = os.path.splitext(subtitles_file_path)
        return filename + self.add_name_translated_file + translate_to_language + file_extension

    @staticmethod
    def write_file(new_name_subtitles, translated_lines):
        with open(new_name_subtitles, 'w') as file_:
            file_.writelines(translated_lines)


def translate_subtitle(subtitles_file_path, translate_to_language):
    from credentials import YandexTranslatorAPICredential
    from translator import YandexTranslator

    translator = YandexTranslator(
        YandexTranslatorAPICredential.get_credentials(),
    )
    SubtitlesTranslator(translator).translate(
        subtitles_file_path, translate_to_language
    )


def directory_translate_subtitles(directory, translate_from_lang,
                                  translate_to_lang, recursive=False):
    from credentials import YandexTranslatorAPICredential
    from translator import YandexTranslator

    translator = YandexTranslator(
        YandexTranslatorAPICredential.get_credentials(),
    )
    sub_translate_func = SubtitlesTranslator(translator).translate
    directory_translator = DirectoryWithSubtitlesTranslate(sub_translate_func)
    directory_translator.translate_subtitles(
        directory, translate_from_lang, translate_to_lang, recursive
    )


if __name__ == '__main__':
    # sub_translate('01_non-linear-hypotheses.en.srt', 'ru')
    # directory = 'youtube/to_google'
    # directory_subs_translate(directory, 'en', 'ru')
    translate_subtitle('youtube/aaa/Creating Awesome 3D Animations With '
                       'Python In Blender.en.srt', 'ru')
