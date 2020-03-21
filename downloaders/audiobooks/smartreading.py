import re

from downloaders.file import download_file


def download_summary(url, file_name, cookies):
    summary_id, = re.findall(r'\d+', url)
    download_file(f'https://smartreading.ru/file/media/{summary_id}/MP3/get/file.mp3?v1',
                  file_name, cookie=cookies)


if __name__ == '__main__':
    from credentials import Credential

    # from browser document.cookie
    # cookies = {c.split('=')[0]: c.split('=')[1] for c in raw_cookies.split('; ')}
    # Credential.add_credentials('smartreading', cookies)
    cookies = Credential.get_credentials_by_key('smartreading')

    download_summary('https://smartreading.ru/summary/498',
                     'Проверенный способ поднять боевой дух и улучшить результаты.mp3',
                     cookies=cookies)