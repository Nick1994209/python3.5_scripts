import os
import re
from typing import Tuple, Dict, List
from datetime import timedelta

SUBTITLES_TIME = Tuple[timedelta, timedelta]  # from_time, end_time

COUNTER_INDEX = 0
INDEX_TIME = 1
FROM_SENTENCES_INDEX = 2

SUBTITLES_PART_SPLITTER = '\n\n'


class DirectorySubtitlesRepair:
    subtitles_ext = '.srt'

    @classmethod
    def find_subtitles_and_edit(cls, directory, recursive=True):
        list_files_with_directories = os.listdir(directory)

        for path in list_files_with_directories:
            path = os.path.join(directory, path)
            if os.path.isdir(path) and recursive:
                cls.find_subtitles_and_edit(path)
            elif path.lower().endswith(cls.subtitles_ext):
                EditImpositionTimeInSubtitles.edit(path)  # такое ощущение, что больше не надо
                DeleteNotUsedStrings(path).delete()


class EditImpositionTimeInSubtitles:
    time_reg = '(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)'

    @classmethod
    def edit(cls, subtitles_path, edited_subtitle_path=None):
        with open(subtitles_path, 'r', encoding='utf-8') as _file:
            subtitle_strings = list(_file.readlines())

        index_line_with_time, times = None, None

        for current_index, current_line in enumerate(subtitle_strings):
            current_times = cls.get_subtitle_time(current_line)
            if not current_times:
                continue

            if index_line_with_time and cls.imposition_of_times(times, current_times):
                start_time, end_time = times[0], current_times[0]
                time_string = cls.to_string_time(start_time, end_time) + '\n'
                subtitle_strings[index_line_with_time] = time_string

            index_line_with_time = current_index
            times = current_times

        if edited_subtitle_path is None:
            edited_subtitle_path = subtitles_path
        with open(edited_subtitle_path, 'w', encoding='utf-8') as new_subtitles_file:
            new_subtitles_file.writelines(subtitle_strings)

    @classmethod
    def get_subtitle_time(cls, string: str) -> SUBTITLES_TIME:
        find_time = re.findall(cls.time_reg, string)

        if not find_time:
            return None

        find_time = find_time.pop()
        hours1, minutes1, seconds1, microseconds1 = map(int, find_time[0:4])
        hours2, minutes2, seconds2, microseconds2 = map(int, find_time[4:])
        return (timedelta(hours=hours1, minutes=minutes1,
                          seconds=seconds1, microseconds=microseconds1),
                timedelta(hours=hours2, minutes=minutes2, seconds=seconds2,
                          microseconds=microseconds2))

    @staticmethod
    def imposition_of_times(old_times, new_times):
        """наложение времен, друг на друга"""
        start_old_time, end_old_time = old_times
        start_new_time, end_new_time = new_times
        return end_old_time > start_new_time

    @classmethod
    def to_string_time(cls, start_time, end_time):
        return '{}:{}:{},{} --> {}:{}:{},{}'.format(
            *cls.get_days_hours_minutes_secconds(start_time),
            *cls.get_days_hours_minutes_secconds(end_time),
        )

    @staticmethod
    def get_days_hours_minutes_secconds(time_delta):
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds, time_delta.microseconds


class DeleteNotUsedStrings:
    """
    Deleted and union parts subtitles if required

    from bad version:
        81
        00:01:39,630 --> 00:01:42,319
        them through the bpy module you can also
        manipulate and generate objects within

        82
        00:01:42,319 --> 00:01:42,329
        manipulate and generate objects within       # this part is required union with previous


        83
        00:01:42,329 --> 00:01:46,460
        manipulate and generate objects within       # this sentence is required delete
        the scene you can emulate UI commands so
    """

    def __init__(self, subtitle_path):
        self.path = subtitle_path

    def delete(self):
        with open(self.path, encoding='utf-8') as f:
            subtitles = f.read()

        split_parts = subtitles.split(SUBTITLES_PART_SPLITTER)
        split_parts = self.delete_not_used_strings(split_parts)
        self.set_recount(split_parts)

        with open(self.path, 'w', encoding='utf-8') as f:
            for split_part in split_parts:
                f.write('\n'.join(split_part) + SUBTITLES_PART_SPLITTER)

    def delete_not_used_strings(self, split_parts):
        result = []
        previous_sentences = None
        for part in split_parts:
            sentences = part.split('\n')
            sentences = self.delete_blank_strings(sentences)
            if len(sentences) <= 2:
                continue

            sentences = self.get_unique_sentences(previous_sentences, sentences)
            union_sentences = self.union_sentences(previous_sentences, sentences)
            if union_sentences:
                result.pop()
                sentences = union_sentences

            result.append(sentences)
            previous_sentences = sentences
        return result

    @staticmethod
    def delete_blank_strings(part_subtitles):
        return [s for s in part_subtitles if re.search('\w+', s)]

    @staticmethod
    def get_unique_sentences(previous_sentences, current_sentences):
        if not previous_sentences:
            return current_sentences

        # on first sentences [number, time, ...subtitles]
        previous_subtitles = previous_sentences[FROM_SENTENCES_INDEX:]
        current_subtitles = current_sentences[FROM_SENTENCES_INDEX:]

        changes = [s for s in current_subtitles if s not in previous_subtitles]
        if not changes:
            return current_sentences

        return current_sentences[:FROM_SENTENCES_INDEX] + changes

    @staticmethod
    def union_sentences(previous_sentences, current_sentences):
        if not previous_sentences:
            return None

        if previous_sentences[FROM_SENTENCES_INDEX:] != current_sentences[FROM_SENTENCES_INDEX:]:
            return None

        start, _ = EditImpositionTimeInSubtitles.get_subtitle_time(previous_sentences[INDEX_TIME])
        _, end = EditImpositionTimeInSubtitles.get_subtitle_time(current_sentences[INDEX_TIME])
        time_str = EditImpositionTimeInSubtitles.to_string_time(start, end)
        return [
            current_sentences[0],
            time_str,
            *current_sentences[FROM_SENTENCES_INDEX:]
        ]

    @staticmethod
    def set_recount(parts_sentences):
        """
        change index

        [['index', 'time', ...subtitles], ]
        """
        for index, part in enumerate(parts_sentences):
            part[0] = str(index + 1)


class DirectoryUnionSubtitles:
    subtitles_ext = '.srt'

    def __init__(self, directory, main_language='en', sub_language='ru', recursive=True):
        self.directory = directory
        if not main_language or not sub_language:
            raise Exception('Required set main_language "%s", or sub_language "%s"' % (
                main_language, sub_language,
            ))
        self.main_language = main_language
        self.sub_language = sub_language
        self.recursive = recursive
        self.result_end_file = '%s-%s%s' % (
            main_language or 'from', sub_language or 'to', self.subtitles_ext,
        )

    def find_subtitles_and_union(self, directory=None):
        if directory is None:
            directory = self.directory

        main_file_end = self.main_language + self.subtitles_ext

        directory_files = os.listdir(self.directory)
        for file_name in directory_files:
            path = os.path.join(self.directory, file_name)

            if os.path.isdir(path) and self.recursive:
                self.find_subtitles_and_union(path)
            elif file_name.endswith(self.result_end_file):
                continue
            elif file_name.endswith(main_file_end):
                base_name = file_name.replace(main_file_end, '', -1)
                founded_sub_subtitles_name = self.find_sub_subtitle(directory_files, base_name)
                if not founded_sub_subtitles_name:
                    continue

                subtitles_sub_path = os.path.join(directory, founded_sub_subtitles_name)
                result = os.path.join(directory, base_name + self.result_end_file)
                UnionSubtitlesTwoLanguage(path, subtitles_sub_path, result).union()

    def find_sub_subtitle(self, files_names: List[str], base_file_name: str):
        for f_name in files_names:
            if not f_name.startswith(base_file_name):
                continue

            if f_name.endswith(self.result_end_file):
                return None
            elif f_name.endswith(self.sub_language + self.subtitles_ext):
                return f_name
        return None


class UnionSubtitlesTwoLanguage:
    def __init__(self, subtitles_main_path, subtitles_sub_path, result_path,
                 delete_not_used_str=False, mod='simple'):
        self.subtitles_main_path = subtitles_main_path
        self.subtitles_sub_path = subtitles_sub_path
        self.result_path = result_path
        self.delete_not_used_str = delete_not_used_str
        self.mod = mod  # simple or top_bottom
        self.main_sentences_styles = ('<b>', '</b>')
        self.sub_sentences_styles = ('<i>', '</i>')

    def union(self):
        if self.delete_not_used_str:
            DeleteNotUsedStrings(self.subtitles_main_path).delete()
            DeleteNotUsedStrings(self.subtitles_sub_path).delete()

        with open(self.subtitles_main_path, encoding='utf-8', ) as f1, open(self.subtitles_sub_path,
                                                                            encoding='utf-8') as f2:
            subtitles_main = f1.read()
            subtitles_sub = f2.read()

        split_parts_main = subtitles_main.split('\n\n')
        split_parts_sub = subtitles_sub.split('\n\n')

        union_parts = self.union_parts(split_parts_main, split_parts_sub)

        with open(self.result_path, 'w', encoding='utf-8') as f:
            for part in union_parts:
                f.write(part + SUBTITLES_PART_SPLITTER)

    def union_parts(self, split_parts_main, split_parts_sub):
        time_subtitles_2 = self.get_time_subtitles(split_parts_sub)

        result = []
        counter = 1
        for part in split_parts_main:
            sentences = part.split('\n')
            if len(sentences) < FROM_SENTENCES_INDEX:
                continue

            time = EditImpositionTimeInSubtitles.get_subtitle_time(sentences[INDEX_TIME])
            sub_sentences = time_subtitles_2.get(time, []) if time else []

            union_sentences = self._union_parts(
                counter,
                sentences[INDEX_TIME],
                sentences[FROM_SENTENCES_INDEX:],
                sub_sentences,
            )
            counter += 1
            result.append(union_sentences)

        return result

    @staticmethod
    def get_time_subtitles(split_parts: List[str]) -> Dict[SUBTITLES_TIME, List[str]]:
        result = {}

        for split_part in split_parts:
            sentences = split_part.split('\n')
            if len(sentences) < FROM_SENTENCES_INDEX:
                continue

            time = EditImpositionTimeInSubtitles.get_subtitle_time(sentences[INDEX_TIME])
            result[time] = sentences[FROM_SENTENCES_INDEX:]
        return result

    def _union_parts(self, counter: int, time: SUBTITLES_TIME,
                     main_sentences: list, sub_sentences: list):

        main_sentences = self.prepare_string(self.main_sentences_styles, main_sentences)
        edited_sub_sentences = self.prepare_string(self.sub_sentences_styles, sub_sentences)

        if self.mod == 'simple':
            return self.simple_union(counter, time, main_sentences, edited_sub_sentences)
        elif self.mod == 'top_bottom':
            return self.top_bottom_union(counter, time, main_sentences, edited_sub_sentences)
        raise NotImplemented('mod "%s" is not implemented' % self.mod)

    @staticmethod
    def prepare_string(sentence_style: Tuple[str, str], sentences: List[str]):
        return ['%s%s%s' % (sentence_style[0], s.strip(), sentence_style[1]) for s in sentences]

    @staticmethod
    def simple_union(counter, time, main_sentences, sub_sentences):
        return '\n'.join([str(counter), time, *main_sentences, *sub_sentences])

    @staticmethod
    def top_bottom_union(counter, time, main_sentences, sub_sentences):
        bottom_counter = str(counter * 2 - 1)
        top_counter = str(counter * 2)

        bottom_part = '\n'.join([bottom_counter, time, *main_sentences, ])

        sub_sentences_part = '{\\an8}' + '\n'.join(sub_sentences)
        top_part = '\n'.join([top_counter, time, sub_sentences_part, ])

        return SUBTITLES_PART_SPLITTER.join(
            [bottom_part, top_part],
        )


class DirectoryCopySubtitlesAndSetSubName:
    subtitles_ext = '.srt'

    def __init__(self, directory, subtitles_sub_name='.en', to_directory=None):
        self.directory = directory
        self.sub_name = subtitles_sub_name
        self.to_directory = to_directory or self.directory

    def find_subtitles_and_set_subname(self):

        directory_files = os.listdir(self.directory)
        for file_name in directory_files:

            if file_name.endswith(self.subtitles_ext):
                result_name = '%s%s%s' % (
                    file_name.replace(self.subtitles_ext, '', -1),
                    self.sub_name,
                    self.subtitles_ext
                )
                # print(os.path.join(self.directory, file_name))
                # print(os.path.join(self.directory, result_name))
                # os.rename(
                #     os.path.join(self.directory, file_name),
                #     os.path.join(self.to_directory, result_name),
                # )

                import shutil
                shutil.copyfile(
                    os.path.join(self.directory, file_name),
                    os.path.join(self.to_directory, result_name),
                )


if __name__ == '__main__':
    DirectorySubtitlesRepair.find_subtitles_and_edit('youtube/asyncio')
    # EditImpositionTimeInSubtitles.edit('youtube/aaa/Creating Awesome 3D Animations With Python In Blender.en.srt')
    # DeleteNotUsedStrings('youtube/aaa/Creating Awesome 3D Animations With Python In Blender.en.srt').delete()
    # UnionSubtitlesTwoLanguage(
    #     'youtube/aaa/Creating Awesome 3D Animations With Python In Blender.en.srt',
    #     'youtube/aaa/Creating Awesome 3D Animations With Python In Blender.ru.srt',
    #     'youtube/aaa/Creating Awesome 3D Animations With Python In Blender.en-ru.srt',
    #     delete_not_used_str=True,
    # ).union()
    # DirectoryUnionSubtitles('youtube/aaa/').find_subtitles_and_union()
    # DirectoryUnionSubtitles('youtube/Doctor Who Series 3 (2007)/', 'en', 'rus',
    #                         recursive=False).find_subtitles_and_union()
    # DirectoryUnionSubtitles('youtube/ml_google', 'en', 'ru',
    #                         recursive=False).find_subtitles_and_union()
    # DirectorySetEngSubtitlesAndCopy(
    #     'youtube/Doctor Who Series 3 (2007)/Subtitles',
    #     to_directory='youtube/Doctor Who Series 3 (2007)/',
    # ).find_subtitles_and_set_subname()
