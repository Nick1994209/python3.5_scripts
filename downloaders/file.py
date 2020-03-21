import os

import mutagen
import requests
from mutagen.easyid3 import EasyID3
from tqdm import tqdm


def download_file(
        remote_file_path,
        file_name=None,
        download_to='files',
        show_progress=True,
        **request_kwargs
):
    if not os.path.exists(download_to):
        os.makedirs(download_to)

    if not file_name:
        file_name = remote_file_path.rsplit('/')[-1]

    response = requests.get(remote_file_path, **request_kwargs)
    response.raise_for_status()

    total_length = response.headers.get('content-length')
    total_length = total_length and convert_to_readable(int(total_length)) or 'undefined'

    downloaded = 0

    if show_progress:
        print(file_name, total_length)

    with open(os.path.join(download_to, file_name), 'wb') as to_file:
        chunk_size = 4096  # bytes
        for chunk in response.iter_content(chunk_size=chunk_size):
            to_file.write(chunk)
            downloaded += chunk_size
            if show_progress:
                print(
                    f"\r[downloaded: {convert_to_readable(downloaded)}; total: {total_length}]",
                    end='',
                )


def convert_to_readable(file_size: int):  # bytes
    mb = 1024 * 1024
    kb = 1024
    if file_size // mb > 0:
        return f'{round(file_size / mb, 1)}Mb'
    if file_size // kb > 0:
        return f'{round(file_size / kb, 1)}Kb'
    else:
        return f'{file_size}b'


class AudioSetSortlist:
    """
    Часто бывает, что ауидотреки в плейлисте на телефоне не в том порядке, что и на компе-
        решаем эту проблему =)
    """

    def __init__(self, directory_from, files_with_extensions=('mp3',)):
        self.directory = directory_from
        self.files_with_extensions = files_with_extensions

    def sort(self, from_directory_path=None, recursive=True):
        is_main_directory = from_directory_path
        from_directory_path = from_directory_path or self.directory

        main_files_or_directories = os.listdir(from_directory_path)
        if is_main_directory is None:
            main_files_or_directories = tqdm(main_files_or_directories)

        for name in main_files_or_directories:
            path = os.path.join(from_directory_path, name)
            if os.path.isdir(path):
                if recursive:
                    self.sort(path)
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


if __name__ == '__main__':
    # AudioSetSortlist('/Users/n.korolkov/Downloads/pasha-i-papa').sort()
    download_file('https://smartreading.ru/file/media/227/MP3/get/file.mp3?v1',
                  'принцип пирамиды минто.mp3')
