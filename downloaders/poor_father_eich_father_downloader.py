from tqdm import tqdm

from file import download_file, AudioSetSortlist


def download_from_audiokniga(audiobook, template, from_file_index, to_file_index):
    # example template 'uploads/books/book202/rus/reader107/128/{index}.mp3'
    page = 'https://audiokniga.club/'
    files_dir = 'files/' + audiobook

    print('Download files')
    for index in tqdm(range(from_file_index, to_file_index + 1)):
        raw_index_mp3 = ('000' + str(index))
        n = len(raw_index_mp3)
        max_count_symbols = 3
        index_mp3 = raw_index_mp3[n - max_count_symbols:]
        mp3_file_path = page + template.format(index=index_mp3)
        download_file(mp3_file_path, download_to=files_dir)

    print('Sort files')
    AudioSetSortlist(files_dir).sort()


def download_father_rich():
    template = 'uploads/books/book202/rus/reader107/128/{index}.mp3'
    download_from_audiokniga('rich_poor_father', template, 1, 31)


if __name__ == '__main__':
    download_father_rich()
