import requests
from tqdm import tqdm

from file import download_file, AudioSetSortlist


def download_from_abook_info():
    files_dir = 'files/bern_igry_v_kotorye_igrajut_ljudi'

    url = 'https://abooks.info/?audioigniter_playlist_id=3197'
    response_data = requests.get(url).json()

    print('Start download files')
    for part in tqdm(response_data[50:]):
        download_file(part['audio'], download_to=files_dir)

    print('Sort files')
    AudioSetSortlist(files_dir).sort()


if __name__ == '__main__':
    download_from_abook_info()
