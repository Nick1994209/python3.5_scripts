import os
import re

import bs4
import requests
from furl import furl
from tqdm import tqdm


def download_from_histrf():
    page = 'http://histrf.ru/lectorium/audio-coursebook'

    content = bs4.BeautifulSoup(requests.get(page).content, 'html.parser')
    blocks_with_mp3_data = content.find_all(
        True, {'class': ['list-item', 'clearfix', 'video-list']})

    for block_with_mp3_data in tqdm(blocks_with_mp3_data):
        description = block_with_mp3_data.find(True, {'class': 'left-part'})
        source = block_with_mp3_data.find('source')

        if source and description:
            mp3 = block_with_mp3_data.find('source')['src']
            about_mp3 = description.find('span').text

            # full_file_name = re.findall('\w*-.*\.mp3', mp3)
            file_sequence = re.findall('\d+-\d+', mp3)[0]
            _, extension = os.path.splitext(mp3)

            file_name = file_sequence + ' ' + about_mp3 + extension

            f = furl(page)
            f.path = mp3
            download_file(f.url, file_name, 'mp3/histrf')


def download_file(remote_file_path, file_name=None, download_to='files'):
    if not os.path.exists(download_to):
        os.makedirs(download_to)

    response = requests.get(remote_file_path)
    with open(os.path.join(download_to, file_name), 'wb') as to_file:
        for chunk in response.iter_content(chunk_size=1024):
            to_file.write(chunk)


if __name__ == '__main__':
    download_from_histrf()
