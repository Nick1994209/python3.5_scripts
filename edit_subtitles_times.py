import os
import re
from datetime import timedelta


class DirectoryWithSubtitlesEditImpositionTime:
    subtitles_ext = '.srt'

    @classmethod
    def find_subtitles_and_edit(cls, directory, recursive=True):
        list_files_with_directories = os.listdir(directory)

        for path in list_files_with_directories:
            path = os.path.join(directory, path)
            if os.path.isdir(path) and recursive:
                cls.find_subtitles_and_edit(path)
            elif path.lower().endswith(cls.subtitles_ext):
                EditImpositionTimeInSubtitles.edit(path)


class EditImpositionTimeInSubtitles:
    time_reg = '(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)'

    @classmethod
    def edit(cls, subtitles_path):
        with open(subtitles_path) as _file:
            subtitle_strings = list(_file.readlines())

        index_line_with_time, times = None, None

        for current_index, current_line in enumerate(subtitle_strings):
            current_times = cls.get_subtitle_time(current_line)
            if not current_times:
                continue

            if index_line_with_time and cls.imposition_of_times(times, current_times):
                start_time, end_time = times[0], current_times[0]
                time_string = cls.to_string_time(start_time, end_time)
                subtitle_strings[index_line_with_time] = time_string

            index_line_with_time = current_index
            times = current_times

        with open(subtitles_path, 'w') as new_subtitles_file:
            new_subtitles_file.writelines(subtitle_strings)

    @classmethod
    def get_subtitle_time(cls, string):
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
        return '{}:{}:{},{} --> {}:{}:{},{}\n'.format(
            *cls.get_days_hours_minutes_secconds(start_time),
            *cls.get_days_hours_minutes_secconds(end_time),
        )

    @staticmethod
    def get_days_hours_minutes_secconds(time_delta):
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds, time_delta.microseconds


if __name__ == '__main__':
    DirectoryWithSubtitlesEditImpositionTime.find_subtitles_and_edit('youtube')
