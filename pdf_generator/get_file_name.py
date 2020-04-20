import os
import re

from pdf_generator.generator import get_sorted_func

directory = '/Users/n.korolkov/Documents/Mangas/Дорохедоро'
for file_name in os.listdir(directory):
    manga_part = get_sorted_func()(file_name)
    matches_name = re.findall(r'[A-Za-zА-Яа-я]+', file_name.rstrip('.pdf'))
    name = '_'.join(matches_name)

    result_name = f'{manga_part}-{name}.pdf'
    os.rename(os.path.join(directory, file_name), os.path.join(directory, result_name))
