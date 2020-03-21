import bs4
import requests
from tqdm import tqdm

from file import download_file, AudioSetSortlist


def download_from_knigavuhe():
    # example template 'http://audio.rmail.pro/audio/brandon_sanderson/002/{index}.mp3'
    files_dir = 'files/akademija'

    url = 'https://knigavuhe.org/book/akademija/'
    file_path_template = 'https://s2.knigavuhe.org/1/audio/1939/{index}.mp3'

    content = bs4.BeautifulSoup(requests.get(url).content, 'html.parser')

    blocks_with_mp3_data = content.find_all(
        True, {'class': ['book_playlist_item_name']},
    )

    print('Download files')
    for block in tqdm(blocks_with_mp3_data):
        mp3_file_path = file_path_template.format(index=block.contents[0])
        download_file(mp3_file_path, download_to=files_dir)

    print('Sort files')
    AudioSetSortlist(files_dir).sort()


if __name__ == '__main__':
    download_from_knigavuhe()

# https://audioknigi.club/strugackie-paren-iz-preispodney
