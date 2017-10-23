import mutagen
import re
import shutil
import subprocess
import os
from mutagen.easyid3 import EasyID3
from tqdm import tqdm


class DeleteUnnecessaryFiles:
    def __init__(self, directory, need_delete_files_with_extensions=(),
                 need_leave_files_with_path_ends=()):
        self.directory = directory
        self.need_delete_files_with_extensions = need_delete_files_with_extensions
        self.need_leave_files_with_path_ends = need_leave_files_with_path_ends

    def main(self, from_directory_path=None):
        from_directory_path = from_directory_path or self.directory

        for name in os.listdir(from_directory_path):
            path = os.path.join(from_directory_path, name)
            if os.path.isdir(path):
                self.main(path)

            if not self.is_file_with_delete_extension(path):
                continue
            if self.is_need_leave_file(path):
                continue
            print(path)
            os.remove(path)

    def is_file_with_delete_extension(self, file_path):
        for extension in self.need_delete_files_with_extensions:
            if file_path.endswith(extension):
                return True
        return False

    def is_need_leave_file(self, file_path):
        for end_file_path in self.need_leave_files_with_path_ends:
            if file_path.endswith(end_file_path):
                return True
        return False

    @staticmethod
    def get_need_leave_files_with_ends(contains_symbols, extensions, splitter='.'):
        return [lang + splitter + ext for lang in contains_symbols for ext in extensions]


class CopyFilesHelper:
    def __init__(self, directory_from, directory_to, files_with_extensions='*',
                 regexp_for_get_filename_base_from_path='\d+'):
        """

        :param directory_from: 
        :param directory_to: 
        :param files_with_extensions: list or '*'
        :param regexp_for_get_filename_base_from_path: 
        """
        if not os.path.exists(directory_to):
            os.makedirs(directory_to)
        self.directory_from, self.directory_to = directory_from, directory_to
        self.files_with_extensions = files_with_extensions
        self.regexp_for_get_filename_base_from_path = regexp_for_get_filename_base_from_path

    def main(self, from_directory_path=None):
        is_main_directory = from_directory_path
        from_directory_path = from_directory_path or self.directory_from

        main_files_or_directories = os.listdir(from_directory_path)
        if is_main_directory is None:
            main_files_or_directories = tqdm(main_files_or_directories)

        for name in main_files_or_directories:
            path = os.path.join(from_directory_path, name)
            if os.path.isdir(path):
                self.main(path)
                continue

            if not self.is_file_with_reset_extension(path):
                continue
            shutil.copyfile(path, os.path.join(self.directory_to, self.get_file_name(path)))

    def is_file_with_reset_extension(self, file_path):
        if self.files_with_extensions is '*':
            return True
        for extension in self.files_with_extensions:
            if file_path.endswith(extension):
                return True
        return False

    def get_file_name(self, file_path):
        directory, name = os.path.split(file_path)
        sequence = re.findall(self.regexp_for_get_filename_base_from_path, directory)
        if sequence:
            return ''.join(sequence) + '_' + name
        return name


class AudioSetSortlist:
    """
    Часто бывает, что ауидотреки в плейлисте на телефоне не в том порядке, что и на компе-
        решаем эту проблему =)
    """
    def __init__(self, directory_from, files_with_extensions=('mp3', )):
        self.directory = directory_from
        self.files_with_extensions = files_with_extensions

    def main(self, from_directory_path=None):
        is_main_directory = from_directory_path
        from_directory_path = from_directory_path or self.directory

        main_files_or_directories = os.listdir(from_directory_path)
        if is_main_directory is None:
            main_files_or_directories = tqdm(main_files_or_directories)

        for name in main_files_or_directories:
            path = os.path.join(from_directory_path, name)
            if os.path.isdir(path):
                self.main(path)
                continue

            if not self.is_file_with_extension(path):
                continue
            # self.check_albumsort(path)
            self.set_albumsort(path)

    def is_file_with_extension(self, file_path):
        if self.files_with_extensions is '*':
            return True
        for extension in self.files_with_extensions:
            if file_path.endswith(extension):
                return True
        return False

    @staticmethod
    def set_albumsort(file_path):
        _, name = os.path.split(file_path)
        try:
            audio_meta = EasyID3(file_path)
        except mutagen.id3.ID3NoHeaderError:
            audio_meta = mutagen.File(file_path, easy=True)
            audio_meta.add_tags()
        audio_meta['albumsort'] = name
        audio_meta['title'] = name
        audio_meta.save()

    @staticmethod
    def check_albumsort(file_path):
        EasyID3(file_path)
        print(file_path)


class ConvertVideo:
    def __init__(self, directory, from_extension, to_extension):
        self.directory = directory
        self.from_extension = from_extension.lower()
        self.to_extension = to_extension.lower()

    def run(self):
        self._main()

    def _main(self, from_directory_path=None):
        is_main_directory = from_directory_path
        from_directory_path = from_directory_path or self.directory

        main_files_or_directories = os.listdir(from_directory_path)
        if is_main_directory is None:
            main_files_or_directories = tqdm(main_files_or_directories)

        for name in main_files_or_directories:
            path = os.path.join(from_directory_path, name)
            if os.path.isdir(path):
                self._main(path)
                continue

            if self.is_file_with_extension(path):
                self.convert_video(path)

    def is_file_with_extension(self, file_path):
        if file_path.lower().endswith(self.from_extension):
            return True
        return False

    def convert_video(self, file_path):
        _, name = os.path.split(file_path)
        """
        fmpeg -i лучшие/\ 06-Можно\ ли\ верить\ гороскопам—\ Научпок.webm a.mp4
        """
        # file_path = file_path.replace(' ', r'\ ')

        # to_path = '{}.{}'.format(name, self.to_extension)
        import re
        # file_path = re.sub(' ', '\ ', file_path)
        to_path = file_path + '.' + self.to_extension

        # command = 'ffmpeg -i {file_path} {to_path}'.format(file_path=file_path, to_path=to_path)
        # command = 'ffmpeg -i ' + file_path + ' ' + to_path
        # print(repr(command))
        subprocess.check_call(['ffmpeg', '-i', file_path, to_path])
        # subprocess.check_call(repr(command))
        os.remove(file_path)


if __name__ == '__main__':
    pass
    # extensions = ['vtt', 'srt']
    # languages = ['ru', 'en']
    # need_leave_files_with_ends = DeleteUnnecessaryFiles.get_need_leave_files_with_ends(
    #     languages, extensions)
    # DeleteUnnecessaryFiles('coursera', ['srt', 'txt'], ['en.srt', 'ru.srt', 'ru.txt', 'en.txt'], ).main()
    # DeleteUnnecessaryFiles('coursera_show', ['html', ], ).main()
    #
    # CopyFilesHelper('coursera/mfti/supervised-learning', 'coursera_show/mfti-2supervised-learning', ['mp4', 'srt'], '\d+_').main()
    # CopyFilesHelper('coursera/algorithmic-thinking-1', 'coursera_show/algorithmic-thinking', ['mp4', 'srt'], '\d+_').main()
    # CopyFilesHelper('coursera/machine-learning', 'coursera_show/machine-learning', ['mp4', 'srt'], '\d+_').main()
    AudioSetSortlist('/Users/n.korolkov/Documents/audiobook').main()
    # ConvertVideo('youtube/научлок', from_extension='webm', to_extension='mp4').run()
